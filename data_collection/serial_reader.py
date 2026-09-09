import serial
import serial.tools.list_ports
import csv
import os
import json
import statistics
from collections import deque

BAUDRATE = 115200
CALIBRATION_FILE = 'data/calibration.json'
DATA_FILE = 'data/distance_data.csv'
FILTER_WINDOW_SIZE = 8

def get_arduino_port():
    ports = serial.tools.list_ports.comports()
    for p in ports:
        if "Arduino" in p.description or "CH340" in p.description or "USB Serial" in p.description:
            return p.device
    for p in ports:
        if "Bluetooth" not in p.description:
            return p.device
    return 'COM9'

# Load Calibration Model (Linear Regression)
slope_m = 1.0
intercept_c = 0.0

if os.path.exists(CALIBRATION_FILE):
    try:
        with open(CALIBRATION_FILE, 'r') as f:
            calib = json.load(f)
            slope_m = calib.get("slope_m", 1.0)
            intercept_c = calib.get("intercept_c", calib.get("offset_error_cm", 0.0))
            r2 = calib.get("r_squared", "N/A")
            print(f"[REGRESSION MODEL ACTIVE] Calibrated = ({slope_m:.4f} * Raw) + ({intercept_c:+.2f}) | R² = {r2}")
    except Exception:
        pass

port = get_arduino_port()
print(f"[AUTO-DETECT] Connecting to Arduino on {port}...")

os.makedirs('data', exist_ok=True)
try:
    arduino = serial.Serial(port, BAUDRATE)
except Exception as e:
    print(f"[ERROR] Could not open {port}: {e}")
    print("Please close Arduino IDE Serial Monitor.")
    exit(1)

file_exists = os.path.exists(DATA_FILE)

with open(DATA_FILE, 'a', newline='') as file:
    writer = csv.writer(file)

    if not file_exists or os.path.getsize(DATA_FILE) == 0:
        writer.writerow(["Raw_Distance", "Calibrated_Distance"])

    print("Reading Multi-Point Calibrated & Filtered Data... (Press Ctrl+C to stop)")

    filter_queue = deque(maxlen=FILTER_WINDOW_SIZE)

    while True:
        try:
            line = arduino.readline().decode('utf-8', errors='ignore').strip()
            if not line:
                continue

            parts = line.split(',')
            if len(parts) >= 3:
                raw_dist = float(parts[2])
            elif len(parts) == 1 and parts[0].replace('.', '', 1).isdigit():
                raw_dist = float(parts[0])
            else:
                continue

            if raw_dist > 0:
                # Apply Linear Regression Model: y = m * x + c
                calibrated = (slope_m * raw_dist) + intercept_c
                filter_queue.append(calibrated)

                # Digital Median Filter
                filtered_dist = round(statistics.median(filter_queue), 2)

                print(f"Raw: {raw_dist:6.2f} cm  ==>  Accurate Calibrated: {filtered_dist:6.2f} cm")
                writer.writerow([raw_dist, filtered_dist])
                file.flush()

        except KeyboardInterrupt:
            print("\nStopped.")
            break
        except Exception:
            pass
