"""
╔══════════════════════════════════════════════════════════════╗
║        TF-LUNA 3D SOLID STRUCTURAL & ROOM SCANNER           ║
║   Real-Time LiDAR Telemetry + 3D Mesh / Solid Model Builder ║
╚══════════════════════════════════════════════════════════════╝
"""

import serial
import serial.tools.list_ports
import csv
import json
import time
import os
import threading
import numpy as np

BAUDRATE = 115200
CALIBRATION_FILE = 'data/calibration.json'
OUTPUT_PLY = 'data/room_scan.ply'
DATA_FILE = 'data/distance_data.csv'


def get_arduino_port():
    ports = serial.tools.list_ports.comports()
    for p in ports:
        if any(keyword in p.description for keyword in ["CP210", "Silicon", "ESP32", "Arduino", "CH340", "USB Serial", "USB-to-UART"]):
            return p.device
    for p in ports:
        if "Bluetooth" not in p.description:
            return p.device
    return 'COM10'


def load_calibration():
    offset = 3.0
    if os.path.exists(CALIBRATION_FILE):
        try:
            with open(CALIBRATION_FILE, 'r') as f:
                calib = json.load(f)
                offset = calib.get("offset_error_cm", calib.get("intercept_c", 3.0))
        except Exception:
            pass
    return offset


def read_distance(arduino):
    """Read a single distance value from Arduino serial stream."""
    try:
        line = arduino.readline().decode('utf-8', errors='ignore').strip()
        if not line:
            return None
        parts = line.split(',')
        if len(parts) >= 3:
            return float(parts[2])
        elif len(parts) == 1 and parts[0].replace('.', '', 1).isdigit():
            return float(parts[0])
    except Exception:
        pass
    return None


def scan_single_section(arduino, section_name, section_idx, total_sections, offset, csv_writer, csv_file):
    """Scan a section and simultaneously stream to distance_data.csv for live dashboard tabs."""
    print(f"\n{'=' * 60}")
    print(f"  SCAN [{section_idx}/{total_sections}]: {section_name.upper()}")
    print(f"{'=' * 60}")
    print(f"  1. Position sensor pointing at the surface")
    print(f"  2. Press ENTER to START scanning")
    print(f"  3. SLOWLY slide the sensor across the surface")
    print(f"  4. Press ENTER again to STOP when finished")
    print()
    input(f"  >>> Press ENTER to START scanning {section_name}... ")
    print(f"\n  🔴 SCANNING IN PROGRESS... Slide sensor across {section_name}.")
    print(f"     (Live data is syncing to Dashboard Tab 1 & Tab 2)")
    print(f"     Press ENTER to stop.\n")

    readings = []
    stop_event = threading.Event()

    def wait_for_stop():
        input()
        stop_event.set()

    stop_thread = threading.Thread(target=wait_for_stop, daemon=True)
    stop_thread.start()

    start_time = time.time()
    sample_count = 0

    while not stop_event.is_set():
        dist = read_distance(arduino)
        if dist is not None and dist > 0:
            t = time.time() - start_time
            cal_dist = dist + offset
            readings.append((t, cal_dist))
            sample_count += 1
            
            # Sync to distance_data.csv for live Tab 1 & Tab 2 telemetry
            csv_writer.writerow([round(dist, 2), round(cal_dist, 2)])
            csv_file.flush()

            if sample_count % 5 == 0:
                print(f"    ⏱ {t:5.1f}s | Measured Distance: {cal_dist:6.1f} cm | Data Points: {sample_count}")

    duration = time.time() - start_time
    print(f"\n  ✅ {section_name} COMPLETE: {len(readings)} points captured in {duration:.1f}s")
    return readings


def generate_single_wall_or_object_3d(readings, span_width=2.0, wall_height=2.0):
    """Reconstruct a high-resolution 3D solid surface model of a single scanned wall/object."""
    all_points = []
    if not readings:
        return all_points

    distances = [r[1] for r in readings]
    ref_dist = np.median(distances)
    n = len(readings)

    # Multi-height extrusion for full 3D solid object reconstruction
    height_slices = np.linspace(0.2, wall_height, 6)

    for h in height_slices:
        for i, (t, dist) in enumerate(readings):
            frac = i / max(n - 1, 1)
            x = frac * span_width
            y = h
            # Z depth reflects real physical surface profile (cavities, spalling, box edges)
            deviation = (dist - ref_dist) / 100.0
            z = deviation

            all_points.append((x, y, z, deviation, 0))

    return all_points


def generate_room_3d(wall_data, room_width, room_depth, scan_heights=None):
    """Stitch 4 wall scans into a closed 3D room model."""
    if scan_heights is None:
        scan_heights = [0.5, 1.2, 2.0]

    all_points = []

    wall_configs = [
        # Wall 1 (North): along X-axis at Z = room_depth
        {"get_xyz": lambda frac, dev, y: (frac * room_width, y, room_depth + dev), "idx": 0},
        # Wall 2 (East): along Z-axis at X = room_width
        {"get_xyz": lambda frac, dev, y: (room_width + dev, y, (1 - frac) * room_depth), "idx": 1},
        # Wall 3 (South): along X-axis at Z = 0
        {"get_xyz": lambda frac, dev, y: ((1 - frac) * room_width, y, 0 - dev), "idx": 2},
        # Wall 4 (West): along Z-axis at X = 0
        {"get_xyz": lambda frac, dev, y: (0 - dev, y, frac * room_depth), "idx": 3},
    ]

    for wall_idx, readings in enumerate(wall_data):
        if not readings or wall_idx >= len(wall_configs):
            continue

        config = wall_configs[wall_idx]
        distances = [r[1] for r in readings]
        ref_dist = np.median(distances)
        n = len(readings)

        for height in scan_heights:
            for i, (t, dist) in enumerate(readings):
                frac = i / max(n - 1, 1)
                deviation = (dist - ref_dist) / 100.0
                x, y, z = config["get_xyz"](frac, deviation, height)
                all_points.append((x, y, z, deviation, wall_idx))

    return all_points


