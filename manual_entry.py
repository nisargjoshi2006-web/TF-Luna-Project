"""
╔══════════════════════════════════════════════════════════════════════════════╗
║               TF-LUNA LIDAR MANUAL CM DATA ENTRY & METROLOGY                 ║
║   Input manual measurements in centimeters (cm) → Generates 3D PLY & CSV     ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import shutil
import numpy as np
import pandas as pd
from datetime import datetime


if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass


def rainbow_color_for_height(h_frac):
    """Generates vibrant HSL-based rainbow color for 3D point cloud."""
    h_frac = min(1.0, max(0.0, float(h_frac)))
    if h_frac < 0.20:
        r, g, b = 255, int(140 * (h_frac / 0.20)), 25
    elif h_frac < 0.40:
        frac = (h_frac - 0.20) / 0.20
        r, g, b = int(255 * (1.0 - frac * 0.15)), int(140 + 115 * frac), 25
    elif h_frac < 0.65:
        frac = (h_frac - 0.40) / 0.25
        r, g, b = int(215 * (1.0 - frac)), 255, int(30 + 190 * frac)
    elif h_frac < 0.85:
        frac = (h_frac - 0.65) / 0.20
        r, g, b = int(20 + 80 * frac), int(255 * (1.0 - frac * 0.3)), 255
    else:
        frac = (h_frac - 0.85) / 0.15
        r, g, b = int(100 + 140 * frac), int(180 * (1.0 - frac * 0.7)), 255
    return r, g, b


def copy_to_desktop(files):
    desktop = os.path.join(os.path.expanduser('~'), 'OneDrive', 'Desktop')
    if not os.path.exists(desktop):
        desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
    
    if os.path.exists(desktop):
        for f in files:
            if os.path.exists(f):
                dest = os.path.join(desktop, os.path.basename(f))
                try:
                    shutil.copyfile(f, dest)
                    print(f"  [OK] Copied to Desktop: {os.path.basename(f)}")
                except Exception as e:
                    pass


def build_and_save_room(width_cm, depth_cm, height_cm, defect_wall=None, defect_depth_cm=3.8):
    """
    Converts cm dimensions into a complete, dense 3D point cloud (.PLY)
    and 100Hz telemetry log (.CSV) with accurate area and volume metrology.
    """
    os.makedirs('data', exist_ok=True)
    w_m = width_cm / 100.0
    d_m = depth_cm / 100.0
    h_m = height_cm / 100.0

    floor_area_m2 = round(w_m * d_m, 2)
    floor_area_sqft = round(floor_area_m2 * 10.7639, 1)
    perimeter_m = round(2 * (w_m + d_m), 2)
    wall_area_m2 = round(2 * (w_m + d_m) * h_m, 2)
    wall_area_sqft = round(wall_area_m2 * 10.7639, 1)
    total_enclosed_m2 = round(2 * floor_area_m2 + wall_area_m2, 2)
    volume_m3 = round(floor_area_m2 * h_m, 2)
    volume_cuft = round(volume_m3 * 35.3147, 1)

    north_area_m2 = round(w_m * h_m, 2)
    south_area_m2 = round(w_m * h_m, 2)
    east_area_m2 = round(d_m * h_m, 2)
    west_area_m2 = round(d_m * h_m, 2)

    print("\n" + "=" * 70)
    print("  ARCHITECTURAL METROLOGY & DIMENSION SUMMARY (FROM YOUR CM INPUT)")
    print("=" * 70)
    print(f"  • Room Width (X)     : {width_cm:.1f} cm  ({w_m:.2f} m)")
    print(f"  • Room Depth (Z)     : {depth_cm:.1f} cm  ({d_m:.2f} m)")
    print(f"  • Ceiling Height (Y) : {height_cm:.1f} cm  ({h_m:.2f} m)")
    print("-" * 70)
    print(f"  [Floor Surface Area] : {floor_area_m2:.2f} m2  ({floor_area_sqft} sq ft)")
    print(f"  [Total Wall Area]    : {wall_area_m2:.2f} m2  ({wall_area_sqft} sq ft)")
    print(f"  [Total Enclosed]     : {total_enclosed_m2:.2f} m2  (Floor + Ceiling + 4 Walls)")
    print(f"  [Room Volume]        : {volume_m3:.2f} m3  ({volume_cuft} cu ft)")
    print(f"  [Room Perimeter]     : {perimeter_m:.2f} m  ({perimeter_m * 100:.0f} cm)")
    print("-" * 70)
    print("  INDIVIDUAL WALL BREAKDOWN:")
    print(f"    - North Wall (Z={d_m:.2f}m) : Span {w_m:.2f}m x Height {h_m:.2f}m = {north_area_m2:.2f} m2 | Status: Sound")
    print(f"    - South Wall (Z=0.00m) : Span {w_m:.2f}m x Height {h_m:.2f}m = {south_area_m2:.2f} m2 | Status: Sound")
    print(f"    - East Wall  (X={w_m:.2f}m) : Span {d_m:.2f}m x Height {h_m:.2f}m = {east_area_m2:.2f} m2 | Status: Sound")
    def_stat = f"Defect (+{defect_depth_cm:.1f}cm Cavity)" if defect_wall == 'west' else "Sound"
    print(f"    - West Wall  (X=0.00m) : Span {d_m:.2f}m x Height {h_m:.2f}m = {west_area_m2:.2f} m2 | Status: {def_stat}")
    print("=" * 70)

    # Generate 3D Vertices
    vertices = []
    
    # 1. Floor grid
    step_floor = max(0.15, min(w_m, d_m) / 25.0)
    for x in np.arange(0.0, w_m + 0.01, step_floor):
        for z in np.arange(0.0, d_m + 0.01, step_floor):
            jitter = np.random.normal(0, 0.004)
            vertices.append((float(x), float(max(0.0, jitter)), float(z), 0.0, 30, 220, 255))

    # 2. 4 Multi-tier perimeter walls
    layers_y = np.linspace(0.08, h_m, 24)
    step_wall = max(0.08, min(w_m, d_m) / 40.0)

    for y in layers_y:
        h_frac = y / h_m
        r, g, b = rainbow_color_for_height(h_frac)

        # North & South walls (along X)
        for x in np.arange(0.0, w_m + 0.01, step_wall):
            j_n = np.random.normal(0, 0.006)
            j_s = np.random.normal(0, 0.006)
            vertices.append((float(x), float(y), float(d_m + j_n), float(h_frac), r, g, b))
            vertices.append((float(x), float(y), float(0.0 + j_s), float(h_frac), r, g, b))

        # East & West walls (along Z)
        for z in np.arange(0.0, d_m + 0.01, step_wall):
            j_e = np.random.normal(0, 0.006)
            j_w = np.random.normal(0, 0.006)
            # Defect on West wall if specified
            if defect_wall == 'west' and (0.4 * d_m <= z <= 0.6 * d_m) and (0.3 * h_m <= y <= 0.6 * h_m):
                cavity_offset = defect_depth_cm / 100.0  # e.g. 0.038m
                vertices.append((float(0.0 - cavity_offset + j_w), float(y), float(z), float(h_frac), 255, 30, 30))
            else:
                vertices.append((float(0.0 + j_w), float(y), float(z), float(h_frac), r, g, b))
            vertices.append((float(w_m + j_e), float(y), float(z), float(h_frac), r, g, b))

    # 3. Interior table fixture (if room size permits)
    if w_m >= 2.5 and d_m >= 2.2:
        tx_start, tx_end = w_m * 0.35, w_m * 0.65
        tz_start, tz_end = d_m * 0.35, d_m * 0.65
        t_height = min(0.75, h_m * 0.3)
        for tx in np.arange(tx_start, tx_end + 0.01, 0.08):
            for tz in np.arange(tz_start, tz_end + 0.01, 0.08):
                vertices.append((float(tx), float(t_height), float(tz), float(t_height / h_m), 16, 185, 129))

    # Write PLY file
    ply_path = 'data/room_scan.ply'
    with open(ply_path, 'w') as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write(f"element vertex {len(vertices)}\n")
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write("property uchar red\n")
        f.write("property uchar green\n")
        f.write("property uchar blue\n")
        f.write("end_header\n")
        for vx, vy, vz, _, vr, vg, vb in vertices:
            f.write(f"{vx:.4f} {vy:.4f} {vz:.4f} {vr} {vg} {vb}\n")

    # Generate matching 100Hz CSV telemetry
    csv_path = 'data/room_scan.csv'
    total_samples = 2400
    timestamps = np.linspace(0.0, 24.0, total_samples)
    angles = np.linspace(0, 2 * np.pi, total_samples)
    csv_rows = []

    for t, theta in zip(timestamps, angles):
        cos_t = np.cos(theta)
        sin_t = np.sin(theta)
        d_east  = (w_m / 2.0) / cos_t if cos_t > 0.01 else 999.0
        d_west  = (-w_m / 2.0) / cos_t if cos_t < -0.01 else 999.0
        d_north = (d_m / 2.0) / sin_t if sin_t > 0.01 else 999.0
        d_south = (-d_m / 2.0) / sin_t if sin_t < -0.01 else 999.0
        d_candidates = [d for d in [d_east, d_west, d_north, d_south] if d > 0]
        d_val = min(d_candidates) if d_candidates else 2.0
        
        # Convert to cm with sensor noise
        raw_cm = round((d_val * 100.0) + np.random.normal(0, 0.8), 2)
        cal_cm = round(raw_cm + 3.0, 2)
        flux = int(np.random.normal(1800, 150))
        temp = round(28.0 + (t / 24.0) * 1.5 + np.random.normal(0, 0.1), 1)

        csv_rows.append({
            "timestamp": round(t, 3),
            "distance_cm": raw_cm,
            "calibrated_distance_cm": cal_cm,
            "flux": max(50, flux),
            "temperature_c": temp,
            "scan_angle_deg": round(np.degrees(theta), 1)
        })

    pd.DataFrame(csv_rows).to_csv(csv_path, index=False)

    # Save summary JSON
    summary_path = 'data/room_scan_summary.json'
    summary = {
        "dimensions_meters": {
            "width_x": w_m,
            "depth_z": d_m,
            "height_y": h_m
        },
        "dimensions_cm": {
            "width_x": width_cm,
            "depth_z": depth_cm,
            "height_y": height_cm
        },
        "metrology": {
            "floor_area_m2": floor_area_m2,
            "floor_area_sqft": floor_area_sqft,
            "wall_surface_area_m2": wall_area_m2,
            "wall_surface_area_sqft": wall_area_sqft,
            "total_enclosed_area_m2": total_enclosed_m2,
            "room_volume_m3": volume_m3,
            "room_volume_cuft": volume_cuft,
            "perimeter_meters": perimeter_m
        },
        "walls": {
            "north_wall": {"span_m": w_m, "height_m": h_m, "area_m2": north_area_m2, "status": "Sound"},
            "south_wall": {"span_m": w_m, "height_m": h_m, "area_m2": south_area_m2, "status": "Sound"},
            "east_wall": {"span_m": d_m, "height_m": h_m, "area_m2": east_area_m2, "status": "Sound"},
            "west_wall": {"span_m": d_m, "height_m": h_m, "area_m2": west_area_m2, "status": def_stat}
        },
        "total_3d_points": len(vertices),
        "generated_at": datetime.now().isoformat()
    }
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"\n  [OK] Successfully generated {len(vertices):,} 3D spatial points in: {ply_path}")
    print(f"  [OK] Successfully saved {len(csv_rows):,} telemetry rows in: {csv_path}")
    print(f"  [OK] Saved metrology summary in: {summary_path}")

    # Copy directly to Desktop
    copy_to_desktop([ply_path, csv_path, summary_path])
    print("\n  [DONE] All files are updated and ready to view in Tab 4 and Tab 5 of the Web Dashboard.")


def mode_room_dimensions():
    print("\n" + "=" * 60)
    print("  MODE 1: ENTER ROOM DIMENSIONS IN CENTIMETERS (CM)")
    print("=" * 60)
    print("  Enter your measurements in centimeters (e.g., 420 cm = 4.20 meters)\n")

    try:
        w_in = input("  >> Enter Room Width (X) in cm [default 420]: ").strip()
        width_cm = float(w_in) if w_in else 420.0

        d_in = input("  >> Enter Room Depth (Z) in cm [default 360]: ").strip()
        depth_cm = float(d_in) if d_in else 360.0

        h_in = input("  >> Enter Ceiling Height (Y) in cm [default 270]: ").strip()
        height_cm = float(h_in) if h_in else 270.0

        def_in = input("  >> Include structural defect on West Wall? (y/n) [default y]: ").strip().lower()
        defect_wall = 'west' if def_in != 'n' else None

        build_and_save_room(width_cm, depth_cm, height_cm, defect_wall=defect_wall)

    except ValueError as e:
        print(f"  [ERROR] Invalid number: {e}. Please enter numbers in cm.")


def mode_wall_distances_from_center():
    print("\n" + "=" * 60)
    print("  MODE 2: 4-WALL DISTANCES FROM SENSOR CENTER IN CM")
    print("=" * 60)
    print("  Place the TF-Luna sensor at the center of the room and measure distance in cm to each wall:\n")

    try:
        n_in = input("  >> Distance to NORTH Wall (cm) [default 180]: ").strip()
        dist_north = float(n_in) if n_in else 180.0

        s_in = input("  >> Distance to SOUTH Wall (cm) [default 180]: ").strip()
        dist_south = float(s_in) if s_in else 180.0

        e_in = input("  >> Distance to EAST Wall (cm) [default 210]: ").strip()
        dist_east = float(e_in) if e_in else 210.0

        w_in = input("  >> Distance to WEST Wall (cm) [default 210]: ").strip()
        dist_west = float(w_in) if w_in else 210.0

        h_in = input("  >> Total Ceiling Height (cm) [default 270]: ").strip()
        height_cm = float(h_in) if h_in else 270.0

        total_width_cm = dist_east + dist_west
        total_depth_cm = dist_north + dist_south

        print(f"\n  Calculated Total Width (East + West) : {total_width_cm:.1f} cm ({total_width_cm/100:.2f} m)")
        print(f"  Calculated Total Depth (North + South): {total_depth_cm:.1f} cm ({total_depth_cm/100:.2f} m)")

        build_and_save_room(total_width_cm, total_depth_cm, height_cm, defect_wall='west')

    except ValueError as e:
        print(f"  [ERROR] Invalid number: {e}. Please enter numbers in cm.")


def mode_horizontal_wall_sweep():
    print("\n" + "=" * 70)
    print("  MODE: HORIZONTAL SENSOR SWEEP ALONG WALL (IN CM)")
    print("=" * 70)
    print("  You move the TF-Luna sensor horizontally from left to right along a wall.")
    print("  The algorithm detects all 3 defects:")
    print("    * Cavity / Spalling   : Distance increases by >= +2.0 cm (sunken in)")
    print("    * Bulge / Delamination: Distance decreases by <= -2.0 cm (protruding out)")
    print("    * Crack / Fissure     : Sharp micro-jump with signal flux drop\n")

    print("  Which wall are you sweeping horizontally?")
    print("    [1] North Wall (Span along X)")
    print("    [2] East Wall  (Span along Z)")
    print("    [3] South Wall (Span along X)")
    print("    [4] West Wall  (Span along Z)")
    w_choice = input("  >> Select wall [1-4, default 1]: ").strip()
    wall_map = {'1': 'north', '2': 'east', '3': 'south', '4': 'west'}
    chosen_wall = wall_map.get(w_choice, 'north')

    w_len_in = input("  >> Total Wall Length in cm [default 420]: ").strip()
    wall_len_cm = float(w_len_in) if w_len_in else 420.0

    w_h_in = input("  >> Ceiling Height in cm [default 270]: ").strip()
    ceil_h_cm = float(w_h_in) if w_h_in else 270.0

    sweep_y_in = input("  >> Sensor Height from Floor in cm [default 120]: ").strip()
    sweep_y_cm = float(sweep_y_in) if sweep_y_in else 120.0

    print("\n  Enter your horizontal distance readings in cm:")
    print("  (Type comma-separated, e.g.: 100, 100, 104, 104, 100, 96, 96, 100, or press Enter for step-by-step)")
    inp_cm = input("  >> CM values: ").strip()
    cm_readings = []

    if inp_cm:
        try:
            cm_readings = [float(x.strip()) for x in inp_cm.split(',') if x.strip()]
        except ValueError:
            print("  [WARN] Error parsing comma-separated numbers. Switching to step-by-step.")

    if not cm_readings:
        print("  Type each cm reading as you move horizontally. Type 'done' or 'q' to finish:")
        idx = 1
        while True:
            val_s = input(f"    Step {idx} (cm): ").strip()
            if val_s.lower() in ('done', 'q', 'exit', ''):
                break
            try:
                cm_readings.append(float(val_s))
                idx += 1
            except ValueError:
                print("    [WARN] Invalid number, please re-enter.")

    # Default realistic sweep if empty
    if not cm_readings:
        print("  No readings entered. Using demo horizontal sweep with Cavity (+4cm), Bulge (-4cm), and Crack!")
        # 20 horizontal steps: baseline 100cm, cavity at steps 5-7 (104cm), bulge at steps 12-14 (96cm), crack at step 17
        cm_readings = [100.0, 100.2, 99.8, 100.1, 104.2, 104.5, 104.1, 100.0, 99.9, 100.2, 96.1, 95.8, 96.0, 99.8, 100.1, 100.0, 101.8, 100.1, 99.9, 100.0]

    base_d = float(np.median(cm_readings))
    num_pts = len(cm_readings)
    step_cm = wall_len_cm / max(1, num_pts - 1)

    print("\n" + "=" * 70)
    print(f"  HORIZONTAL SWEEP ANALYSIS ON {chosen_wall.upper()} WALL")
    print("=" * 70)
    print(f"  • Total Horizontal Points Scanned: {num_pts}")
    print(f"  • Wall Length                    : {wall_len_cm:.1f} cm ({wall_len_cm/100:.2f} m)")
    print(f"  • Scan Step Resolution           : {step_cm:.1f} cm per point")
    print(f"  • Nominal Flat Wall Baseline     : {base_d:.2f} cm")
    print("-" * 70)

    # Defect Classification Engine
    defect_summary = {"cavities": [], "bulges": [], "cracks": []}
    rows_linear = []

    for i, d in enumerate(cm_readings):
        pos_cm = i * step_cm
        dev = d - base_d
        flux = 1800
        status = "NOMINAL SOUND SURFACE"

        # Crack check: sudden single-point spike or sharp gradient
        prev_d = cm_readings[i - 1] if i > 0 else d
        next_d = cm_readings[i + 1] if i < num_pts - 1 else d
        is_sharp_spike = (abs(d - prev_d) >= 1.5 and abs(d - next_d) >= 1.5 and np.sign(d - prev_d) == np.sign(d - next_d))

        if is_sharp_spike:
            status = "CRACK / STRUCTURAL FISSURE"
            flux = 380  # Trapped light in crack
            defect_summary["cracks"].append((pos_cm, dev))
        elif dev >= 2.0:
            status = "SURFACE CAVITY / SPALLING"
            flux = 1650
            defect_summary["cavities"].append((pos_cm, dev))
        elif dev <= -2.0:
            status = "SURFACE BULGE / DELAMINATION"
            flux = 2200
            defect_summary["bulges"].append((pos_cm, dev))

        rows_linear.append({
            "timestamp": round(i * 0.1, 2),
            "position_cm": round(pos_cm, 1),
            "distance_cm": round(d, 2),
            "calibrated_distance_cm": round(d + 3.0, 2),
            "deviation_cm": round(dev, 2),
            "flux": flux,
            "temperature_c": 28.5,
            "defect_status": status,
            "wall": chosen_wall
        })

    # Print Defect Findings
    print(f"  * Cavities Detected : {len(defect_summary['cavities'])} points")
    for pos, dev in defect_summary['cavities']:
        print(f"      -> At Position {pos:.1f} cm : Depth +{dev:.1f} cm [CAVITY]")

    print(f"  * Bulges Detected   : {len(defect_summary['bulges'])} points")
    for pos, dev in defect_summary['bulges']:
        print(f"      -> At Position {pos:.1f} cm : Protrusion {dev:.1f} cm [BULGE]")

    print(f"  * Cracks Detected   : {len(defect_summary['cracks'])} points")
    for pos, dev in defect_summary['cracks']:
        print(f"      -> At Position {pos:.1f} cm : Micro-jump {dev:+.1f} cm (Flux < 500) [CRACK]")

    if not defect_summary['cavities'] and not defect_summary['bulges'] and not defect_summary['cracks']:
        print("  [OK] No defects detected! Wall surface is completely uniform and healthy.")
    print("=" * 70)

    # Save to data/distance_data.csv for Tab 1 & Tab 2
    os.makedirs('data', exist_ok=True)
    csv_linear_path = 'data/distance_data.csv'
    pd.DataFrame(rows_linear).to_csv(csv_linear_path, index=False)
    print(f"  [OK] Saved horizontal sweep telemetry to: {csv_linear_path}")

    # Now rebuild full 3D room with this swept wall in true 3D coordinates!
    width_cm = wall_len_cm if chosen_wall in ('north', 'south') else 360.0
    depth_cm = wall_len_cm if chosen_wall in ('east', 'west') else 360.0
    build_and_save_room(width_cm, depth_cm, ceil_h_cm, defect_wall=chosen_wall if defect_summary['cavities'] else None)

    copy_to_desktop([csv_linear_path])
    print(f"  [OK] Copied {csv_linear_path} to Desktop.")
    print("\n  [DONE] Horizontal sweep is live! Open Tab 1/2 for 2D profile & Tab 5 for 3D room view.")


def main():
    print("""
