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

def run_single_point_calibration():
    print("=" * 60)
    print("      TF-LUNA SINGLE-POINT ZERO-OFFSET CALIBRATION      ")
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

    while True:
        try:
            target_cm = float(input("\nEnter the KNOWN reference distance to the target (in cm) [e.g. 50 or 100]: "))
            if target_cm <= 0:
                print("Please enter a positive distance.")
                continue
            break
        except ValueError:
            print("Invalid input. Enter a numerical value.")

    print(f"\nTarget fixed at: {target_cm:.1f} cm")
    print("Collecting 50 high-precision laser samples...")

    readings = []
    num_samples = 50

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

    arduino.close()

    avg_measured = float(np.mean(readings))
    std_dev = float(np.std(readings))
    offset_error = target_cm - avg_measured

    print("\n" + "=" * 60)
    print("               CALIBRATION RESULTS SUMMARY                    ")
    print("=" * 60)
    print(f"True (Reference) Distance : {target_cm:.2f} cm")
    print(f"Average Measured Reading  : {avg_measured:.2f} cm")
    print(f"Sensor Noise (Std Dev)    : {std_dev:.2f} cm")
    print(f"Calculated Zero Offset    : {offset_error:+.2f} cm")
    print("=" * 60)

    # Save to JSON
    os.makedirs('data', exist_ok=True)
    calib_data = {
        "model_type": "Single_Point_Offset",
        "true_distance_cm": target_cm,
        "measured_avg_cm": round(avg_measured, 2),
        "offset_error_cm": round(offset_error, 2),
        "slope_m": 1.0,
        "intercept_c": round(offset_error, 2),
        "std_dev_cm": round(std_dev, 2),
        "calibration_points": [
            {"true_cm": target_cm, "measured_cm": round(avg_measured, 2), "std_cm": round(std_dev, 2)}
        ],
        "calibrated_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    with open(CALIBRATION_FILE, 'w') as f:
        json.dump(calib_data, f, indent=4)

    print(f"\n[SUCCESS] Saved verified offset ({offset_error:+.2f} cm) to '{CALIBRATION_FILE}'.")
    print("Your reader and dashboard will now automatically apply this exact correction!")

if __name__ == "__main__":
    run_single_point_calibration()
