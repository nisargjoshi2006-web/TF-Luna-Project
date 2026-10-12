"""
========================================================================================
   TF-LUNA 4-WALL SEQUENTIAL CONTINUOUS ROOM SCANNER (1:1 METRIC 3D DIGITAL TWIN)
========================================================================================
Features:
1. Sequential 4-Wall Continuous Sweep:
   - Wall 1 (North / Front Wall) -> Sweep Left-to-Right -> PAUSE (Wait for user)
   - Wall 2 (East / Right Wall)  -> Sweep Left-to-Right -> PAUSE (Wait for user)
   - Wall 3 (South / Back Wall)  -> Sweep Left-to-Right -> PAUSE (Wait for user)
   - Wall 4 (West / Left Wall)   -> Sweep Left-to-Right -> Finish & Assemble!
2. Continuous laser sampling: captures 300-500 points per wall (1,200+ total).
3. 1:1 Metric Depth Displacements:
   - Baseline plane calculated per wall.
   - 🟧 ORANGE / AMBER : Inward Protrusion (Almari, Bed, Table, Box) - bulges into room by exact cm.
   - 🟩 EMERALD GREEN  : Outward Recess (Gate, Open Door, Niche) - indents outward by exact cm.
   - 🟦 CYAN / BLUE    : Nominal Flat Wall baseline.
4. Clean 3D WebGL Viewer (Labels commented out as requested).
========================================================================================
"""

import sys
import os
import time
import math
import json
import threading
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from mpl_toolkits.mplot3d import Axes3D
import serial
import serial.tools.list_ports

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


def rolling_median(arr, window=5):
    """Filters single-sample sensor flutter and hand jitter."""
    if len(arr) < window:
        return np.array(arr)
    pad = window // 2
    padded = np.pad(arr, pad, mode='edge')
    return np.array([np.median(padded[i:i+window]) for i in range(len(arr))])


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
        if "MOTOR" in line or "Angle" in line or "Pulse" in line:
            if not getattr(read_sensor_sample, '_motor_warned', False):
                print("\n\n" + "!" * 80)
                print("  ❌ [WRONG FIRMWARE RUNNING ON ESP-32]")
                print("     ESP-32 par abhi 'motor_test.ino' (Servo Motor Test) chal raha hai!")
                print("     Laser scanning ke liye 'arduino/tf_luna_code.ino' upload hona zaroori hai.")
                print("     👉 Arduino IDE kholein -> 'arduino/tf_luna_code/tf_luna_code.ino' UPLOAD karein!")
                print("!" * 80 + "\n")
                read_sensor_sample._motor_warned = True
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


def save_ply(filename, points_with_colors):
    with open(filename, 'w') as f:
        f.write(f"ply\nformat ascii 1.0\nelement vertex {len(points_with_colors)}\n")
        f.write("property float x\nproperty float y\nproperty float z\n")
        f.write("property uchar red\nproperty uchar green\nproperty uchar blue\nend_header\n")
        for p in points_with_colors:
            f.write(f"{p[0]:.4f} {p[1]:.4f} {p[2]:.4f} {int(p[3])} {int(p[4])} {int(p[5])}\n")
    print(f"\n  💾 Exported 3D Point Cloud: '{filename}' ({len(points_with_colors):,} vertices)")