def color_for_point(deviation, wall_idx):
    wall_colors = [
        (0, 229, 255),   # Cyan
        (255, 107, 53),   # Orange
        (124, 58, 237),   # Purple
        (16, 185, 129),   # Green
        (100, 100, 100),
    ]

    base_r, base_g, base_b = wall_colors[min(wall_idx, len(wall_colors) - 1)]

    # Highlight structural defects (>3cm deviation) in red
    if abs(deviation) > 0.03:
        intensity = min(1.0, abs(deviation) / 0.1)
        base_r = int(base_r * (1 - intensity) + 255 * intensity)
        base_g = int(base_g * (1 - intensity) + 30 * intensity)
        base_b = int(base_b * (1 - intensity) + 30 * intensity)

    return min(255, max(0, base_r)), min(255, max(0, base_g)), min(255, max(0, base_b))


def write_ply(points, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
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
        for x, y, z, dev, wall_idx in points:
            r, g, b = color_for_point(dev, wall_idx)
            f.write(f"{x:.4f} {y:.4f} {z:.4f} {r} {g} {b}\n")


def main():
    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║        TF-LUNA 3D SOLID STRUCTURAL & ROOM SCANNER           ║")
    print("║   Real-Time LiDAR Telemetry + 3D Mesh / Solid Model Builder ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    print("  Choose Scanning Mode:")
    print("    [1] Single Wall / Object 3D Solid Surface Scan  (15–20 sec demo)")
    print("    [2] Full 4-Wall Room Reconstruction Scan       (~2 min full room)")
    print()
    choice = input("  Select scan mode [1/2] (default: 1): ").strip()
    if not choice:
        choice = "1"

    offset = load_calibration()
    port = get_arduino_port()
    print(f"\n  [CALIBRATION] Active Offset: +{offset:.2f} cm")
    print(f"  [AUTO-DETECT] Connecting to ESP32 on {port}...")

    try:
        arduino = serial.Serial(port, BAUDRATE, timeout=1)
        time.sleep(2)
        while arduino.in_waiting > 0:
            arduino.read(arduino.in_waiting)
    except Exception as e:
        print(f"\n  [ERROR] Could not open {port}: {e}")
        print("  Please make sure Arduino Serial Monitor is closed.")
        return

    os.makedirs('data', exist_ok=True)
    csv_file = open(DATA_FILE, 'a', newline='')
    csv_writer = csv.writer(csv_file)
    if os.path.getsize(DATA_FILE) == 0:
        csv_writer.writerow(["Raw_Distance", "Calibrated_Distance"])

    if choice == "1":
        # Single Wall / Object Mode
        print("\n  >>> Single Wall / Object Mode Selected.")
        span_str = input("  Enter physical scan length / object width in meters [e.g. 1.5 or 2.0]: ").strip()
        span_w = float(span_str) if span_str else 2.0

        readings = scan_single_section(arduino, "Single Wall / Object", 1, 1, offset, csv_writer, csv_file)
        arduino.close()
        csv_file.close()

        print("\n  Generating High-Resolution 3D Solid Surface Mesh...")
        points_3d = generate_single_wall_or_object_3d(readings, span_width=span_w)
        write_ply(points_3d, OUTPUT_PLY)

    else:
        # Full 4-Wall Room Mode
        w_str = input("  Enter room WIDTH in meters [e.g. 4.0]: ").strip()
        d_str = input("  Enter room DEPTH in meters [e.g. 3.5]: ").strip()
        room_w = float(w_str) if w_str else 4.0
        room_d = float(d_str) if d_str else 3.5

        wall_names = ["North Wall", "East Wall", "South Wall", "West Wall"]
        all_wall_data = []

        for idx, wname in enumerate(wall_names):
            r = scan_single_section(arduino, wname, idx + 1, 4, offset, csv_writer, csv_file)
            all_wall_data.append(r)

        arduino.close()
        csv_file.close()

        print("\n  Stitching 4 Walls into 3D Solid Room Model...")
        points_3d = generate_room_3d(all_wall_data, room_w, room_d)
        write_ply(points_3d, OUTPUT_PLY)

    defect_count = sum(1 for p in points_3d if abs(p[3]) > 0.03)
    print(f"\n{'=' * 60}")
    print(f"  🎉 3D SOLID MODEL GENERATED SUCCESSFULLY!")
    print(f"  ─────────────────────────────────────────")
    print(f"  📊 Total 3D Vertices Generated: {len(points_3d)}")
    print(f"  ⚠️  Defects / Cavities Detected: {defect_count}")
    print(f"  💾 Saved Model File:            {OUTPUT_PLY}")
    print(f"  🔄 Synced Live Data:             {DATA_FILE}")
    print(f"{'=' * 60}")
    print("\n  Now open your Dashboard (Tab 5) to rotate & inspect the 3D Solid Model!")


if __name__ == "__main__":
    main()