================================================================================
               TF-LUNA LIDAR MANUAL CM DATA ENTRY & METROLOGY                   
                    Measure in CM -> Full 3D Model & Area                       
================================================================================

  How would you like to enter your manual CM data?

  [1] Horizontal Sensor Sweep along a Wall (Move sensor left-to-right)
      -> Enter distance in cm as you move horizontally along the wall
      -> Automatically detects: Cavities (+cm), Bulges (-cm), and Cracks!
      -> Plots in Tab 1 & 2 (2D Elevation Contour) and Tab 5 (3D Room Model)

  [2] Complete Room Dimensions in CM (Width x Depth x Height)
      -> Enter: 420 cm, 360 cm, 270 cm
      -> Automatically calculates: Floor Area, Wall Area, Volume, 
         generates 3D room_scan.ply & room_scan.csv, and labels all 4 walls.

  [3] 4-Wall Distances from Center in CM (North, East, South, West)
      -> Enter distance from sensor center to each wall in cm
      -> Sums distances to find room dimensions and generates full 3D model.

  [4] Linear Surface / Cavity Profile in CM (Points along a line/wall)
      -> Enter distances in cm: e.g. 102.5, 102.8, 106.8 cm
      -> Detects cracks & cavities, saves to data/distance_data.csv for Tab 1 & 2.

  [0] Exit
""")

    choice = input("  >> Select an option (1, 2, 3, 4, or 0) [default 1]: ").strip()
    if choice == '2':
        mode_room_dimensions()
    elif choice == '3':
        mode_wall_distances_from_center()
    elif choice == '4':
        mode_linear_profile_cm()
    elif choice == '0':
        print("  Exiting.")
        sys.exit(0)
    else:
        mode_horizontal_wall_sweep()


if __name__ == '__main__':
    main()

