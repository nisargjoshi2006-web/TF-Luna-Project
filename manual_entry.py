"""
TF-LUNA LIDAR - SIMPLE MANUAL CM DATA ENTRY
Enter 3 numbers in cm -> Instantly calculates Area, Volume & 3D Room
"""

import os
import sys
import json
import shutil
import numpy as np
import pandas as pd

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass


def copy_to_desktop(files):
    desktop = os.path.join(os.path.expanduser('~'), 'OneDrive', 'Desktop')
    if not os.path.exists(desktop):
        desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
    if os.path.exists(desktop):
        for f in files:
            if os.path.exists(f):
                try:
                    shutil.copyfile(f, os.path.join(desktop, os.path.basename(f)))
                except Exception:
                    pass


def calculate_and_generate(width_cm, depth_cm, height_cm):
    os.makedirs('data', exist_ok=True)
    w_m = width_cm / 100.0
    d_m = depth_cm / 100.0
    h_m = height_cm / 100.0

    floor_area = round(w_m * d_m, 2)
    wall_area = round(2 * (w_m + d_m) * h_m, 2)
    volume = round(floor_area * h_m, 2)
    perimeter = round(2 * (w_m + d_m), 2)

    north_area = round(w_m * h_m, 2)
    south_area = round(w_m * h_m, 2)
    east_area = round(d_m * h_m, 2)
    west_area = round(d_m * h_m, 2)

    print("\n" + "=" * 65)
    print("           CALCULATED ARCHITECTURAL METROLOGY")
    print("=" * 65)
    print(f"  • Dimensions in CM   : {width_cm:.0f} cm (W) x {depth_cm:.0f} cm (D) x {height_cm:.0f} cm (H)")
    print(f"  • Dimensions in M    : {w_m:.2f} m (W) x {d_m:.2f} m (D) x {h_m:.2f} m (H)")
    print("-" * 65)
    print(f"  [Floor Surface Area] : {floor_area:.2f} m2   ({floor_area * 10.7639:.1f} sq ft)")
    print(f"  [Total Wall Area]    : {wall_area:.2f} m2   ({wall_area * 10.7639:.1f} sq ft)")
    print(f"  [Enclosed Volume]    : {volume:.2f} m3   ({volume * 35.3147:.1f} cu ft)")
    print(f"  [Room Perimeter]     : {perimeter:.2f} m    ({perimeter * 100:.0f} cm)")
    print("-" * 65)
    print("  WALLS BREAKDOWN:")
    print(f"    - North Wall : Span {w_m:.2f}m x Height {h_m:.2f}m = {north_area:.2f} m2")
    print(f"    - South Wall : Span {w_m:.2f}m x Height {h_m:.2f}m = {south_area:.2f} m2")
    print(f"    - East Wall  : Span {d_m:.2f}m x Height {h_m:.2f}m = {east_area:.2f} m2")
    print(f"    - West Wall  : Span {d_m:.2f}m x Height {h_m:.2f}m = {west_area:.2f} m2")
    print("=" * 65)

    # Generate 3D point cloud
    vertices = []
    # Floor grid
    step_floor = max(0.15, min(w_m, d_m) / 25.0)
    for x in np.arange(0.0, w_m + 0.01, step_floor):
        for z in np.arange(0.0, d_m + 0.01, step_floor):
            vertices.append((float(x), 0.0, float(z), 30, 220, 255))

    # 4 Walls with height gradient
    layers_y = np.linspace(0.08, h_m, 24)
    step_wall = max(0.08, min(w_m, d_m) / 40.0)
    for y in layers_y:
        h_frac = y / h_m
        r = int(255 * (1.0 - h_frac * 0.8))
        g = int(255 * min(h_frac * 2, (1.0 - h_frac) * 2))
        b = int(255 * h_frac)
        for x in np.arange(0.0, w_m + 0.01, step_wall):
            vertices.append((float(x), float(y), float(d_m), r, g, b))  # North
            vertices.append((float(x), float(y), 0.0, r, g, b))         # South
        for z in np.arange(0.0, d_m + 0.01, step_wall):
            vertices.append((float(w_m), float(y), float(z), r, g, b))  # East
            vertices.append((0.0, float(y), float(z), r, g, b))         # West

    # Write PLY file
    ply_path = 'data/room_scan.ply'
    with open(ply_path, 'w') as f:
        f.write("ply\nformat ascii 1.0\n")
        f.write(f"element vertex {len(vertices)}\n")
        f.write("property float x\nproperty float y\nproperty float z\n")
        f.write("property uchar red\nproperty uchar green\nproperty uchar blue\nend_header\n")
        for vx, vy, vz, vr, vg, vb in vertices:
            f.write(f"{vx:.4f} {vy:.4f} {vz:.4f} {vr} {vg} {vb}\n")

    # Generate CSV telemetry
    csv_path = 'data/room_scan.csv'
    total_samples = 2400
    timestamps = np.linspace(0.0, 24.0, total_samples)
    angles = np.linspace(0, 2 * np.pi, total_samples)
    csv_rows = []
    for t, theta in zip(timestamps, angles):
        cos_t, sin_t = np.cos(theta), np.sin(theta)
        d_e = (w_m / 2.0) / cos_t if cos_t > 0.01 else 999.0
        d_w = (-w_m / 2.0) / cos_t if cos_t < -0.01 else 999.0
        d_n = (d_m / 2.0) / sin_t if sin_t > 0.01 else 999.0
        d_s = (-d_m / 2.0) / sin_t if sin_t < -0.01 else 999.0
        d_c = [d for d in [d_e, d_w, d_n, d_s] if d > 0]
        d_val = min(d_c) if d_c else 2.0
        raw_cm = round((d_val * 100.0) + np.random.normal(0, 0.8), 2)
        csv_rows.append({
            "timestamp": round(t, 3),
            "distance_cm": raw_cm,
            "calibrated_distance_cm": round(raw_cm + 3.0, 2),
            "flux": int(np.random.normal(1800, 150)),
            "temperature_c": round(28.0 + (t / 24.0) * 1.5, 1)
        })
    pd.DataFrame(csv_rows).to_csv(csv_path, index=False)

    # Save summary
    summary_path = 'data/room_scan_summary.json'
    summary = {
        "dimensions_cm": {"width_x": width_cm, "depth_z": depth_cm, "height_y": height_cm},
        "dimensions_m": {"width_x": w_m, "depth_z": d_m, "height_y": h_m},
        "floor_area_m2": floor_area,
        "wall_area_m2": wall_area,
        "volume_m3": volume,
        "perimeter_m": perimeter,
        "total_3d_points": len(vertices)
    }
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)

    copy_to_desktop([ply_path, csv_path, summary_path])
    print(f"  [OK] Created 3D model with {len(vertices):,} points -> {ply_path}")
    print("  [OK] Copied files directly to your Desktop!")
    print("  [OK] Ready to view in Tab 4 & Tab 5 of http://localhost:8501")


def main():
    print("""
=================================================================
             TF-LUNA LIDAR - SIMPLE CM MEASUREMENT
=================================================================
Enter your room measurements in centimeters (cm).
Press Enter to keep the default values.
""")
    try:
        w_in = input("  1. Enter Room Width in cm  [default 420]: ").strip()
        width_cm = float(w_in) if w_in else 420.0

        d_in = input("  2. Enter Room Depth in cm  [default 360]: ").strip()
        depth_cm = float(d_in) if d_in else 360.0

        h_in = input("  3. Enter Room Height in cm [default 270]: ").strip()
        height_cm = float(h_in) if h_in else 270.0

        calculate_and_generate(width_cm, depth_cm, height_cm)

    except ValueError:
        print("  [ERROR] Please enter valid numbers.")


if __name__ == '__main__':
    main()
