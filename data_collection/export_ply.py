import serial
import serial.tools.list_ports
import json
import time
import os
import math

BAUDRATE = 115200
CALIBRATION_FILE = 'data/calibration.json'
OUTPUT_PLY = 'data/live_scan.ply'

def get_arduino_port():
    ports = serial.tools.list_ports.comports()
    for p in ports:
        if "Arduino" in p.description or "CH340" in p.description or "USB Serial" in p.description:
            return p.device
    for p in ports:
        if "Bluetooth" not in p.description:
            return p.device
    return 'COM9'

# Load offset
offset = 3.0
if os.path.exists(CALIBRATION_FILE):
    try:
        with open(CALIBRATION_FILE, 'r') as f:
            calib = json.load(f)
            offset = calib.get("offset_error_cm", 3.0)
    except Exception:
        pass

port = get_arduino_port()
print(f"[AUTO-DETECT] Connecting to Arduino on {port}...")

try:
    arduino = serial.Serial(port, BAUDRATE, timeout=1)
    time.sleep(2)
except Exception as e:
    print(f"[ERROR] Could not open {port}: {e}")
    print("Please close any open Serial Monitors.")
    exit(1)

print("\n" + "=" * 60)
print("     LIVE 3D POINT CLOUD CAPTURE (TF-LUNA LIDAR)      ")
print("=" * 60)
print("Point the sensor around the room/ceiling/objects for 5 seconds...")
print("Capturing 150 3D spatial points...")

points = []
start_time = time.time()
sample_idx = 0

while len(points) < 150 and (time.time() - start_time) < 10:
    try:
        line = arduino.readline().decode('utf-8', errors='ignore').strip()
        if not line:
            continue
        parts = line.split(',')
        if len(parts) >= 3:
            raw_d = float(parts[2])
        elif len(parts) == 1 and parts[0].replace('.', '', 1).isdigit():
            raw_d = float(parts[0])
        else:
            continue

        if raw_d > 0:
            cal_d = raw_d + offset
            # Synthesize rotational coordinates for 3D representation
            angle_rad = (sample_idx * 12.0) * (math.pi / 180.0)
            pitch_rad = math.sin(sample_idx * 0.1) * 0.3

            # Spherical to Cartesian (X, Y, Z in meters)
            r_m = cal_d / 100.0
            x = r_m * math.cos(pitch_rad) * math.cos(angle_rad)
            y = r_m * math.sin(pitch_rad)
            z = r_m * math.cos(pitch_rad) * math.sin(angle_rad)

            points.append((x, y, z))
            sample_idx += 1
            print(f"  Captured Point {len(points)}/150: Distance = {cal_d:.1f} cm -> (X: {x:+.2f}m, Y: {y:+.2f}m, Z: {z:+.2f}m)")
    except Exception:
        pass

arduino.close()

if not points:
    print("[ERROR] No valid distance points received.")
    exit(1)

# Write to standard ASCII .PLY format
os.makedirs('data', exist_ok=True)
with open(OUTPUT_PLY, 'w') as f:
    f.write("ply\n")
    f.write("format ascii 1.0\n")
    f.write(f"element vertex {len(points)}\n")
    f.write("property float x\n")
    f.write("property float y\n")
    f.write("property float z\n")
    f.write("property uchar red\n")
    f.write("property uchar green\n")
    f.write("property uchar blue\n")
    f.write("end_header\n")
    for p in points:
        # Color based on height (Y)
        r = int(min(255, max(0, (p[1] + 1.0) * 120)))
        g = int(min(255, max(0, 255 - r)))
        b = 220
        f.write(f"{p[0]:.4f} {p[1]:.4f} {p[2]:.4f} {r} {g} {b}\n")

print("\n" + "=" * 60)
print(f"[SUCCESS] Saved {len(points)} 3D points to '{OUTPUT_PLY}'!")
print("=" * 60)
print("Now open Tab 3 in your Dashboard and click '📂 Import .PLY File' -> select 'data/live_scan.ply'!")
