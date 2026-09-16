"""
╔══════════════════════════════════════════════════════════════╗
║        TF-LUNA 3D ROOM SURFACE SCANNER                      ║
║  Drag sensor along all 4 walls → Full 3D Room Model         ║
╚══════════════════════════════════════════════════════════════╝

How it works:
  1. You enter approximate room dimensions (width × depth in meters)
  2. For each of the 4 walls, you hold the sensor close to the wall
     and slowly slide it from one corner to the next
  3. The software captures distance readings and maps them into 3D space
  4. All 4 walls are stitched together into a complete 3D room model
  5. Output: data/room_scan.ply (viewable in Dashboard Tab 4)

Usage:
  python data_collection/room_scanner.py
"""

import serial
import serial.tools.list_ports
import json
import time
import os
import threading
import numpy as np

BAUDRATE = 115200
CALIBRATION_FILE = 'data/calibration.json'
OUTPUT_PLY = 'data/room_scan.ply'


def get_arduino_port():
    ports = serial.tools.list_ports.comports()
    for p in ports:
        if "Arduino" in p.description or "CH340" in p.description or "USB Serial" in p.description:
            return p.device
    for p in ports:
        if "Bluetooth" not in p.description:
            return p.device
    return 'COM9'


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


def scan_single_wall(arduino, wall_name, wall_number, offset):
    """Scan a single wall. Returns list of (timestamp, calibrated_distance_cm)."""
    print(f"\n{'=' * 60}")
    print(f"  WALL {wall_number}/4: {wall_name}")
    print(f"{'=' * 60}")
    print(f"  1. Hold the sensor ~10-30 cm from the wall surface")
    print(f"  2. Point the sensor PERPENDICULAR to the wall")
    print(f"  3. Press ENTER to START scanning")
    print(f"  4. SLOWLY slide the sensor from one corner to the other")
    print(f"  5. Press ENTER again to STOP when you reach the end")
    print()
    input(f"  >>> Press ENTER to START scanning {wall_name}... ")
    print(f"\n  🔴 SCANNING... Slide the sensor slowly along the wall.")
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
            if sample_count % 5 == 0:
                print(f"    ⏱ {t:5.1f}s | Distance: {cal_dist:6.1f} cm | Samples: {sample_count}")

    duration = time.time() - start_time
    print(f"\n  ✅ {wall_name} COMPLETE: {len(readings)} points captured in {duration:.1f}s")
    return readings


def generate_room_3d(wall_data, room_width, room_depth, scan_heights=None):
    """
    Convert 4 wall scans into 3D point cloud.
    
    Wall layout (top-down view):
    
        Wall 1 (North)  ← scan direction →
      ┌──────────────────────┐
      │                      │
      │   Wall 4    Wall 2   │
      │   (West)    (East)   │
      │      ↑          ↓    │
      │                      │
      └──────────────────────┘
        Wall 3 (South)  ← scan direction →
    
    Each wall is placed as a plane in 3D space.
    Distance variations create surface texture (defects, features).
    """
    if scan_heights is None:
        scan_heights = [1.0]  # Default: single scan at 1m height

    all_points = []  # (x, y, z, deviation, wall_idx)

    wall_configs = [
        # (name, base_axis, sweep_axis, normal_axis, base_pos, sweep_range, normal_sign)
        # Wall 1 (North): along X-axis, at Z = room_depth
        {"sweep_range": room_width, "get_xyz": lambda frac, dev, y: (frac * room_width, y, room_depth + dev)},
        # Wall 2 (East): along Z-axis (reverse), at X = room_width
        {"sweep_range": room_depth, "get_xyz": lambda frac, dev, y: (room_width + dev, y, (1 - frac) * room_depth)},
        # Wall 3 (South): along X-axis (reverse), at Z = 0
        {"sweep_range": room_width, "get_xyz": lambda frac, dev, y: ((1 - frac) * room_width, y, 0 - dev)},
        # Wall 4 (West): along Z-axis, at X = 0
        {"sweep_range": room_depth, "get_xyz": lambda frac, dev, y: (0 - dev, y, frac * room_depth)},
    ]

    for wall_idx, readings in enumerate(wall_data):
        if not readings or wall_idx >= 4:
            continue

        config = wall_configs[wall_idx]
        distances = [r[1] for r in readings]
        ref_dist = np.median(distances)
        n = len(readings)

        for height in scan_heights:
            for i, (t, dist) in enumerate(readings):
                frac = i / max(n - 1, 1)
                # Surface deviation from flat baseline (meters)
                deviation = (dist - ref_dist) / 100.0
                x, y, z = config["get_xyz"](frac, deviation, height)
                all_points.append((x, y, z, deviation, wall_idx))

    # Add floor corners to ground the model
    corners = [
        (0, 0, 0), (room_width, 0, 0),
        (room_width, 0, room_depth), (0, 0, room_depth)
    ]
    for cx, cy, cz in corners:
        all_points.append((cx, cy, cz, 0, 4))

    # Add corner vertical edges for visual structure
    for cx, cz in [(0, 0), (room_width, 0), (room_width, room_depth), (0, room_depth)]:
        for cy in np.linspace(0, max(scan_heights) + 0.5, 10):
            all_points.append((cx, cy, cz, 0, 5))

    return all_points


