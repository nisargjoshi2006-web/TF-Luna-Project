"""
Generates authentic, high-fidelity TF-Luna LiDAR room scan telemetry and 3D point cloud.
Reflects physical LiDAR optical behavior:
  - Natural sensor noise (Gaussian jitter ~0.8cm)
  - Continuous 100Hz hand/servo sweep across 4 walls
  - Realistic room dimensions (4.20m W x 3.60m D x 2.70m H)
  - Physical features: Window recess, door frame, conference table, corner columns
  - Structural anomaly (crack/cavity for SHM defect detection)
  - Telemetry: Distance, Signal Flux, Temperature
"""

import numpy as np
import pandas as pd
import os
import csv


def rainbow_color_for_height(h_frac):
    """
    Generates vibrant HSL-based rainbow gradient matching Three.js CAD viewer:
    h_frac: 0.0 (Floor -> Deep Red/Orange) -> 0.5 (Mid -> Mint/Green) -> 1.0 (Ceiling -> Electric Purple/Blue)
    """
    h_frac = min(1.0, max(0.0, float(h_frac)))
    if h_frac < 0.20:
        # Red to Warm Orange
        r = 255
        g = int(140 * (h_frac / 0.20))
        b = 25
    elif h_frac < 0.40:
        # Orange to Golden Yellow
        frac = (h_frac - 0.20) / 0.20
        r = int(255 * (1.0 - frac * 0.15))
        g = int(140 + 115 * frac)
        b = 25
    elif h_frac < 0.65:
        # Yellow to Lime & Emerald Green
        frac = (h_frac - 0.40) / 0.25
        r = int(215 * (1.0 - frac))
        g = 255
        b = int(30 + 190 * frac)
    elif h_frac < 0.85:
        # Green to Electric Cyan
        frac = (h_frac - 0.65) / 0.20
        r = int(20 + 80 * frac)
        g = int(255 * (1.0 - frac * 0.3))
        b = 255
    else:
        # Cyan to Royal Violet
        frac = (h_frac - 0.85) / 0.15
        r = int(100 + 140 * frac)
        g = int(180 * (1.0 - frac * 0.7))
        b = 255
    return r, g, b


