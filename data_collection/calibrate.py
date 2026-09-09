import serial
import serial.tools.list_ports
import json
import time
import os
import statistics

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

def run_calibration():
    print("=" * 50)
    print("         TF-LUNA LIDAR CALIBRATION TOOL         ")
    print("=" * 50)
    
    port = get_arduino_port()
    print(f"[AUTO-DETECT] Found Arduino on port: {port}")

    try:
        true_distance = float(input("\nEnter the KNOWN actual distance to the target (in cm) [e.g. 30.7 or 100]: "))
    except ValueError:
        print("Invalid input. Please enter a numerical distance in cm.")
        return

    print(f"\nTarget set to: {true_distance:.2f} cm")
    print("Please keep the TF-Luna pointed firmly at the target.")
    print("Opening serial port and collecting 50 samples...")

    try:
        arduino = serial.Serial(port, BAUDRATE, timeout=2)
        time.sleep(2)
    except Exception as e:
        print(f"\n[ERROR] Could not open {port}: {e}")
        print("Tip: Make sure the Arduino Serial Monitor is CLOSED before running this script.")
        return

    readings = []
    sample_count = 50

    while len(readings) < sample_count:
        try:
            line = arduino.readline().decode('utf-8', errors='ignore').strip()
            if not line:
                continue

            parts = line.split(',')
            if len(parts) >= 3:
                val = float(parts[2])  # distance is 3rd column
            elif len(parts) == 1 and parts[0].replace('.', '', 1).isdigit():
                val = float(parts[0])
            else:
                continue

            if val > 0:
                readings.append(val)
                print(f"Sample {len(readings)}/{sample_count}: Measured = {val:.2f} cm")

        except KeyboardInterrupt:
            print("\nCalibration cancelled by user.")
            arduino.close()
            return
        except Exception:
            pass

    arduino.close()

    avg_measured = statistics.mean(readings)
    stdev = statistics.stdev(readings) if len(readings) > 1 else 0.0
    offset_error = true_distance - avg_measured

    print("\n" + "=" * 50)
    print("            CALIBRATION RESULTS                 ")
    print("=" * 50)
    print(f"True (Reference) Distance: {true_distance:.2f} cm")
    print(f"Average Measured Value:   {avg_measured:.2f} cm")
    print(f"Sensor Std Deviation:     {stdev:.2f} cm (stability)")
    print(f"Calculated Error Offset:  {offset_error:+.2f} cm")
    print("=" * 50)

    os.makedirs('data', exist_ok=True)
    calib_data = {
        "true_distance_cm": true_distance,
        "measured_avg_cm": round(avg_measured, 2),
        "offset_error_cm": round(offset_error, 2),
        "scale_factor": 1.0,
        "calibrated_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    with open(CALIBRATION_FILE, 'w') as f:
        json.dump(calib_data, f, indent=4)

    print(f"\n[SUCCESS] Calibration saved to '{CALIBRATION_FILE}'.")
    print("Your data reader and dashboard will now automatically apply this correction!")

if __name__ == "__main__":
    run_calibration()
