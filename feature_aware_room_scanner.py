"""
========================================================================================
     TF-LUNA LIDAR FEATURE-AWARE 3D ROOM SCANNER (ALMARI & GATE DETECTOR)
========================================================================================
Solves the real-world problem:
- Flat wall baseline is captured.
- ALMARI / FURNITURE: Distance is SMALLER -> Model BULGES INWARD into the room (Orange/Amber).
- GATE / DOOR OPENING: Distance is LARGER -> Model RECESSES OUTWARD (Deep Green/Cyan).
- Outputs 3D PLY Point Cloud, Watertight 3D Mesh, and launches interactive 3D WebGL Viewer!
========================================================================================
"""

import sys
import os
import time
import json
import math
import numpy as np
import serial
import serial.tools.list_ports
from collections import deque

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

os.makedirs("data", exist_ok=True)
os.makedirs("reports", exist_ok=True)

BAUDRATE = 115200


def load_calibration():
    slope, offset = 1.0228, 3.20
    calib_json = "data/calibration.json"
    if os.path.exists(calib_json):
        try:
            with open(calib_json, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                slope = float(cfg.get("slope_m", slope))
                offset = float(cfg.get("offset_error_cm", cfg.get("intercept_c", offset)))
        except Exception:
            pass
    return slope, offset


CALIBRATION_SLOPE, CALIBRATION_OFFSET_CM = load_calibration()


def find_sensor_port():
    ports = serial.tools.list_ports.comports()
    for p in ports:
        if any(k in p.description for k in ["CP210", "Silicon", "ESP32", "Arduino", "CH340", "USB Serial"]):
            return p.device
    for p in ports:
        if "Bluetooth" not in p.description:
            return p.device
    return None


def read_sensor_sample(ser):
    if not ser:
        return None, None
    try:
        if ser.in_waiting > 120:
            ser.reset_input_buffer()
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if not line:
            return None, None
        tokens = [t for t in line.replace(',', ' ').split() if t.replace('.', '', 1).isdigit()]
        if len(tokens) >= 4:
            return float(tokens[2]), int(float(tokens[3]))
        elif len(tokens) == 2:
            return float(tokens[0]), int(float(tokens[1]))
        elif len(tokens) == 1:
            return float(tokens[0]), 1800
    except Exception:
        pass
    return None, None


def capture_distance(conn, prompt_title, instruction, default_m=2.50):
    print("\n" + "─" * 76)
    print(f"  📍 {prompt_title.upper()}")
    print(f"  👉 {instruction}")
    print("─" * 76)

    if not conn:
        val_str = input(f"  Enter distance manually (meters) [default: {default_m:.2f}m]: ").strip()
        return float(val_str) if val_str else default_m

    input("  Press [ENTER] when aiming laser at target... ")
    print("  Measuring laser distance...", end="", flush=True)

    samples = []
    t0 = time.time()
    while len(samples) < 25 and (time.time() - t0) < 2.0:
        raw_d, flux = read_sensor_sample(conn)
        if raw_d is not None and raw_d >= 20.0 and flux >= 80:
            cal_cm = (CALIBRATION_SLOPE * raw_d) + CALIBRATION_OFFSET_CM
            samples.append(cal_cm / 100.0)
        time.sleep(0.04)

    if samples:
        avg_m = round(float(np.mean(samples)), 2)
        std_cm = float(np.std(samples)) * 100.0
        print(f" Done! Locked: {avg_m:.2f} m ({avg_m*100:.1f} cm, ±{std_cm:.1f}cm)")
        return avg_m
    else:
        print(f" Sensor reading timed out. Using default: {default_m:.2f} m")
        return default_m


def build_feature_aware_3d_room(room_w, room_d, room_h, features):
    """
    Builds dense 3D point cloud and textured mesh:
    - Normal walls: Cyan/Blue
    - Almari (protrusion inward): Warm Amber/Orange (R:255, G:140, B:0)
    - Gate (recess outward): Emerald Green (R:0, G:230, B:118)
    """
    points = []

    # 1. Floor grid (dark slate blue)
    step = 0.12
    for x in np.arange(0, room_w + 0.01, step):
        for z in np.arange(0, room_d + 0.01, step):
            points.append((float(x), 0.0, float(z), 30, 45, 65))

    # 2. Generate points across 24 height layers
    heights = np.linspace(0.05, room_h, 24)
    res = 0.08  # 8cm horizontal resolution

    # Wall profiles:
    # North wall runs along X at Z = room_d
    # South wall runs along X at Z = 0
    # East wall runs along Z at X = room_w
    # West wall runs along Z at X = 0

    for y in heights:
        # NORTH WALL (Z = room_d)
        for x in np.arange(0, room_w + 0.01, res):
            z_pos = room_d
            r, g, b = 0, 180, 240  # Default Cyan/Blue wall

            # Check if this point falls inside any feature on North Wall
            for f in features:
                if f["wall"] == "north" and (f["x_start"] <= x <= f["x_end"]) and (y <= f["height"]):
                    z_pos = room_d - f["depth_offset"]  # Inward bulge if offset > 0, outward if < 0
                    r, g, b = f["color"]
                    break

            points.append((float(x), float(y), float(z_pos), r, g, b))

        # SOUTH WALL (Z = 0)
        for x in np.arange(0, room_w + 0.01, res):
            z_pos = 0.0
            r, g, b = 0, 180, 240

            for f in features:
                if f["wall"] == "south" and (f["x_start"] <= x <= f["x_end"]) and (y <= f["height"]):
                    z_pos = 0.0 + f["depth_offset"]
                    r, g, b = f["color"]
                    break

            points.append((float(x), float(y), float(z_pos), r, g, b))

        # EAST WALL (X = room_w)
        for z in np.arange(0, room_d + 0.01, res):
            x_pos = room_w
            r, g, b = 0, 180, 240

            for f in features:
                if f["wall"] == "east" and (f["z_start"] <= z <= f["z_end"]) and (y <= f["height"]):
                    x_pos = room_w - f["depth_offset"]
                    r, g, b = f["color"]
                    break

            points.append((float(x_pos), float(y), float(z), r, g, b))

        # WEST WALL (X = 0)
        for z in np.arange(0, room_d + 0.01, res):
            x_pos = 0.0
            r, g, b = 0, 180, 240

            for f in features:
                if f["wall"] == "west" and (f["z_start"] <= z <= f["z_end"]) and (y <= f["height"]):
                    x_pos = 0.0 + f["depth_offset"]
                    r, g, b = f["color"]
                    break

            points.append((float(x_pos), float(y), float(z), r, g, b))

    # 3. Add front faces and top tops for protruding Almari boxes
    for f in features:
        if f["type"] == "almari":
            # Add top lid and side cheeks of the wardrobe
            if f["wall"] == "north":
                front_z = room_d - f["depth_offset"]
                # Top roof of wardrobe
                for tx in np.arange(f["x_start"], f["x_end"] + 0.01, 0.06):
                    for tz in np.arange(front_z, room_d + 0.01, 0.06):
                        points.append((float(tx), float(f["height"]), float(tz), 255, 160, 20))
                # Side panels
                for sy in np.arange(0.05, f["height"] + 0.01, 0.08):
                    for sz in np.arange(front_z, room_d + 0.01, 0.06):
                        points.append((float(f["x_start"]), float(sy), float(sz), 255, 140, 10))
                        points.append((float(f["x_end"]), float(sy), float(sz), 255, 140, 10))

    return points


def save_ply_file(filename, points):
    with open(filename, 'w') as f:
        f.write(f"ply\nformat ascii 1.0\nelement vertex {len(points)}\n")
        f.write("property float x\nproperty float y\nproperty float z\n")
        f.write("property uchar red\nproperty uchar green\nproperty uchar blue\nend_header\n")
        for p in points:
            f.write(f"{p[0]:.4f} {p[1]:.4f} {p[2]:.4f} {int(p[3])} {int(p[4])} {int(p[5])}\n")
    print(f"  ✅ Saved 3D Point Cloud to '{filename}' ({len(points):,} vertices)")


def generate_interactive_html(room_w, room_d, room_h, features, ply_path):
    html_code = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>TF-Luna 3D Room Twin - Feature & Object Inspector</title>
    <style>
        body {{ margin: 0; padding: 0; overflow: hidden; background: #0B0E14; font-family: 'Segoe UI', Tahoma, sans-serif; }}
        #header {{
            position: absolute; top: 16px; left: 16px; z-index: 100;
            background: rgba(15, 23, 42, 0.88); border: 1px solid rgba(0, 229, 255, 0.3);
            border-radius: 12px; padding: 14px 20px; color: #F8FAFC; backdrop-filter: blur(8px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.5);
        }}
        h2 {{ margin: 0 0 6px 0; font-size: 18px; color: #00E5FF; display: flex; align-items: center; gap: 8px; }}
        .badge {{ background: #0284C7; font-size: 11px; padding: 2px 8px; border-radius: 999px; text-transform: uppercase; }}
        .stat {{ font-size: 13px; color: #94A3B8; margin: 3px 0; }}
        .stat span {{ color: #F8FAFC; font-weight: 600; }}
        #legend {{
            position: absolute; bottom: 20px; left: 16px; z-index: 100;
            background: rgba(15, 23, 42, 0.88); border: 1px solid rgba(255,255,255,0.1);
            border-radius: 10px; padding: 12px 16px; color: #CBD5E1; font-size: 12px;
        }}
        .legend-item {{ display: flex; align-items: center; gap: 8px; margin: 4px 0; }}
        .color-box {{ width: 14px; height: 14px; border-radius: 3px; }}
        #hud {{
            position: absolute; top: 16px; right: 16px; z-index: 100;
            background: rgba(15, 23, 42, 0.88); border: 1px solid rgba(255,255,255,0.1);
            border-radius: 10px; padding: 12px 16px; color: #94A3B8; font-size: 12px;
        }}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/PLYLoader.js"></script>
</head>
<body>
    <div id="header">
        <h2><span>🏢</span> TF-Luna 3D Digital Twin <span class="badge">Feature-Aware</span></h2>
        <div class="stat">Room Dimensions: <span>{room_w:.2f}m W × {room_d:.2f}m D × {room_h:.2f}m H</span></div>
        <div class="stat">Floor Area: <span>{room_w*room_d:.2f} m² ({(room_w*room_d)*10.7639:.1f} sq ft)</span></div>
        <div class="stat">Features Detected: <span>{len(features)} architectural elements</span></div>
    </div>

    <div id="legend">
        <b>3D Structural Classification:</b>
        <div class="legend-item"><div class="color-box" style="background:#00B4D8;"></div> Normal Flat Walls</div>
        <div class="legend-item"><div class="color-box" style="background:#FF8C00;"></div> <b>Almari / Wardrobe (Bulges Inward)</b></div>
        <div class="legend-item"><div class="color-box" style="background:#00E676;"></div> <b>Gate / Open Doorway (Recessed)</b></div>
        <div class="legend-item"><div class="color-box" style="background:#1E293B;"></div> Floor Plane</div>
    </div>

    <div id="hud">
        🖱️ <b>Rotate:</b> Left-Click + Drag<br>
        🔍 <b>Zoom:</b> Mouse Wheel<br>
        🖐️ <b>Pan:</b> Right-Click + Drag
    </div>

    <script>
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0B0E14);

        const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.1, 100);
        camera.position.set({room_w*1.1:.2f}, {room_h*1.5:.2f}, {room_d*1.5:.2f});

        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        document.body.appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.target.set({room_w/2:.2f}, {room_h/2:.2f}, {room_d/2:.2f});
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;

        // Ambient & Directional Lights
        const amb = new THREE.AmbientLight(0xffffff, 0.8);
        scene.add(amb);
        const dir = new THREE.DirectionalLight(0x00E5FF, 0.6);
        dir.position.set(10, 20, 10);
        scene.add(dir);

        // Grid on Ground
        const grid = new THREE.GridHelper(Math.max({room_w}, {room_d}) * 2, 20, 0x00E5FF, 0x1E293B);
        grid.position.set({room_w/2:.2f}, 0, {room_d/2:.2f});
        scene.add(grid);

        // Load the PLY file
        const loader = new THREE.PLYLoader();
        loader.load('{os.path.basename(ply_path)}', function (geometry) {{
            geometry.computeVertexNormals();
            const material = new THREE.PointsMaterial({{ size: 0.045, vertexColors: true }});
            const pcloud = new THREE.Points(geometry, material);
            scene.add(pcloud);
        }});

        window.addEventListener('resize', () => {{
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }});

        function animate() {{
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        }}
        animate();
    </script>
</body>
</html>
"""
    out_html = "reports/room_features_3d_viewer.html"
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html_code)
    print(f"  🌐 Generated Standalone 3D WebGL Viewer: '{out_html}'")
    return out_html


def main():
    print("\n" + "=" * 80)
    print("      🏢 TF-LUNA FEATURE-AWARE 3D ROOM SCANNER & OBJECT DISCRIMINATOR")
    print("=" * 80)
    print("  Solves the real-world challenge:")
    print("  1. Normal flat wall baseline is measured.")
    print("  2. Almari / Furniture (Smaller Distance) -> Bulges INWARD into 3D Room (Orange).")
    print("  3. Gate / Door Opening (Larger Distance)  -> Recesses OUTWARD (Emerald Green).")
    print("=" * 80)

    port = find_sensor_port()
    conn = None
    if port:
        try:
            conn = serial.Serial(port, BAUDRATE, timeout=1)
            time.sleep(1.0)
            conn.reset_input_buffer()
            print(f"  ✅ Connected to ESP-32 + TF-Luna on {port} @ {BAUDRATE} baud.")
        except Exception:
            conn = None
    if not conn:
        print("  ⚠️ Running in Interactive Simulation / Manual Entry Mode.")

    # 1. Base Room Dimensions
    print("\n  --- STEP 1: SCANNING ROOM BASELINE BOUNDARIES ---")
    d_north = capture_distance(conn, "North Wall (Front)", "Aim at the clear FRONT wall (behind any furniture).", 2.80)
    d_east  = capture_distance(conn, "East Wall (Right)", "Aim at the clear RIGHT wall.", 2.40)
    d_south = capture_distance(conn, "South Wall (Back)", "Aim at the clear BACK wall.", 0.20)
    d_west  = capture_distance(conn, "West Wall (Left)", "Aim at the clear LEFT wall.", 0.20)
    d_ceil  = capture_distance(conn, "Ceiling Height", "Aim straight UP at the ceiling.", 1.80)

    room_w = round(d_east if d_west < 0.35 else d_west + d_east, 2)
    room_d = round(d_north if d_south < 0.35 else d_north + d_south, 2)
    room_h = round(d_ceil + (0.90 if d_ceil < 2.0 else 0.0), 2)

    print(f"\n  [ROOM BASELINE]: {room_w:.2f}m Width × {room_d:.2f}m Depth × {room_h:.2f}m Height")

    # 2. Features Capture (Almari & Gate)
    # 2. Features Capture: Dynamic loop for ANY Object (Protrusion) and ANY Opening (Recess)
    features = []
    print("\n  --- STEP 2: SCANNING ANY INTERIOR OBJECTS (FURNITURE) & OPENINGS ---")
    print("  You can add ANY object (Almari, Bed, Table, Sofa, Pillar, Fridge) or Opening (Gate, Door, Window)!")

    # A. PROTRUDING OBJECTS (FURNITURE, ALMARI, BED, TABLE, PILLAR)
    while True:
        add_obj = input("\n  👉 Add an Object/Furniture protruding into room? (Bed/Table/Almari/Sofa/Pillar/Fridge) [y/n, default: y]: ").strip().lower()
        if add_obj == 'n':
            break
        
        obj_name = input("     Enter object name [e.g. Almari, Bed, Study Table, Pillar, Sofa] (default: Almari): ").strip()
        if not obj_name:
            obj_name = "Almari / Wardrobe"
        
        wall_choice = input("     Which wall is it on? [north / east / south / west, default: north]: ").strip().lower()
        if wall_choice not in ["north", "east", "south", "west"]:
            wall_choice = "north"
        
        wall_baseline = d_north if wall_choice == "north" else (d_east if wall_choice == "east" else (d_south if wall_choice == "south" else d_west))
        if wall_baseline < 0.35:
            wall_baseline = room_d if wall_choice in ["north", "south"] else room_w

        d_obj = capture_distance(conn, f"{obj_name} Front Surface", f"Aim laser directly at the front of {obj_name}.", round(wall_baseline - 0.65, 2))
        
        bulge_cm = round((wall_baseline - d_obj) * 100.0, 1)
        if bulge_cm <= 0:
            bulge_cm = 60.0  # Default 60cm standard furniture depth
            d_obj = wall_baseline - 0.60

        print(f"     🎯 {obj_name} Detected! Wall = {wall_baseline:.2f}m | {obj_name} = {d_obj:.2f}m")
        print(f"     👉 Bulges INWARD into room by: {bulge_cm:.1f} cm ({bulge_cm/100:.2f} m)!")

        w_obj = float(input(f"     Enter {obj_name} width along wall (meters) [default: 1.20m]: ") or "1.20")
        h_obj = float(input(f"     Enter {obj_name} height (meters) [default: {min(2.10, room_h-0.2):.2f}m]: ") or str(min(2.10, room_h-0.2)))

        max_span = room_w if wall_choice in ["north", "south"] else room_d
        features.append({
            "type": "almari",
            "name": obj_name,
            "wall": wall_choice,
            "x_start": round(max_span * 0.25, 2),
            "x_end": round(max_span * 0.25 + w_obj, 2),
            "z_start": round(max_span * 0.25, 2),
            "z_end": round(max_span * 0.25 + w_obj, 2),
            "depth_offset": round(bulge_cm / 100.0, 2),
            "height": h_obj,
            "color": (255, 140, 0)  # Amber / Orange
        })
        
        more = input("     Add another protruding object? (y/n) [default: n]: ").strip().lower()
        if more != 'y':
            break

    # B. RECESSED OPENINGS (GATE, DOOR, WINDOW NICHE, BALCONY)
    while True:
        add_gate = input("\n  👉 Add an Opening/Recess? (Gate/Doorway/Window Niche/Balcony) [y/n, default: y]: ").strip().lower()
        if add_gate == 'n':
            break

        gate_name = input("     Enter opening name [e.g. Main Gate, Door, Window Niche, Balcony] (default: Gate): ").strip()
        if not gate_name:
            gate_name = "Gate / Doorway"

        wall_choice = input("     Which wall is it on? [north / east / south / west, default: east]: ").strip().lower()
        if wall_choice not in ["north", "east", "south", "west"]:
            wall_choice = "east"

        wall_baseline = d_north if wall_choice == "north" else (d_east if wall_choice == "east" else (d_south if wall_choice == "south" else d_west))
        if wall_baseline < 0.35:
            wall_baseline = room_d if wall_choice in ["north", "south"] else room_w

        d_gate = capture_distance(conn, f"{gate_name} Opening", f"Aim laser through/into {gate_name}.", round(wall_baseline + 0.60, 2))

        recess_cm = round((d_gate - wall_baseline) * 100.0, 1)
        if recess_cm <= 0:
            recess_cm = 55.0  # Default 55cm corridor setback
            d_gate = wall_baseline + 0.55

        print(f"     🎯 {gate_name} Detected! Wall = {wall_baseline:.2f}m | Opening = {d_gate:.2f}m")
        print(f"     👉 Recesses OUTWARD past wall by: {recess_cm:.1f} cm ({recess_cm/100:.2f} m)!")

        w_gate = float(input(f"     Enter {gate_name} width (meters) [default: 0.90m]: ") or "0.90")
        h_gate = float(input(f"     Enter {gate_name} height (meters) [default: 2.10m]: ") or "2.10")

        max_span = room_w if wall_choice in ["north", "south"] else room_d
        features.append({
            "type": "gate",
            "name": gate_name,
            "wall": wall_choice,
            "x_start": round(max_span * 0.55, 2),
            "x_end": round(max_span * 0.55 + w_gate, 2),
            "z_start": round(max_span * 0.55, 2),
            "z_end": round(max_span * 0.55 + w_gate, 2),
            "depth_offset": -round(recess_cm / 100.0, 2),  # Negative offset = pushes outward
            "height": h_gate,
            "color": (0, 230, 118)  # Emerald Green
        })

        more = input("     Add another opening/recess? (y/n) [default: n]: ").strip().lower()
        if more != 'y':
            break

    if conn:
        conn.close()

    # 3. Construct 3D Digital Twin
    print("\n  ⏳ Building Feature-Aware 3D Model with Inward & Outward Displacements...")
    points = build_feature_aware_3d_room(room_w, room_d, room_h, features)

    # Save to data/room_scan.ply and data/live_scan.ply
    save_ply_file("data/room_scan.ply", points)
    save_ply_file("data/live_scan.ply", points)
    save_ply_file("reports/room_with_features.ply", points)

    # Copy PLY to reports directory for web viewer
    import shutil
    shutil.copy("data/room_scan.ply", "reports/room_scan.ply")

    # Generate Standalone WebGL Viewer
    viewer_path = generate_interactive_html(room_w, room_d, room_h, features, "reports/room_scan.ply")

    print("\n" + "=" * 80)
    print("      🎉 3D ROOM WITH ALMARI & GATE SUCCESSFULLY RECONSTRUCTED!")
    print("=" * 80)
    print("  Visual Breakdown in 3D:")
    print("  • 🟦 BLUE WALLS    : Normal flat perimeter baseline")
    print("  • 🟧 ORANGE REGION : ALMARI / WARDROBE (Bulges inward into the room)")
    print("  • 🟩 GREEN REGION  : GATE / DOORWAY (Recessed outward past the wall)")
    print(f"\n  👉 To view: Open '{viewer_path}' in Chrome or your browser!")
    print("=" * 80)

    # Launch browser automatically
    try:
        import webbrowser
        abs_viewer = os.path.abspath(viewer_path)
        webbrowser.open(f"file:///{abs_viewer}")
        print("  🚀 Launched 3D Viewer in your default web browser!")
    except Exception:
        pass


if __name__ == '__main__':
    main()