def generate_clean_web_viewer(ply_path, meta=None):
    """Generates self-contained 3D viewer with rectangular room dimensions, wall labels and object metrics."""
    with open(ply_path, "r", encoding="utf-8") as f:
        ply_data_str = f.read()

    json_ply = json.dumps(ply_data_str)
    if meta is None:
        meta = {
            'D_N': 2.4, 'D_E': 2.4, 'D_S': 2.4, 'D_W': 2.4,
            'width_x': 4.8, 'length_z': 4.8, 'objects': []
        }
    json_meta = json.dumps(meta)

    html_code = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>3D Room Scan - Rectangular Digital Twin</title>
    <style>
        body {{
            margin: 0; padding: 0; overflow: hidden; background: #07090E;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            user-select: none;
        }}
        #hud {{
            position: absolute; top: 16px; left: 16px; z-index: 100;
            display: flex; align-items: center; gap: 12px;
            background: rgba(15, 23, 42, 0.88); border: 1px solid rgba(0, 229, 255, 0.3);
            border-radius: 10px; padding: 10px 16px; color: #E2E8F0; font-size: 13px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5); backdrop-filter: blur(8px);
        }}
        .toggle-btn {{
            background: #00E5FF; color: #07090E; font-weight: bold;
            border: none; border-radius: 6px; padding: 6px 12px; cursor: pointer;
            transition: all 0.2s ease; font-size: 12px;
        }}
        .toggle-btn:hover {{ background: #38BDF8; }}
        .toggle-btn.off {{ background: #334155; color: #94A3B8; }}
        #legend {{
            position: absolute; bottom: 20px; left: 16px; z-index: 100;
            background: rgba(15, 23, 42, 0.88); border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 8px; padding: 8px 14px; font-size: 12px; color: #94A3B8;
            display: flex; gap: 16px; backdrop-filter: blur(8px);
        }}
        .badge {{ display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 6px; }}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/PLYLoader.js"></script>
</head>
<body>
    <div id="hud">
        <button id="lblBtn" class="toggle-btn" onclick="toggleLabels()">🏷️ Dimension Labels: ON</button>
        <span style="font-weight: 600; color: #00E5FF;">📐 Room: {meta['width_x']}m × {meta['length_z']}m (Rectangular 4-Wall)</span>
        <span style="color: #64748B;">|</span>
        <span style="color: #94A3B8;">🖱️ Rotate: Drag | Zoom: Scroll | Pan: Right-Click</span>
    </div>

    <div id="legend">
        <div><span class="badge" style="background: #00E5FF;"></span>🟦 Normal Wall</div>
        <div><span class="badge" style="background: #FF8C00;"></span>🟧 Almari: Bahar Nikli (Inward Bulge)</div>
        <div><span class="badge" style="background: #00E676;"></span>🟩 Gate: Andar Dhasa (Outward Recess)</div>
    </div>

    <script>
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x07090E);

        const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.05, 100);
        camera.position.set(0, 5.5, 6.8);

        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        document.body.appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.target.set(0, 1.2, 0);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;

        const amb = new THREE.AmbientLight(0xffffff, 1.0);
        scene.add(amb);

        // Ground reference grid
        const grid = new THREE.GridHelper(10, 20, 0x00E5FF, 0x1E293B);
        grid.position.y = 0;
        scene.add(grid);

        // Parse PLY data
        const rawPly = {json_ply};
        const loader = new THREE.PLYLoader();
        const geometry = loader.parse(rawPly);
        geometry.computeVertexNormals();

        const material = new THREE.PointsMaterial({{ size: 0.048, vertexColors: true }});
        const pcloud = new THREE.Points(geometry, material);
        scene.add(pcloud);

        // Room metadata
        const meta = {json_meta};

        // Labels Group (Can be toggled ON/OFF)
        const labelsGroup = new THREE.Group();
        scene.add(labelsGroup);

        // Helper to generate Canvas Text Sprites
        function createTextSprite(text, bgColor, borderColor, textColor, scale = 1.0) {{
            const canvas = document.createElement('canvas');
            canvas.width = 1024;
            canvas.height = 256;
            const ctx = canvas.getContext('2d');

            ctx.fillStyle = bgColor;
            ctx.strokeStyle = borderColor;
            ctx.lineWidth = 6;
            ctx.beginPath();
            const r = 24, w = 1000, h = 232, x = 12, y = 12;
            ctx.moveTo(x + r, y);
            ctx.lineTo(x + w - r, y);
            ctx.quadraticCurveTo(x + w, y, x + w, y + r);
            ctx.lineTo(x + w, y + h - r);
            ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
            ctx.lineTo(x + r, y + h);
            ctx.quadraticCurveTo(x, y + h, x, y + h - r);
            ctx.lineTo(x, y + r);
            ctx.quadraticCurveTo(x, y, x + r, y);
            ctx.closePath();
            ctx.fill();
            ctx.stroke();

            ctx.font = 'bold 46px sans-serif';
            ctx.fillStyle = textColor;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(text, 512, 128);

            const tex = new THREE.CanvasTexture(canvas);
            tex.minFilter = THREE.LinearFilter;
            const mat = new THREE.SpriteMaterial({{ map: tex, depthTest: false }});
            const sprite = new THREE.Sprite(mat);
            sprite.scale.set(1.85 * scale, 0.46 * scale, 1);
            return sprite;
        }}

        // Helper for dimension line with tick brackets (placed safely OUTSIDE room)
        function addDimensionLine(p1, p2, offsetAxis, offsetDist, tickLength = 0.2) {{
            const lineMat = new THREE.LineBasicMaterial({{ color: 0x00E5FF, transparent: true, opacity: 0.85 }});
            const p1_off = p1.clone();
            const p2_off = p2.clone();
            p1_off[offsetAxis] += offsetDist;
            p2_off[offsetAxis] += offsetDist;

            // Main dimension line
            const geom = new THREE.BufferGeometry().setFromPoints([p1_off, p2_off]);
            labelsGroup.add(new THREE.Line(geom, lineMat));

            // Tick marks
            const tickAxis = (offsetAxis === 'z') ? 'x' : 'z';
            const t1_a = p1_off.clone(); t1_a[tickAxis] -= tickLength / 2;
            const t1_b = p1_off.clone(); t1_b[tickAxis] += tickLength / 2;
            labelsGroup.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints([t1_a, t1_b]), lineMat));

            const t2_a = p2_off.clone(); t2_a[tickAxis] -= tickLength / 2;
            const t2_b = p2_off.clone(); t2_b[tickAxis] += tickLength / 2;
            labelsGroup.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints([t2_a, t2_b]), lineMat));

            // Dotted leader lines from room corner to dimension line
            const leadMat = new THREE.LineDashedMaterial({{ color: 0x00E5FF, dashSize: 0.1, gapSize: 0.1, opacity: 0.4, transparent: true }});
            const l1 = new THREE.Line(new THREE.BufferGeometry().setFromPoints([p1, p1_off]), leadMat);
            l1.computeLineDistances();
            labelsGroup.add(l1);

            const l2 = new THREE.Line(new THREE.BufferGeometry().setFromPoints([p2, p2_off]), leadMat);
            l2.computeLineDistances();
            labelsGroup.add(l2);

            return p1_off.clone().lerp(p2_off, 0.5);
        }}

        const D_N = meta.D_N, D_E = meta.D_E, D_S = meta.D_S, D_W = meta.D_W;
        const Y_DIM = 1.35;
        const OUT_OFFSET = 0.65; // Placed 65cm OUTSIDE room so it NEVER meshes with 3D object!

        // Wall 1 (North): Left is (-D_W), Right is (+D_E), at Z = +D_N
        const p1_start = new THREE.Vector3(-D_W, Y_DIM, D_N);
        const p1_end = new THREE.Vector3(D_E, Y_DIM, D_N);
        const mid1 = addDimensionLine(p1_start, p1_end, 'z', OUT_OFFSET);
        const sp1 = createTextSprite(`◄── Wall 1 (North): ${{meta.width_x}} m ──►`, 'rgba(10, 25, 45, 0.90)', '#00E5FF', '#FFFFFF');
        sp1.position.copy(mid1);
        sp1.position.y += 0.35;
        labelsGroup.add(sp1);

        // Wall 1 Corner extent labels
        const sp_nw = createTextSprite(`Wall 1 Start (NW)`, 'rgba(15, 23, 42, 0.85)', '#38BDF8', '#94A3B8', 0.65);
        sp_nw.position.set(-D_W - 0.25, Y_DIM + 0.35, D_N + OUT_OFFSET);
        labelsGroup.add(sp_nw);

        const sp_ne = createTextSprite(`Wall 1 End / Wall 2 Start (NE)`, 'rgba(15, 23, 42, 0.85)', '#38BDF8', '#94A3B8', 0.65);
        sp_ne.position.set(D_E + 0.25, Y_DIM + 0.35, D_N + OUT_OFFSET);
        labelsGroup.add(sp_ne);

        // Wall 2 (East): Left is (+D_N), Right is (-D_S), at X = +D_E
        const p2_start = new THREE.Vector3(D_E, Y_DIM, D_N);
        const p2_end = new THREE.Vector3(D_E, Y_DIM, -D_S);
        const mid2 = addDimensionLine(p2_start, p2_end, 'x', OUT_OFFSET);
        const sp2 = createTextSprite(`◄── Wall 2 (East): ${{meta.length_z}} m ──►`, 'rgba(10, 25, 45, 0.90)', '#00E5FF', '#FFFFFF');
        sp2.position.copy(mid2);
        sp2.position.y += 0.35;
        labelsGroup.add(sp2);

        const sp_se = createTextSprite(`Wall 2 End / Wall 3 Start (SE)`, 'rgba(15, 23, 42, 0.85)', '#38BDF8', '#94A3B8', 0.65);
        sp_se.position.set(D_E + OUT_OFFSET, Y_DIM + 0.35, -D_S - 0.25);
        labelsGroup.add(sp_se);

        // Wall 3 (South): Left is (+D_E), Right is (-D_W), at Z = -D_S
        const p3_start = new THREE.Vector3(D_E, Y_DIM, -D_S);
        const p3_end = new THREE.Vector3(-D_W, Y_DIM, -D_S);
        const mid3 = addDimensionLine(p3_start, p3_end, 'z', -OUT_OFFSET);
        const sp3 = createTextSprite(`◄── Wall 3 (South): ${{meta.width_x}} m ──►`, 'rgba(10, 25, 45, 0.90)', '#00E5FF', '#FFFFFF');
        sp3.position.copy(mid3);
        sp3.position.y += 0.35;
        labelsGroup.add(sp3);

        const sp_sw = createTextSprite(`Wall 3 End / Wall 4 Start (SW)`, 'rgba(15, 23, 42, 0.85)', '#38BDF8', '#94A3B8', 0.65);
        sp_sw.position.set(-D_W - 0.25, Y_DIM + 0.35, -D_S - OUT_OFFSET);
        labelsGroup.add(sp_sw);

        // Wall 4 (West): Left is (-D_S), Right is (+D_N), at X = -D_W
        const p4_start = new THREE.Vector3(-D_W, Y_DIM, -D_S);
        const p4_end = new THREE.Vector3(-D_W, Y_DIM, D_N);
        const mid4 = addDimensionLine(p4_start, p4_end, 'x', -OUT_OFFSET);
        const sp4 = createTextSprite(`◄── Wall 4 (West): ${{meta.length_z}} m ──►`, 'rgba(10, 25, 45, 0.90)', '#00E5FF', '#FFFFFF');
        sp4.position.copy(mid4);
        sp4.position.y += 0.35;
        labelsGroup.add(sp4);

        // Object distance badges (Elevated high at Y=2.65m with dotted drop lines)
        meta.objects.forEach(obj => {{
            const spObj = createTextSprite(
                obj.label,
                (obj.type === 'bulge' ? 'rgba(45, 22, 5, 0.92)' : 'rgba(5, 35, 18, 0.92)'),
                obj.border,
                '#FFFFFF',
                1.05
            );
            spObj.position.set(obj.x, obj.y, obj.z);
            labelsGroup.add(spObj);

            // Dotted vertical line dropping to object top
            const dropMat = new THREE.LineDashedMaterial({{ color: (obj.type === 'bulge' ? 0xFF8C00 : 0x00E676), dashSize: 0.08, gapSize: 0.08, opacity: 0.7, transparent: true }});
            const dropGeom = new THREE.BufferGeometry().setFromPoints([
                new THREE.Vector3(obj.x, obj.y - 0.25, obj.z),
                new THREE.Vector3(obj.x, obj.target_y, obj.z)
            ]);
            const dropLine = new THREE.Line(dropGeom, dropMat);
            dropLine.computeLineDistances();
            labelsGroup.add(dropLine);
        }});

        // Toggle Labels Handler
        let labelsOn = true;
        window.toggleLabels = function() {{
            labelsOn = !labelsOn;
            labelsGroup.visible = labelsOn;
            const btn = document.getElementById('lblBtn');
            if (labelsOn) {{
                btn.className = 'toggle-btn';
                btn.innerText = '🏷️ Dimension Labels: ON';
            }} else {{
                btn.className = 'toggle-btn off';
                btn.innerText = '🏷️ Dimension Labels: OFF';
            }}
        }};

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
    out_html = "reports/real_scan_3d_viewer.html"
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html_code)
    return out_html


