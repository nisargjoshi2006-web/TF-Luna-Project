import serial
import serial.tools.list_ports
import json
import time
import os
import numpy as np

BAUDRATE = 115200
CALIBRATION_FILE = 'data/calibration.json'

def get_arduino_port():
    ports = serial.tools.list_ports.comports()
    for p in ports:
        if "Arduino" in p.description or "CH340" in p.description or "USB Serial" in p.description:
            return p.device
    for p in ports:
        if "Bluetooth" not in p.description:
            return p.device
    return 'COM9'

def capture_samples(arduino, target_cm, num_samples=30):
    readings = []
    print(f"\n[RECORDING] Please keep sensor pointed steadily at {target_cm:.1f} cm target...")
    
    while len(readings) < num_samples:
        try:
            line = arduino.readline().decode('utf-8', errors='ignore').strip()
            if not line:
                continue
            parts = line.split(',')
            if len(parts) >= 3:
                val = float(parts[2])
            elif len(parts) == 1 and parts[0].replace('.', '', 1).isdigit():
                val = float(parts[0])
            else:
                continue

            if val > 0:
                readings.append(val)
                print(f"  Sample {len(readings)}/{num_samples}: Measured = {val:.2f} cm")
        except Exception:
            pass

    avg_measured = float(np.mean(readings))
    std_dev = float(np.std(readings))
    print(f"--> Target: {target_cm:.1f} cm | Average Measured: {avg_measured:.2f} cm | Std Dev: {std_dev:.2f} cm")
    return avg_measured, std_dev

def run_multi_point_calibration():
    print("=" * 60)
    print("   TF-LUNA PROFESSIONAL MULTI-POINT REGRESSION CALIBRATION   ")
    print("=" * 60)
    
    port = get_arduino_port()
    print(f"[AUTO-DETECT] Connecting to Arduino on {port}...")

    try:
        arduino = serial.Serial(port, BAUDRATE, timeout=2)
        time.sleep(2)
    except Exception as e:
        print(f"\n[ERROR] Could not open {port}: {e}")
        print("Tip: Make sure the Arduino IDE Serial Monitor is CLOSED.")
        return

    print("\nWe will record data at 3 distinct reference distances (e.g. 50cm, 100cm, 200cm).")
    
    targets = []
    measured_points = []
    stds = []

    for i in range(1, 4):
        print("-" * 50)
        while True:
            try:
                user_dist = float(input(f"Enter Reference Distance #{i} (in cm) [e.g. {50 if i==1 else (100 if i==2 else 200)}]: "))
                if user_dist <= 0:
                    print("Please enter a positive distance.")
                    continue
                break
            except ValueError:
                print("Invalid input. Enter a valid numerical value in cm.")
        
        input(f"Place the sensor exactly {user_dist:.1f} cm from target, then press ENTER to measure...")
        avg_m, s_dev = capture_samples(arduino, user_dist, num_samples=30)
        targets.append(user_dist)
        measured_points.append(avg_m)
        stds.append(s_dev)

    arduino.close()

    # Linear Regression: True = Slope * Measured + Intercept
    x = np.array(measured_points)
    y = np.array(targets)
    
    # Calculate best fit line (y = mx + c)
    slope, intercept = np.polyfit(x, y, 1)

    # Calculate R-squared (Coefficient of Determination)
    y_pred = slope * x + intercept
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r_squared = float(1 - (ss_res / ss_tot)) if ss_tot != 0 else 1.0

    print("\n" + "=" * 60)
    print("               CALIBRATION MODEL SUMMARY                     ")
    print("=" * 60)
    for i in range(3):
        print(f"Point {i+1}: True = {targets[i]:6.1f} cm  |  Raw Measured = {measured_points[i]:6.2f} cm (Error: {targets[i]-measured_points[i]:+6.2f} cm)")
    print("-" * 60)
    print(f"Regression Formula : Calibrated = ({slope:.4f} * Raw) + ({intercept:+.4f})")
    print(f"Slope (Gain m)     : {slope:.4f}")
    print(f"Intercept (Offset c): {intercept:+.4f} cm")
    print(f"R² Accuracy Score  : {r_squared:.5f} (1.0000 = Ideal)")
    print("=" * 60)

    # Save to JSON
    os.makedirs('data', exist_ok=True)
    calib_data = {
        "model_type": "Linear_Regression",
        "slope_m": round(float(slope), 4),
        "intercept_c": round(float(intercept), 4),
        "r_squared": round(r_squared, 5),
        "calibration_points": [
            {"true_cm": targets[i], "measured_cm": round(measured_points[i], 2), "std_cm": round(stds[i], 2)}
            for i in range(3)
        ],
        "calibrated_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    with open(CALIBRATION_FILE, 'w') as f:
        json.dump(calib_data, f, indent=4)

    print(f"\n[SUCCESS] Calibration model saved to '{CALIBRATION_FILE}'.")
    print("Your live reader and dashboard will now use this high-precision linear model!")

if __name__ == "__main__":
    run_multi_point_calibration()