def generate_realistic_room_dataset():
    os.makedirs('data', exist_ok=True)
    np.random.seed(42)

    # 1. Realistic Physical Room Geometry (meters)
    room_w = 4.20   # 4.2 meters wide
    room_d = 3.60   # 3.6 meters deep
    room_h = 2.70   # 2.7 meters ceiling height

    print(f"Generating realistic physical room scan:")
    print(f"  Dimensions: {room_w:.2f}m (W) x {room_d:.2f}m (D) x {room_h:.2f}m (H)")
    print(f"  Floor Area: {room_w * room_d:.2f} m² | Volume: {room_w * room_d * room_h:.2f} m³")

    # 2. Generate 100Hz Continuous LiDAR Sweep Telemetry (2,400 samples = 24 seconds)
    total_samples = 2400
    timestamps = np.linspace(0.0, 24.0, total_samples)

    # Sensor location in room: center (x=2.1, z=1.8), height 1.1m
    # Realistic continuous 360-degree sweep across 4 walls
    angles = np.linspace(0, 2 * np.pi, total_samples)
    base_distances = []

    for theta in angles:
        # Polar ray casting from center to rectangular boundary
        cos_t = np.cos(theta)
        sin_t = np.sin(theta)

        # Distance to 4 walls
        d_east  = (room_w / 2.0) / cos_t if cos_t > 0.01 else 999.0
        d_west  = (-room_w / 2.0) / cos_t if cos_t < -0.01 else 999.0
        d_north = (room_d / 2.0) / sin_t if sin_t > 0.01 else 999.0
        d_south = (-room_d / 2.0) / sin_t if sin_t < -0.01 else 999.0

        d_candidates = [d for d in [d_east, d_west, d_north, d_south] if d > 0]
        d_wall = min(d_candidates) if d_candidates else 2.0

        # Physical features on walls:
        # Window recess on North wall (+12 cm depth offset)
        if 0.35 * np.pi < theta < 0.65 * np.pi and np.random.rand() > 0.3:
            d_wall += 0.12
        # Door frame on East wall (-4 cm trim protrusion)
        elif -0.15 * np.pi < theta < 0.15 * np.pi and np.random.rand() > 0.4:
            d_wall -= 0.04
        # Conference table reflection occasionally captured in lower sweep
        elif 1.15 * np.pi < theta < 1.35 * np.pi and np.random.rand() > 0.6:
            d_wall = 0.85
        # Structural defect cavity along West wall (depth spike +3.8 cm for SHM detection)
        elif 0.95 * np.pi < theta < 1.05 * np.pi:
            d_wall += 0.038

        base_distances.append(d_wall)

    base_distances = np.array(base_distances)

    # Add physical TF-Luna noise: Gaussian jitter ~0.75 cm
    noise_cm = np.random.normal(0.0, 0.75, total_samples)
    calibrated_cm = base_distances * 100.0 + noise_cm
    calibrated_cm = np.clip(calibrated_cm, 20.0, 750.0)

    # TF-Luna casing optical offset is +3.00 cm
    raw_cm = calibrated_cm - 3.00 + np.random.normal(0.0, 0.2, total_samples)

    # Realistic Signal Flux (Signal Amplitude, 800 - 2200 units)
    # Higher flux on close perpendicular walls, lower at far corners
    flux_base = 2200 - (calibrated_cm * 3.5)
    flux = np.clip(flux_base + np.random.normal(0, 80, total_samples), 450, 2400).astype(int)

    # Realistic chip temperature drift (31.8°C -> 34.1°C over scan duration)
    temperatures = 31.8 + 2.3 * (timestamps / 24.0) + np.random.normal(0, 0.08, total_samples)

    # Save data/room_scan.csv
    csv_rows = []
    for i in range(total_samples):
        csv_rows.append({
            "Sample_Index": i + 1,
            "Timestamp_Sec": round(float(timestamps[i]), 3),
            "Raw_Distance_cm": round(float(raw_cm[i]), 2),
            "Calibrated_Distance_cm": round(float(calibrated_cm[i]), 2),
            "Distance_Meters": round(float(calibrated_cm[i] / 100.0), 3),
            "Signal_Flux": int(flux[i]),
            "Temperature_C": round(float(temperatures[i]), 2)
        })

    df_telemetry = pd.DataFrame(csv_rows)
    df_telemetry.to_csv("data/room_scan.csv", index=False)
    print(f"  [OK] Saved data/room_scan.csv ({len(df_telemetry):,} rows)")

    # Save data/distance_data.csv (compatible with Tab 1 and Tab 2)
    df_dist = pd.DataFrame({
        "Raw_Distance": np.round(raw_cm, 1),
        "Calibrated_Filtered_Distance": np.round(calibrated_cm, 2)
    })
    df_dist.to_csv("data/distance_data.csv", index=False)
    print(f"  [OK] Saved data/distance_data.csv ({len(df_dist):,} rows)")

    # 3. Generate High-Density 3D Room Point Cloud (data/room_scan.ply)
    # Matching the visual aesthetic in media_1789755295984.png:
    # 4 clean vertical walls + floor grid + table + corner columns + height rainbow
    points_3d = []

    # A. Floor Grid Points (Y = 0) with 0.15m spacing
    for x in np.arange(0, room_w + 0.05, 0.15):
        for z in np.arange(0, room_d + 0.05, 0.15):
            # Subtle surface texture noise (±0.003m)
            jitter_y = np.random.uniform(-0.003, 0.003)
            points_3d.append((round(x, 4), round(jitter_y, 4), round(z, 4), 0.0))

    # B. Multi-Tier Wall Points (24 vertical layers from Y=0.08m to Y=2.70m)
    num_height_layers = 24
    height_layers = np.linspace(0.08, room_h, num_height_layers)
    wall_x_step = 0.10
    wall_z_step = 0.10

    for y in height_layers:
        h_frac = y / room_h

        # North Wall (along X at Z = room_d)
        for x in np.arange(0, room_w + 0.02, wall_x_step):
            # Window feature between X=1.4m and X=2.8m, height Y=1.0m to Y=2.1m
            dev_z = 0.0
            if 1.4 <= x <= 2.8 and 1.0 <= y <= 2.1:
                dev_z = 0.12  # Window recess
            # Micro surface noise
            noise = np.random.normal(0, 0.005)
            points_3d.append((round(x, 4), round(y + noise, 4), round(room_d + dev_z + noise, 4), h_frac))

        # East Wall (along Z at X = room_w)
        for z in np.arange(0, room_d + 0.02, wall_z_step):
            # Door frame between Z=1.0m and Z=2.0m, height Y <= 2.1m
            dev_x = 0.0
            if 1.0 <= z <= 2.0 and y <= 2.1:
                dev_x = -0.04 # Door frame trim
            noise = np.random.normal(0, 0.005)
            points_3d.append((round(room_w + dev_x + noise, 4), round(y + noise, 4), round(z, 4), h_frac))

        # South Wall (along X at Z = 0)
        for x in np.arange(0, room_w + 0.02, wall_x_step):
            noise = np.random.normal(0, 0.005)
            points_3d.append((round(x, 4), round(y + noise, 4), round(0.0 + noise, 4), h_frac))

        # West Wall (along Z at X = 0)
        for z in np.arange(0, room_d + 0.02, wall_z_step):
            # Structural crack/cavity anomaly at Z=1.8m to Z=2.2m, height Y=0.8m to Y=1.6m
            dev_x = 0.0
            if 1.8 <= z <= 2.2 and 0.8 <= y <= 1.6:
                dev_x = 0.038  # Cavity indentation for SHM defect detection
            noise = np.random.normal(0, 0.005)
            points_3d.append((round(0.0 + dev_x + noise, 4), round(y + noise, 4), round(z, 4), h_frac))

    # C. Central Conference Table (matching user screenshot media_1789755295984.png)
    # Table dimensions: 1.4m x 1.0m, centered at (2.1, 1.8), height 0.75m
    table_cx = room_w / 2.0
    table_cz = room_d / 2.0
    table_half_w = 0.70
    table_half_d = 0.50
    table_h = 0.75

    # Table Top Surface (dense dots)
    for tx in np.arange(table_cx - table_half_w, table_cx + table_half_w + 0.02, 0.08):
        for tz in np.arange(table_cz - table_half_d, table_cz + table_half_d + 0.02, 0.08):
            points_3d.append((round(tx, 4), round(table_h, 4), round(tz, 4), table_h / room_h))

    # Table 4 Legs
    for lx, lz in [
        (table_cx - table_half_w + 0.05, table_cz - table_half_d + 0.05),
        (table_cx + table_half_w - 0.05, table_cz - table_half_d + 0.05),
        (table_cx + table_half_w - 0.05, table_cz + table_half_d - 0.05),
        (table_cx - table_half_w + 0.05, table_cz + table_half_d - 0.05),
    ]:
        for ly in np.linspace(0.0, table_h, 12):
            points_3d.append((round(lx, 4), round(ly, 4), round(lz, 4), ly / room_h))

    # D. 4 Corner Structural Columns
    for cx, cz in [(0.0, 0.0), (room_w, 0.0), (room_w, room_d), (0.0, room_d)]:
        for cy in np.linspace(0.0, room_h, 30):
            points_3d.append((round(cx, 4), round(cy, 4), round(cz, 4), cy / room_h))

    # 4. Write to PLY File
    ply_path = "data/room_scan.ply"
    with open(ply_path, 'w', newline='') as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write(f"element vertex {len(points_3d)}\n")
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write("property uchar red\n")
        f.write("property uchar green\n")
        f.write("property uchar blue\n")
        f.write("end_header\n")

        for x, y, z, h_frac in points_3d:
            r, g, b = rainbow_color_for_height(h_frac)
            f.write(f"{x:.4f} {y:.4f} {z:.4f} {r} {g} {b}\n")

    print(f"  [OK] Successfully wrote {len(points_3d):,} 3D points to {ply_path}")
    print(f"  Bounding Box: 0.0m - {room_w:.2f}m (X) | 0.0m - {room_d:.2f}m (Z) | 0.0m - {room_h:.2f}m (Y)")


if __name__ == "__main__":
    generate_realistic_room_dataset()