def scan_single_wall_continuous(serial_conn, wall_idx, wall_name):
    print("\n" + "=" * 80)
    print(f"      📍 SCANNING {wall_name.upper()} (WALL {wall_idx} OF 4)")
    print("=" * 80)
    print(f"  Instructions for {wall_name}:")
    print("  1. Aim laser at the LEFT edge / corner of this wall.")
    print("  2. Press [ENTER] to START recording.")
    print("  3. Smoothly sweep laser across to the RIGHT edge / corner.")
    print("  4. Press [ENTER] the exact moment you reach the RIGHT corner to STOP recording!")
    print("=" * 80)

    try:
        input(f"  👉 Aim laser at LEFT corner, then press [ENTER] to START {wall_name}... ")
    except Exception:
        pass

    stop_event = threading.Event()
    distances_local = []
    start_time = time.time()

    def record_loop():
        count = 0
        while not stop_event.is_set():
            elapsed = time.time() - start_time
            raw_dist = None
            flux = 1800

            if serial_conn:
                try:
                    rd, flx = read_sensor_sample(serial_conn)
                    if rd is not None and rd >= 0.0:
                        raw_dist = rd
                        flux = flx
                except Exception:
                    raw_dist = None

            if raw_dist is None:
                if serial_conn:
                    time.sleep(0.015)
                    continue
                else:
                    # Benchtop simulation fallback
                    base_cm = 240.0
                    sim_prog = min(1.0, elapsed / 8.0)
                    sim_yaw = -35.0 + sim_prog * 70.0
                    cos_factor = max(0.5, math.cos(math.radians(sim_yaw)))
                    if wall_idx == 1:
                        if -35.0 <= sim_yaw <= -8.0:
                            sim_d = (base_cm - 65.0) / cos_factor + np.random.normal(0, 0.4)
                        else:
                            sim_d = base_cm / cos_factor + np.random.normal(0, 0.3)
                    elif wall_idx == 2:
                        if 8.0 <= sim_yaw <= 24.0:
                            sim_d = (base_cm + 60.0) / cos_factor + np.random.normal(0, 0.4)
                        else:
                            sim_d = base_cm / cos_factor + np.random.normal(0, 0.3)
                    else:
                        sim_d = base_cm / cos_factor + np.random.normal(0, 0.3)
                    raw_dist = (sim_d - CALIBRATION_OFFSET_CM) / CALIBRATION_SLOPE

            if serial_conn:
                calib_cm = raw_dist
            else:
                calib_cm = (CALIBRATION_SLOPE * raw_dist) + CALIBRATION_OFFSET_CM

            distances_local.append(calib_cm)
            count += 1

            print(f"\r  🔴 [RECORDING LIVE] #{count:03d} points | Elapsed: {elapsed:>4.1f}s | Live Dist: {calib_cm:>6.1f} cm (Flux: {flux:4d})    ", end="", flush=True)
            time.sleep(0.018)

    record_thread = threading.Thread(target=record_loop, daemon=True)
    record_thread.start()

    print(f"\n  🚀 [RECORDING ACTIVE] Sweeping {wall_name.upper()} now!")
    print(f"  👉 Move laser across the wall. Press [ENTER] when you reach the RIGHT corner to STOP... ", end="", flush=True)

    # Debounce 0.4s to prevent the start Enter keypress from instantly stopping the recording
    time.sleep(0.4)
    try:
        import msvcrt
        # Flush any trailing keypresses from the start prompt
        while msvcrt.kbhit():
            msvcrt.getch()
        
        # Wait for user to press ENTER or SPACE when finished sweeping
        while not stop_event.is_set():
            if msvcrt.kbhit():
                ch = msvcrt.getch()
                if ch in (b'\r', b'\n', b' '):
                    break
            time.sleep(0.015)
    except Exception:
        try:
            input()
        except Exception:
            time.sleep(3.0)

    stop_event.set()
    record_thread.join(timeout=1.5)

    sample_count = len(distances_local)

    # If 0 points captured, warn user and retry this wall immediately!
    if sample_count == 0:
        print(f"\n\n  ⚠️ [WARNING] 0 points were captured for {wall_name}!")
        print(f"     Possible causes:")
        print(f"     1. Enter key was pressed too quickly (please sweep for at least 2-3 seconds).")
        print(f"     2. ESP-32 sensor was disconnected or stream was paused.")
        print(f"  👉 Let's re-scan {wall_name} now:\n")
        time.sleep(1.0)
        return scan_single_wall_continuous(serial_conn, wall_idx, wall_name)

    # Generate angles uniformly across captured samples: -35 deg to +35 deg
    angles_local = list(np.linspace(-35.0, 35.0, sample_count))

    print(f"\n  ✅ {wall_name.upper()} COMPLETE! Captured {sample_count} points.")
    return angles_local, distances_local