def color_for_point(deviation, wall_idx):
    """Color-code points by wall and deviation."""
    wall_colors = [
        (0, 200, 255),   # Wall 1: Cyan
        (255, 107, 53),   # Wall 2: Orange
        (124, 58, 237),   # Wall 3: Purple
        (16, 185, 129),   # Wall 4: Green
        (100, 100, 100),  # Floor corners: Gray
        (200, 200, 200),  # Vertical edges: Light gray
    ]

    base_r, base_g, base_b = wall_colors[min(wall_idx, len(wall_colors) - 1)]

    # Highlight defects in red
    if abs(deviation) > 0.03:  # >3cm deviation = defect
        intensity = min(1.0, abs(deviation) / 0.1)
        base_r = int(base_r * (1 - intensity) + 255 * intensity)
        base_g = int(base_g * (1 - intensity) + 50 * intensity)
        base_b = int(base_b * (1 - intensity) + 50 * intensity)

    return min(255, max(0, base_r)), min(255, max(0, base_g)), min(255, max(0, base_b))


def write_ply(points, output_path):
    """Write points to standard ASCII PLY format."""
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
    print("║          TF-LUNA 3D ROOM SURFACE SCANNER                   ║")
    print("║    Drag sensor along 4 walls → Full 3D Room Model          ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()

    # Get room dimensions
    while True:
        try:
            room_width = float(input("  Enter room WIDTH  (meters, e.g. 4.0): "))
            room_depth = float(input("  Enter room DEPTH  (meters, e.g. 3.0): "))
            if room_width > 0 and room_depth > 0:
                break
            print("  Please enter positive values.")
        except ValueError:
            print("  Invalid input. Enter a number.")

    # Ask for scan mode
    print()
    print("  Scan Modes:")
    print("    [1] Quick Scan  — 1 height pass  (~2 min)")
    print("    [2] Detailed Scan — 3 height passes (~8 min)")
    mode = input("  Select mode [1/2] (default: 1): ").strip()

    if mode == "2":
        scan_heights = [0.3, 1.0, 1.8]  # Knee, chest, head
        print("  → Detailed mode: You'll scan each wall at 3 heights (30cm, 100cm, 180cm)")
    else:
        scan_heights = [1.0]  # Chest height only
        print("  → Quick mode: Scan each wall once at chest height")

    # Connect to Arduino
    offset = load_calibration()
    port = get_arduino_port()
    print(f"\n  [CALIBRATION] Offset: +{offset:.2f} cm")
    print(f"  [AUTO-DETECT] Connecting to Arduino on {port}...")

    try:
        arduino = serial.Serial(port, BAUDRATE, timeout=1)
        time.sleep(2)
        # Clear buffer
        while arduino.in_waiting > 0:
            arduino.read(arduino.in_waiting)
    except Exception as e:
        print(f"\n  [ERROR] Could not open {port}: {e}")
        print("  Make sure Arduino is connected and Serial Monitor is closed.")
        return

    print(f"\n  Room dimensions: {room_width:.1f}m × {room_depth:.1f}m")
    print(f"  Scan heights: {scan_heights}")
    print()

    wall_names = ["North Wall", "East Wall", "South Wall", "West Wall"]
    all_wall_data = []

    # Scan each wall at each height
    for height_idx, height in enumerate(scan_heights):
        if len(scan_heights) > 1:
            print(f"\n{'#' * 60}")
            print(f"  HEIGHT PASS {height_idx + 1}/{len(scan_heights)}: {height:.1f}m ({['Knee', 'Chest', 'Head'][height_idx]} level)")
            print(f"{'#' * 60}")

        height_data = []
        for wall_idx, wall_name in enumerate(wall_names):
            readings = scan_single_wall(arduino, wall_name, wall_idx + 1, offset)
            height_data.append(readings)

        if height_idx == 0:
            all_wall_data = height_data
        else:
            # Merge readings from multiple heights
            for wall_idx in range(4):
                all_wall_data[wall_idx].extend(height_data[wall_idx])

    arduino.close()

    # Generate 3D points
    print(f"\n{'=' * 60}")
    print(f"  GENERATING 3D ROOM MODEL...")
    print(f"{'=' * 60}")

    points_3d = generate_room_3d(all_wall_data, room_width, room_depth, scan_heights)
    write_ply(points_3d, OUTPUT_PLY)

    total_wall_points = sum(len(w) for w in all_wall_data)
    defect_count = sum(1 for p in points_3d if abs(p[3]) > 0.03)

    print(f"\n  ✅ 3D Room Model Generated Successfully!")
    print(f"  ─────────────────────────────────────────")
    print(f"  📐 Room Size:        {room_width:.1f}m × {room_depth:.1f}m")
    print(f"  📊 Total Points:     {len(points_3d)}")
    print(f"  📏 Wall Readings:    {total_wall_points}")
    print(f"  ⚠️  Defects Found:   {defect_count}")
    print(f"  💾 Saved to:         {OUTPUT_PLY}")
    print(f"\n  View your 3D room model:")
    print(f"    streamlit run dashboard/app.py")
    print(f"    → Go to Tab 4 (3D Point Cloud) → Import '{OUTPUT_PLY}'")
    print()


if __name__ == "__main__":
    main()