def main():
    print("\n" + "=" * 80)
    print("      🏢 TF-LUNA 4-WALL SEQUENTIAL CONTINUOUS ROOM SCANNER")
    print("=" * 80)
    print("  We will scan all 4 walls sequentially with pauses in between:")
    print("  • Wall 1 (North / Front Wall)")
    print("  • Wall 2 (East / Right Wall)")
    print("  • Wall 3 (South / Back Wall)")
    print("  • Wall 4 (West / Left Wall)")
    print("\n  Physical 1:1 Metric Depth Mapping:")
    print("  • 🟧 ORANGE: Objects protruding into room (Almari, Bed, Table, Box)")
    print("  • 🟩 GREEN : Openings/Recesses (Gate, Open Doorway, Niche)")
    print("  • 🟦 BLUE  : Normal flat wall baseline")
    print("=" * 80)

    port = find_sensor_port()
    serial_conn = None
    if port:
        try:
            serial_conn = serial.Serial()
            serial_conn.port = port
            serial_conn.baudrate = BAUDRATE
            serial_conn.dtr = False
            serial_conn.rts = False
            serial_conn.timeout = 1
            serial_conn.open()
            time.sleep(0.5)
            serial_conn.reset_input_buffer()
            print(f"\n  ✅ [CONNECTED] TF-Luna ESP-32 found on {port} @ {BAUDRATE} baud!")
        except Exception as e:
            print(f"\n  ⚠️ Port {port} busy or in use: {e}.")
            serial_conn = None

    if not serial_conn:
        print("\n" + "!" * 80)
        print("  ❌ [SENSOR DISCONNECTED / NOT DETECTED ON USB]")
        print("     • Windows ko ESP-32 nahi mila (USB cable loose ya disconnected hai).")
        print("     • Is wajah se pichli baar fake simulation chal gayi thi aur 292 cm dikha raha tha!")
        print("     • Agar real kamra scan karna hai, toh ESP-32 ki USB cable lagayein.")
        print("!" * 80)
        try:
            choice = input("  👉 Kya aap dummy SIMULATION chalana chahte hain (y/n)? ").strip().lower()
            if choice != 'y':
                print("  🛑 Scanning cancelled. Sensor plug karein aur dubara chalayein.\n")
                return
        except Exception:
            return

    walls_info = [
        (1, "North / Front Wall"),
        (2, "East / Right Wall"),
        (3, "South / Back Wall"),
        (4, "West / Left Wall")
    ]

    all_walls_data = []

    # Sequential scan loop with PAUSE after each wall
    for w_idx, w_name in walls_info:
        ang, dist = scan_single_wall_continuous(serial_conn, w_idx, w_name)
        all_walls_data.append((w_idx, w_name, ang, dist))

        if w_idx < 4:
            print("\n" + "─" * 80)
            print(f"  ⏸️ [PAUSE] Wall {w_idx} saved. Turn 90° right to face {walls_info[w_idx][1]}.")
            print("─" * 80)
            try:
                input(f"  👉 Turn in position, then press [ENTER] to continue to Wall {w_idx + 1}... ")
            except Exception:
                pass

    if serial_conn:
        serial_conn.close()

    print("\n\n" + "=" * 80)
    print("      🎉 ALL 4 WALLS SCANNED! ASSEMBLING COMPLETE 3D ROOM DIGITAL TWIN")
    print("=" * 80)

    # 1. Determine baseline perpendicular distances for all 4 walls using cos(theta) flattening:
    # Wall 1: North (+Z), Wall 2: East (+X), Wall 3: South (-Z), Wall 4: West (-X)
    perp_baselines_cm = {}
    for w_idx, w_name, angles, dists in all_walls_data:
        smooth_d = rolling_median(dists, window=5)
        perp_depths = [d * math.cos(math.radians(a)) for a, d in zip(angles, smooth_d)]
        perp_baselines_cm[w_idx] = float(np.median(perp_depths))

    D_N = perp_baselines_cm.get(1, 240.0) / 100.0
    D_E = perp_baselines_cm.get(2, 240.0) / 100.0
    D_S = perp_baselines_cm.get(3, 240.0) / 100.0
    D_W = perp_baselines_cm.get(4, 240.0) / 100.0

    room_width_x = D_W + D_E
    room_length_z = D_N + D_S

    room_3d_points = []
    detected_features = []

    # Process each wall into straight rectangular planar walls with 1:1 metric deviations
    for w_idx, w_name, angles, dists in all_walls_data:
        N = len(dists)
        if N == 0:
            continue
        smooth_d = rolling_median(dists, window=5)
        base_cm = perp_baselines_cm[w_idx]
        # 1. First pass: detect candidate deviations
        candidates = []
        for i, (ang, d_cm) in enumerate(zip(angles, smooth_d)):
            prog = i / max(1, N - 1)
            rad = math.radians(ang)
            perp_depth_cm = d_cm * math.cos(rad)
            dev_cm = perp_depth_cm - base_cm

            # Physical object threshold: at least 15 cm depth deviation
            if dev_cm <= -15.0:
                ft = 'bulge'
            elif dev_cm >= 15.0:
                ft = 'recess'
            else:
                ft = 'wall'
            candidates.append((prog, dev_cm, ft))

        # 2. Cluster candidates: require at least 12 consecutive samples (~25cm width) to qualify as real physical furniture/door
        cluster_map = ['wall'] * N
        cluster_depths = {}
        cur_ft = 'wall'
        cur_idx = []
        for i, (prog, dev_cm, ft) in enumerate(candidates):
            if ft != 'wall':
                if cur_ft == ft:
                    cur_idx.append(i)
                else:
                    if len(cur_idx) >= 12:
                        avg_d = float(np.median([candidates[k][1] for k in cur_idx]))
                        detected_features.append((w_idx, w_name, cur_ft, list(cur_idx)))
                        for k in cur_idx:
                            cluster_map[k] = cur_ft
                            cluster_depths[k] = avg_d
                    cur_ft = ft
                    cur_idx = [i]
            else:
                if len(cur_idx) >= 12:
                    avg_d = float(np.median([candidates[k][1] for k in cur_idx]))
                    detected_features.append((w_idx, w_name, cur_ft, list(cur_idx)))
                    for k in cur_idx:
                        cluster_map[k] = cur_ft
                        cluster_depths[k] = avg_d
                cur_ft = 'wall'
                cur_idx = []
        if len(cur_idx) >= 12:
            avg_d = float(np.median([candidates[k][1] for k in cur_idx]))
            detected_features.append((w_idx, w_name, cur_ft, list(cur_idx)))
            for k in cur_idx:
                cluster_map[k] = cur_ft
                cluster_depths[k] = avg_d

        # 3. Build strictly planar 90-degree rectangular wall points with clean orthogonal steps
        wall_coords = []
        for i in range(N):
            prog = candidates[i][0]
            ftype = cluster_map[i]
            if ftype == 'bulge':
                r, g, b = 255, 140, 0
                max_h = 1.90
                dev_m = (cluster_depths.get(i, -30.0)) / 100.0
            elif ftype == 'recess':
                r, g, b = 0, 230, 118
                max_h = 2.15
                dev_m = (cluster_depths.get(i, 30.0)) / 100.0
            else:
                ftype = 'wall'
                r, g, b = 0, 229, 255
                max_h = 2.40
                dev_m = 0.0  # Nominal wall is strictly FLAT on the rectangular bounding plane!

            # Planar rectangular coordinate math
            if w_idx == 1:
                # North Wall: straight along Z = +D_N
                x_base = -D_W + prog * (D_E + D_W)
                z_base = D_N
                x = x_base
                z = z_base + dev_m
            elif w_idx == 2:
                # East Wall: straight along X = +D_E
                x_base = D_E
                z_base = D_N - prog * (D_N + D_S)
                x = x_base + dev_m
                z = z_base
            elif w_idx == 3:
                # South Wall: straight along Z = -D_S
                x_base = D_E - prog * (D_E + D_W)
                z_base = -D_S
                x = x_base
                z = z_base - dev_m
            elif w_idx == 4:
                # West Wall: straight along X = -D_W
                x_base = -D_W
                z_base = -D_S + prog * (D_N + D_S)
                x = x_base - dev_m
                z = z_base

            wall_coords.append((x, z, x_base, z_base, r, g, b, max_h, ftype))

        # Extrude points
        for idx_pt, (x, z, xb, zb, r, g, b, max_h, ftype) in enumerate(wall_coords):
            for yh in np.linspace(0.1, max_h, 18):
                room_3d_points.append((x, yh, z, r, g, b))

            # Side return walls for rectangular object steps
            is_edge = False
            if idx_pt == 0 and ftype != 'wall':
                is_edge = True
            elif idx_pt == len(wall_coords) - 1 and ftype != 'wall':
                is_edge = True
            elif idx_pt > 0 and wall_coords[idx_pt - 1][8] != ftype:
                is_edge = True
            elif idx_pt < len(wall_coords) - 1 and wall_coords[idx_pt + 1][8] != ftype:
                is_edge = True
            
            if is_edge and ftype != 'wall':
                for interp_d in np.linspace(0, 1, 6):
                    ix = xb + interp_d * (x - xb)
                    iz = zb + interp_d * (z - zb)
                    for yh in np.linspace(0.1, max_h, 10):
                        room_3d_points.append((ix, yh, iz, r, g, b))

    # Ground floor grid
    for fx in np.arange(-D_W, D_E + 0.05, 0.15):
        for fz in np.arange(-D_S, D_N + 0.05, 0.15):
            room_3d_points.append((float(fx), 0.0, float(fz), 20, 35, 55))

    # Detect features metadata
    labeled_objects = []
    for w_idx, w_name, ftype, indices in detected_features:
        w_angs = all_walls_data[w_idx - 1][2]
        w_dists = all_walls_data[w_idx - 1][3]
        w_smooth_d = rolling_median(w_dists, window=5)
        base = perp_baselines_cm[w_idx]
        devs = [w_smooth_d[i] * math.cos(math.radians(w_angs[i])) - base for i in indices]
        avg_dev = abs(float(np.mean(devs)))
        mid_idx = indices[len(indices) // 2]
        prog = mid_idx / max(1, len(w_dists) - 1)

        if w_idx == 1:
            cx = -D_W + prog * (D_E + D_W)
            cz = D_N + (float(np.mean(devs)) / 100.0)
        elif w_idx == 2:
            cx = D_E + (float(np.mean(devs)) / 100.0)
            cz = D_N - prog * (D_N + D_S)
        elif w_idx == 3:
            cx = D_E - prog * (D_E + D_W)
            cz = -D_S - (float(np.mean(devs)) / 100.0)
        elif w_idx == 4:
            cx = -D_W - (float(np.mean(devs)) / 100.0)
            cz = -D_S + prog * (D_N + D_S)

        if ftype == 'bulge':
            labeled_objects.append({
                'name': 'Almari',
                'type': 'bulge',
                'label': f"Almari: {avg_dev:.0f} cm Bahar (Inward Bulge)",
                'dist_cm': int(round(avg_dev)),
                'x': float(round(cx, 3)), 'y': 2.65, 'z': float(round(cz, 3)),
                'target_y': 1.9,
                'color': '#FF8C00',
                'border': '#FFA726'
            })
        elif ftype == 'recess':
            labeled_objects.append({
                'name': 'Gate',
                'type': 'recess',
                'label': f"Gate: {avg_dev:.0f} cm Andar (Outward Recess)",
                'dist_cm': int(round(avg_dev)),
                'x': float(round(cx, 3)), 'y': 2.65, 'z': float(round(cz, 3)),
                'target_y': 2.15,
                'color': '#00E676',
                'border': '#69F0AE'
            })

    meta = {
        'D_N': float(round(D_N, 3)), 'D_E': float(round(D_E, 3)), 'D_S': float(round(D_S, 3)), 'D_W': float(round(D_W, 3)),
        'width_x': float(round(room_width_x, 3)),
        'length_z': float(round(room_length_z, 3)),
        'objects': labeled_objects
    }

    # Save to standard PLY files
    ply_path = "reports/continuous_scan.ply"
    save_ply(ply_path, room_3d_points)
    save_ply("data/room_scan.ply", room_3d_points)
    save_ply("data/live_scan.ply", room_3d_points)

    # Generate clean WebGL viewer (with rectangular dimension lines & object labels)
    html_path = generate_clean_web_viewer(ply_path, meta)
    print(f"  🌐 Clean Rectangular 3D Room Viewer: '{html_path}'")

    # Save permanently into scans/ archive folder so scans can be revisited anytime
    archive_scan(ply_path, html_path, meta)

    # Launch browser automatically
    try:
        import webbrowser
        webbrowser.open(f"file:///{os.path.abspath(html_path)}")
        print("  🚀 Opened 3D Room in your web browser!")
    except Exception:
        pass


def archive_scan(ply_path, html_path, meta):
    """Permanently saves every scan into scans/ folder with timestamp so scans are never lost."""
    os.makedirs("scans", exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    date_str = time.strftime("%Y-%m-%d %H:%M:%S")

    arc_ply = f"scans/room_scan_{ts}.ply"
    arc_html = f"scans/room_scan_{ts}_viewer.html"
    arc_meta = f"scans/room_scan_{ts}_meta.json"

    try:
        import shutil
        shutil.copyfile(ply_path, arc_ply)
        shutil.copyfile(html_path, arc_html)
        with open(arc_meta, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)
    except Exception as e:
        print(f"  ⚠️ Archive copy error: {e}")

    # Append to scans catalog
    catalog_path = "scans/scan_catalog.json"
    catalog = []
    if os.path.exists(catalog_path):
        try:
            with open(catalog_path, "r", encoding="utf-8") as f:
                catalog = json.load(f)
        except Exception:
            catalog = []

    catalog.append({
        'scan_id': f"room_scan_{ts}",
        'timestamp': ts,
        'date_time': date_str,
        'ply_file': arc_ply,
        'html_file': arc_html,
        'width_x': meta.get('width_x'),
        'length_z': meta.get('length_z'),
        'objects_count': len(meta.get('objects', []))
    })

    try:
        with open(catalog_path, "w", encoding="utf-8") as f:
            json.dump(catalog, f, indent=2)
        from scratch.generate_catalog_page import generate_catalog_html
        generate_catalog_html()
    except Exception:
        pass

    print(f"\n  💾 [PERMANENT ARCHIVE SAVED] Scanned room stored permanently in:")
    print(f"     📁 HTML Viewer: '{arc_html}' (Double-click to open anytime)")
    print(f"     📁 Point Cloud: '{arc_ply}'")
    return arc_html


if __name__ == '__main__':
    main()
