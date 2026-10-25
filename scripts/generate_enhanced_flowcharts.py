import os
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.stdout.reconfigure(encoding='utf-8')

assets_dir = r"c:\Users\nisar\OneDrive\Desktop\TF_LUNA_PROJECT\reports\assets"
os.makedirs(assets_dir, exist_ok=True)

# Set global matplotlib styles for ultra-crisp, professional typography
plt.rcParams['font.sans-serif'] = 'Arial', 'DejaVu Sans', 'Helvetica'
plt.rcParams['font.family'] = 'sans-serif'

# -------------------------------------------------------------
# FLOWCHART 1: SYSTEM ARCHITECTURE (FULL-WIDTH CRISP)
# -------------------------------------------------------------
def create_flowchart_system_architecture():
    fig, ax = plt.subplots(figsize=(13, 5.2), dpi=300)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 5.2)
    ax.axis('off')

    cols = [
        ("1. TARGET FACADE", 0.3, 2.3, "#F8FAFC", "#0F172A"),
        ("2. EMBEDDED SENSING", 2.8, 2.4, "#EFF6FF", "#1E3A8A"),
        ("3. TELEMETRY & LOGGING", 5.4, 2.2, "#F0FDFA", "#0D9488"),
        ("4. GROUND ANALYTICS", 7.8, 2.5, "#FEF3C7", "#D97706"),
        ("5. 3D TWIN & REPORT", 10.5, 2.2, "#ECFDF5", "#059669")
    ]

    for title, x, w, bg, fg in cols:
        rect = patches.FancyBboxPatch((x, 0.25), w, 4.7, boxstyle="round,pad=0.12",
                                      facecolor=bg, edgecolor=fg, linewidth=2.0)
        ax.add_patch(rect)
        ax.text(x + w/2, 4.65, title, ha='center', va='center', fontsize=11, fontweight='bold', color=fg)

    # Col 1: Target
    b1 = patches.FancyBboxPatch((0.45, 2.6), 2.0, 1.7, boxstyle="round,pad=0.1", facecolor="#FFFFFF", edgecolor="#64748B", linewidth=1.5)
    ax.add_patch(b1)
    ax.text(1.45, 3.8, "Concrete Facade / Piers", ha='center', va='center', fontsize=10, fontweight='bold', color="#0F172A")
    ax.text(1.45, 3.1, "• High-rise vertical walls\n• Highway bridge piers\n• Indoor lab room envelope", ha='center', va='center', fontsize=9, color="#334155")

    b1_def = patches.FancyBboxPatch((0.45, 0.55), 2.0, 1.8, boxstyle="round,pad=0.1", facecolor="#FEE2E2", edgecolor="#DC2626", linewidth=1.5)
    ax.add_patch(b1_def)
    ax.text(1.45, 2.05, "Structural Defects", ha='center', va='center', fontsize=10, fontweight='bold', color="#991B1B")
    ax.text(1.45, 1.25, "• Spall Cavity (Δd ≥ +3.5 cm)\n• Bulge / Buckle (Δd ≤ -3.5 cm)\n• Crack (|Δd| ≥ 1.5 cm vs nbrs)", ha='center', va='center', fontsize=8.8, color="#7F1D1D")

    # Col 2: Sensing
    b2_tf = patches.FancyBboxPatch((2.95, 3.2), 2.1, 1.15, boxstyle="round,pad=0.1", facecolor="#DBEAFE", edgecolor="#2563EB", linewidth=1.5)
    ax.add_patch(b2_tf)
    ax.text(4.0, 3.9, "TF-Luna 850nm dToF", ha='center', va='center', fontsize=9.8, fontweight='bold', color="#1E40AF")
    ax.text(4.0, 3.45, "Single-point 100 Hz (<5g, 0.35W)", ha='center', va='center', fontsize=8.8, color="#1E3A8A")

    b2_yd = patches.FancyBboxPatch((2.95, 1.9), 2.1, 1.15, boxstyle="round,pad=0.1", facecolor="#E0E7FF", edgecolor="#4F46E5", linewidth=1.5)
    ax.add_patch(b2_yd)
    ax.text(4.0, 2.6, "YDLIDAR X2 360° (Upgrade)", ha='center', va='center', fontsize=9.8, fontweight='bold', color="#3730A3")
    ax.text(4.0, 2.15, "2D Planar Slicing, 3 kHz, 7 Hz", ha='center', va='center', fontsize=8.8, color="#312E81")

    b2_mcu = patches.FancyBboxPatch((2.95, 0.55), 2.1, 1.15, boxstyle="round,pad=0.1", facecolor="#FFFFFF", edgecolor="#0284C7", linewidth=1.5)
    ax.add_patch(b2_mcu)
    ax.text(4.0, 1.3, "ESP32 MCU + Tilt Sensor", ha='center', va='center', fontsize=9.8, fontweight='bold', color="#0369A1")
    ax.text(4.0, 0.85, "Cal Fit: y = 1.0228x + 3.20 cm\nCosine Tilt Correction: d·cos θ", ha='center', va='center', fontsize=8.5, color="#0C4A6E")

    # Col 3: Telemetry
    b3_uart = patches.FancyBboxPatch((5.55, 2.7), 1.9, 1.6, boxstyle="round,pad=0.1", facecolor="#FFFFFF", edgecolor="#0D9488", linewidth=1.5)
    ax.add_patch(b3_uart)
    ax.text(6.5, 3.8, "Wired Serial Streaming", ha='center', va='center', fontsize=9.8, fontweight='bold', color="#0F766E")
    ax.text(6.5, 3.1, "• USB-UART at 115200 baud\n• Continuous CSV logging\n• Timestamped distance & temp", ha='center', va='center', fontsize=8.8, color="#134E4A")

    b3_udp = patches.FancyBboxPatch((5.55, 0.55), 1.9, 1.9, boxstyle="round,pad=0.1", facecolor="#CCFBF1", edgecolor="#0F766E", linewidth=1.5)
    ax.add_patch(b3_udp)
    ax.text(6.5, 2.05, "Wireless Telemetry", ha='center', va='center', fontsize=9.8, fontweight='bold', color="#115E59")
    ax.text(6.5, 1.25, "• Wi-Fi 802.11 b/g/n\n• UDP Broadcast (Port 5005)\n• Low-latency packet stream", ha='center', va='center', fontsize=8.8, color="#134E4A")

    # Col 4: Ground Analytics
    b4_base = patches.FancyBboxPatch((7.95, 2.7), 2.2, 1.6, boxstyle="round,pad=0.1", facecolor="#FFFFFF", edgecolor="#D97706", linewidth=1.5)
    ax.add_patch(b4_base)
    ax.text(9.05, 3.8, "Adaptive Baseline Filter", ha='center', va='center', fontsize=9.8, fontweight='bold', color="#B45309")
    ax.text(9.05, 3.1, "• Window mean: N=15 samples\n• Reference tracking: d_ref\n• Residual metric: Δd = d - d_ref", ha='center', va='center', fontsize=8.8, color="#78350F")

    b4_def = patches.FancyBboxPatch((7.95, 0.55), 2.2, 1.9, boxstyle="round,pad=0.1", facecolor="#FEF3C7", edgecolor="#B45309", linewidth=1.5)
    ax.add_patch(b4_def)
    ax.text(9.05, 2.05, "Automated Classifier", ha='center', va='center', fontsize=9.8, fontweight='bold', color="#B45309")
    ax.text(9.05, 1.25, "• Spall: Δd ≥ +3.5 cm (Orange)\n• Bulge: Δd ≤ -3.5 cm (Orange)\n• Crack: |Δd| ≥ 1.5 cm vs nbrs\n• Intact: |Δd| < 2.5 cm (Cyan)", ha='center', va='center', fontsize=8.6, color="#78350F")

    # Col 5: 3D Twin & Report
    b5_ply = patches.FancyBboxPatch((10.65, 2.7), 1.9, 1.6, boxstyle="round,pad=0.1", facecolor="#FFFFFF", edgecolor="#059669", linewidth=1.5)
    ax.add_patch(b5_ply)
    ax.text(11.6, 3.8, "3D Room Reconstruction", ha='center', va='center', fontsize=9.8, fontweight='bold', color="#047857")
    ax.text(11.6, 3.1, "• 9,969-point digital twin\n• Almari bulge: +65 cm\n• Gate recess: -60 cm\n• Standardized .PLY format", ha='center', va='center', fontsize=8.8, color="#064E3B")

    b5_ui = patches.FancyBboxPatch((10.65, 0.55), 1.9, 1.9, boxstyle="round,pad=0.1", facecolor="#D1FAE5", edgecolor="#047857", linewidth=1.5)
    ax.add_patch(b5_ui)
    ax.text(11.6, 2.05, "PLY Forge & Dashboard", ha='center', va='center', fontsize=9.8, fontweight='bold', color="#065F46")
    ax.text(11.6, 1.25, "• In-browser WebGL rendering\n• 5-tab Streamlit Ground UI\n• Voxel downsampling (70%)\n• PDF Audit report generator", ha='center', va='center', fontsize=8.6, color="#064E3B")

    # Connective Arrows
    arrow_props = dict(arrowstyle="->", color="#1E3A8A", lw=2.2, mutation_scale=16)
    ax.annotate("", xy=(2.85, 3.8), xytext=(2.45, 3.8), arrowprops=arrow_props)
    ax.annotate("", xy=(2.85, 2.5), xytext=(2.45, 2.5), arrowprops=arrow_props)
    ax.annotate("", xy=(5.45, 3.5), xytext=(5.05, 3.5), arrowprops=arrow_props)
    ax.annotate("", xy=(5.45, 1.5), xytext=(5.05, 1.2), arrowprops=arrow_props)
    ax.annotate("", xy=(7.85, 3.5), xytext=(7.45, 3.5), arrowprops=arrow_props)
    ax.annotate("", xy=(10.55, 3.5), xytext=(10.15, 3.5), arrowprops=arrow_props)
    ax.annotate("", xy=(10.55, 1.5), xytext=(10.15, 1.5), arrowprops=arrow_props)

    plt.tight_layout()
    out_path = os.path.join(assets_dir, "flowchart_system_architecture.png")
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Generated {out_path}")

# -------------------------------------------------------------
# FLOWCHART 2: AERIAL / SENSING ACQUISITION WORKFLOW (ENHANCED)
# -------------------------------------------------------------
def create_flowchart_aerial_acquisition():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.2)
    ax.axis('off')

    # Steps formatted in clear 2-row pipeline
    # Top Row: Ingestion, Validation, Calibration
    steps_top = [
        ("1. Boot & Hardware Init", "ESP32 GPIOs, UART1 (LiDAR),\nUART2 (Debug), I2C / Tilt pin", 0.4, 3.8, 2.5, 1.8, "#F1F5F9", "#0F172A"),
        ("2. UART Frame Sync", "Scan incoming byte stream\nfor 0x59 0x59 preamble", 3.2, 3.8, 2.5, 1.8, "#DBEAFE", "#1E40AF"),
        ("3. Ingest Data Bytes", "Read 9-byte packet:\nDist_L/H, Amp_L/H, Temp", 6.0, 3.8, 2.5, 1.8, "#DBEAFE", "#1E40AF"),
        ("4. Checksum Verification", "Check condition:\n(Σ Byte 0..7) & 0xFF == Byte 8", 8.8, 3.8, 2.8, 1.8, "#FEF3C7", "#B45309"),
    ]

    for title, desc, x, y, w, h, bg, fg in steps_top:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.12", facecolor=bg, edgecolor=fg, linewidth=2.0)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h*0.75, title, ha='center', va='center', fontsize=11, fontweight='bold', color=fg)
        ax.text(x + w/2, y + h*0.35, desc, ha='center', va='center', fontsize=9.5, color="#1E293B", linespacing=1.3)

    # Bottom Row: Actions based on Checksum
    steps_bot = [
        ("5. Corrupt Frame Discard", "Checksum failure detected:\nFlush buffer, resync 0x59 0x59", 8.8, 0.8, 2.8, 1.8, "#FEE2E2", "#DC2626"),
        ("6. Two-Point Calibration", "Apply universal regression:\ny = 1.0228·x + 3.20 cm (RMSE ±0.02cm)", 6.0, 0.8, 2.5, 1.8, "#DCFCE7", "#15803D"),
        ("7. Tilt Compensation", "Sample pitch/roll θ from tilt sensor:\nd_true = d_cal · cos(θ)", 3.2, 0.8, 2.5, 1.8, "#CCFBF1", "#0D9488"),
        ("8. Filter & Broadcast", "Apply running median (N=5);\nBroadcast via UDP / Streamlit CSV", 0.4, 0.8, 2.5, 1.8, "#ECFDF5", "#059669")
    ]

    for title, desc, x, y, w, h, bg, fg in steps_bot:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.12", facecolor=bg, edgecolor=fg, linewidth=2.0)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h*0.75, title, ha='center', va='center', fontsize=11, fontweight='bold', color=fg)
        ax.text(x + w/2, y + h*0.35, desc, ha='center', va='center', fontsize=9.5, color="#1E293B", linespacing=1.3)

    # Connective Arrows Top Row
    arr = dict(arrowstyle="->", color="#1E3A8A", lw=2.2, mutation_scale=16)
    ax.annotate("", xy=(3.15, 4.7), xytext=(2.9, 4.7), arrowprops=arr)
    ax.annotate("", xy=(5.95, 4.7), xytext=(5.7, 4.7), arrowprops=arr)
    ax.annotate("", xy=(8.75, 4.7), xytext=(8.5, 4.7), arrowprops=arr)

    # Checksum FAIL -> Box 5 (Down)
    ax.annotate("", xy=(10.2, 2.65), xytext=(10.2, 3.75),
                arrowprops=dict(arrowstyle="->", color="#DC2626", lw=2.4, mutation_scale=16))
    ax.text(10.35, 3.2, "FAIL (Corrupt)", fontsize=10, fontweight='bold', color="#DC2626")

    # Box 5 -> Resync loop back to Box 2
    ax.annotate("", xy=(4.45, 3.75), xytext=(9.2, 2.65),
                arrowprops=dict(arrowstyle="->", color="#DC2626", lw=1.8, linestyle="--",
                                connectionstyle="arc3,rad=-0.25", mutation_scale=14))
    ax.text(6.8, 3.1, "Discard & Resync", fontsize=9, fontweight='bold', color="#DC2626")

    # Checksum VALID -> Box 6 (Diagonal/Turn Left)
    ax.annotate("", xy=(7.25, 2.65), xytext=(9.2, 3.75),
                arrowprops=dict(arrowstyle="->", color="#15803D", lw=2.4, mutation_scale=16))
    ax.text(7.6, 3.3, "VALID (Pass)", fontsize=10, fontweight='bold', color="#15803D")

    # Bottom Row Flow (Right to Left: 6 -> 7 -> 8)
    arr_bot = dict(arrowstyle="->", color="#059669", lw=2.2, mutation_scale=16)
    ax.annotate("", xy=(5.75, 1.7), xytext=(5.95, 1.7), arrowprops=arr_bot)
    ax.annotate("", xy=(2.95, 1.7), xytext=(3.15, 1.7), arrowprops=arr_bot)

    # Output annotation from Box 8
    ax.annotate("", xy=(1.65, 0.4), xytext=(1.65, 0.75),
                arrowprops=dict(arrowstyle="->", color="#059669", lw=2.4, mutation_scale=16))
    ax.text(1.65, 0.2, "STREAMING TO GROUND STATION (100 Hz)", ha='center', va='center',
            fontsize=9.5, fontweight='bold', color="#047857")

    plt.tight_layout()
    out_path = os.path.join(assets_dir, "flowchart_aerial_acquisition.png")
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Generated {out_path}")

# -------------------------------------------------------------
# FLOWCHART 3: GROUND ANALYTICS & DEFECT CLASSIFIER (ENHANCED)
# -------------------------------------------------------------
def create_flowchart_ground_analytics():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.2)
    ax.axis('off')

    # Left Column: Telemetry Ingestion & Baseline
    p1 = patches.FancyBboxPatch((0.4, 3.6), 2.5, 2.0, boxstyle="round,pad=0.12", facecolor="#EFF6FF", edgecolor="#1E40AF", linewidth=2.0)
    ax.add_patch(p1)
    ax.text(1.65, 5.15, "1. Telemetry Ingestion", ha='center', va='center', fontsize=11.5, fontweight='bold', color="#1E3A8A")
    ax.text(1.65, 4.3, "• Receive d_true(t), θ, Amp\n• USB-UART / UDP stream\n• Verify packet timestamp", ha='center', va='center', fontsize=9.5, color="#1E293B", linespacing=1.3)

    p2 = patches.FancyBboxPatch((0.4, 0.8), 2.5, 2.2, boxstyle="round,pad=0.12", facecolor="#EFF6FF", edgecolor="#1E40AF", linewidth=2.0)
    ax.add_patch(p2)
    ax.text(1.65, 2.55, "2. Baseline Tracking", ha='center', va='center', fontsize=11.5, fontweight='bold', color="#1E3A8A")
    ax.text(1.65, 1.65, "• Compute rolling window:\n  d_ref = Mean(window N=15)\n• Residual Calculation:\n  Δd = d_meas - d_ref", ha='center', va='center', fontsize=9.5, color="#1E293B", linespacing=1.3)

    # Arrow 1 -> 2
    ax.annotate("", xy=(1.65, 3.05), xytext=(1.65, 3.55),
                arrowprops=dict(arrowstyle="->", color="#1E3A8A", lw=2.2, mutation_scale=16))

    # Center: Decision Engine Box
    p3 = patches.FancyBboxPatch((3.5, 1.8), 3.5, 3.0, boxstyle="round,pad=0.15", facecolor="#FEF3C7", edgecolor="#B45309", linewidth=2.2)
    ax.add_patch(p3)
    ax.text(5.25, 4.35, "3. Defect Classification Engine", ha='center', va='center', fontsize=12, fontweight='bold', color="#78350F")
    ax.text(5.25, 3.2, "Evaluate Residual Δd against Thresholds:\n\n1. Spall condition: Is Δd ≥ +3.5 cm?\n2. Bulge condition: Is Δd ≤ -3.5 cm?\n3. Crack condition: Is |Δd| ≥ 1.5 cm vs nbrs?\n4. Baseline: Is |Δd| < 2.5 cm (Normal)?",
            ha='center', va='center', fontsize=9.8, color="#1E293B", linespacing=1.3)

    # Arrow 2 -> 3
    ax.annotate("", xy=(3.45, 3.3), xytext=(2.95, 2.0),
                arrowprops=dict(arrowstyle="->", color="#1E3A8A", lw=2.2, mutation_scale=16))

    # Right Column: 4 Classified Outcomes
    outcomes = [
        ("Spall Cavity (Orange)", "Concrete flaked inward (Δd ≥ +3.5 cm)\nSevere moisture & structural risk", 7.6, 4.7, 4.0, 1.25, "#FFEDD5", "#C2410C"),
        ("Structural Bulge (Orange)", "Delamination / buckling (Δd ≤ -3.5 cm)\nMasonry protruding outward", 7.6, 3.3, 4.0, 1.25, "#FFEDD5", "#C2410C"),
        ("Crack Indication (Gold)", "Localized depth spike (|Δd| ≥ 1.5 cm vs nbrs)\nPotential shear fracture", 7.6, 1.9, 4.0, 1.25, "#FEF9C3", "#A16207"),
        ("Uniform Facade (Cyan)", "Within structural tolerance (|Δd| < 2.5 cm)\nHealthy baseline profile", 7.6, 0.5, 4.0, 1.25, "#CFFAFE", "#0891B2")
    ]

    for title, desc, x, y, w, h, bg, fg in outcomes:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1", facecolor=bg, edgecolor=fg, linewidth=1.8)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h*0.72, title, ha='center', va='center', fontsize=10.5, fontweight='bold', color=fg)
        ax.text(x + w/2, y + h*0.3, desc, ha='center', va='center', fontsize=9.0, color="#1E293B", linespacing=1.2)

    # Branches to outcomes
    ax.annotate("", xy=(7.55, 5.3), xytext=(7.05, 4.0),
                arrowprops=dict(arrowstyle="->", color="#C2410C", lw=2.0, mutation_scale=14))
    ax.annotate("", xy=(7.55, 3.9), xytext=(7.05, 3.5),
                arrowprops=dict(arrowstyle="->", color="#C2410C", lw=2.0, mutation_scale=14))
    ax.annotate("", xy=(7.55, 2.5), xytext=(7.05, 2.9),
                arrowprops=dict(arrowstyle="->", color="#A16207", lw=2.0, mutation_scale=14))
    ax.annotate("", xy=(7.55, 1.1), xytext=(7.05, 2.3),
                arrowprops=dict(arrowstyle="->", color="#0891B2", lw=2.0, mutation_scale=14))

    plt.tight_layout()
    out_path = os.path.join(assets_dir, "flowchart_ground_analytics.png")
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Generated {out_path}")

# -------------------------------------------------------------
# FLOWCHART 4: DUAL-PLATFORM POWER & WIRING ARCHITECTURE (ENHANCED)
# -------------------------------------------------------------
def create_flowchart_power_wiring():
    fig, ax = plt.subplots(figsize=(12, 6.4), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.4)
    ax.axis('off')

    # Background Section Bands: Drone Platform (Top) vs Smart 4WD Car (Bottom)
    drone_bg = patches.FancyBboxPatch((0.2, 3.4), 11.6, 2.8, boxstyle="round,pad=0.1", facecolor="#F8FAFC", edgecolor="#1E3A8A", linewidth=1.5)
    ax.add_patch(drone_bg)
    ax.text(6.0, 6.0, "OPTION A: AERIAL DRONE SUBSYSTEM POWER ARCHITECTURE", ha='center', va='center', fontsize=11, fontweight='bold', color="#1E3A8A")

    # Drone: Battery -> PDB -> ESCs & UBEC -> Avionics
    p_bat = patches.FancyBboxPatch((0.4, 3.7), 2.2, 1.8, boxstyle="round,pad=0.1", facecolor="#FEE2E2", edgecolor="#DC2626", linewidth=1.8)
    ax.add_patch(p_bat)
    ax.text(1.5, 5.0, "3S LiPo Battery", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#991B1B")
    ax.text(1.5, 4.25, "11.1V (12.6V Max)\n4200 mAh, 35C\nXT60 Main Lead", ha='center', va='center', fontsize=9.0, color="#1E293B", linespacing=1.2)

    p_pdb = patches.FancyBboxPatch((3.1, 3.7), 2.3, 1.8, boxstyle="round,pad=0.1", facecolor="#FEF3C7", edgecolor="#D97706", linewidth=1.8)
    ax.add_patch(p_pdb)
    ax.text(4.25, 5.0, "Power Dist. Board", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#92400E")
    ax.text(4.25, 4.25, "11.1V High-Current Bus\n4x ESC Power Rails\nAuxiliary 11.1V Tap", ha='center', va='center', fontsize=9.0, color="#1E293B", linespacing=1.2)

    p_mot = patches.FancyBboxPatch((5.9, 4.5), 2.6, 1.25, boxstyle="round,pad=0.1", facecolor="#F1F5F9", edgecolor="#475569", linewidth=1.5)
    ax.add_patch(p_mot)
    ax.text(7.2, 5.35, "4x 30A ESCs & Motors", ha='center', va='center', fontsize=10, fontweight='bold', color="#1E293B")
    ax.text(7.2, 4.85, "11.1V Direct | Max Thrust = 3,200g", ha='center', va='center', fontsize=8.8, color="#475569")

    p_bec = patches.FancyBboxPatch((5.9, 3.5), 2.6, 0.9, boxstyle="round,pad=0.1", facecolor="#DCFCE7", edgecolor="#16A34A", linewidth=1.5)
    ax.add_patch(p_bec)
    ax.text(7.2, 4.15, "5V 5A UBEC Step-Down", ha='center', va='center', fontsize=9.8, fontweight='bold', color="#15803D")
    ax.text(7.2, 3.75, "Clean 5.0V Ripple-Free Rail", ha='center', va='center', fontsize=8.5, color="#166534")

    p_av = patches.FancyBboxPatch((9.0, 3.6), 2.6, 2.1, boxstyle="round,pad=0.1", facecolor="#DBEAFE", edgecolor="#2563EB", linewidth=1.8)
    ax.add_patch(p_av)
    ax.text(10.3, 5.3, "Drone Avionics & Payload", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#1E40AF")
    ax.text(10.3, 4.4, "• Pixhawk 2.4.8 Autopilot (5V, 1A)\n• YDLIDAR X2 Core & Motor (5V, 0.5A)\n• ESP32 MCU Telemetry (5V, 0.2A)\n• DFRobot Tilt Sensor (5V, 10mA)",
            ha='center', va='center', fontsize=8.8, color="#1E3A8A", linespacing=1.25)

    # Drone Wiring Arrows
    ax.annotate("", xy=(3.05, 4.6), xytext=(2.65, 4.6), arrowprops=dict(arrowstyle="->", color="#DC2626", lw=2.2, mutation_scale=14))
    ax.text(2.85, 4.8, "11.1V", fontsize=8.5, fontweight='bold', color="#DC2626")

    ax.annotate("", xy=(5.85, 5.1), xytext=(5.45, 4.8), arrowprops=dict(arrowstyle="->", color="#DC2626", lw=2.0, mutation_scale=14))
    ax.annotate("", xy=(5.85, 3.95), xytext=(5.45, 4.3), arrowprops=dict(arrowstyle="->", color="#D97706", lw=2.0, mutation_scale=14))

    ax.annotate("", xy=(8.95, 4.4), xytext=(8.55, 3.95), arrowprops=dict(arrowstyle="->", color="#16A34A", lw=2.2, mutation_scale=14))
    ax.text(8.75, 4.4, "5.0V", fontsize=9, fontweight='bold', color="#16A34A")

    # Bottom Band: Smart 4WD Car Platform Power
    car_bg = patches.FancyBboxPatch((0.2, 0.2), 11.6, 2.9, boxstyle="round,pad=0.1", facecolor="#F8FAFC", edgecolor="#D97706", linewidth=1.5)
    ax.add_patch(car_bg)
    ax.text(6.0, 2.85, "OPTION B: SMART 4WD GROUND CAR SUBSYSTEM POWER ARCHITECTURE", ha='center', va='center', fontsize=11, fontweight='bold', color="#D97706")

    c_bat = patches.FancyBboxPatch((0.4, 0.5), 2.2, 1.9, boxstyle="round,pad=0.1", facecolor="#FEF3C7", edgecolor="#D97706", linewidth=1.8)
    ax.add_patch(c_bat)
    ax.text(1.5, 1.9, "12V Li-ion Pack", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#92400E")
    ax.text(1.5, 1.15, "12V Nominal (3S 18650)\n2200 mAh High Discharge\n2--3 Hour Run Time", ha='center', va='center', fontsize=9.0, color="#1E293B", linespacing=1.2)

    c_drv = patches.FancyBboxPatch((3.1, 0.5), 2.4, 1.9, boxstyle="round,pad=0.1", facecolor="#FFFFFF", edgecolor="#EA580C", linewidth=1.8)
    ax.add_patch(c_drv)
    ax.text(4.3, 1.9, "L298N / TB6612FNG Driver", ha='center', va='center', fontsize=10, fontweight='bold', color="#C2410C")
    ax.text(4.3, 1.15, "Dual H-Bridge Motor Control\nPWM Speed Control (5.0 cm/s)\nFeeds 4x DC Motors directly", ha='center', va='center', fontsize=8.8, color="#1E293B", linespacing=1.2)

    c_mot = patches.FancyBboxPatch((6.0, 1.55), 2.6, 1.1, boxstyle="round,pad=0.1", facecolor="#F1F5F9", edgecolor="#475569", linewidth=1.5)
    ax.add_patch(c_mot)
    ax.text(7.3, 2.25, "4x 1:48 Gear DC Motors", ha='center', va='center', fontsize=9.8, fontweight='bold', color="#1E293B")
    ax.text(7.3, 1.8, "High-Traction 65mm Wheels", ha='center', va='center', fontsize=8.5, color="#475569")

    c_buck = patches.FancyBboxPatch((6.0, 0.4), 2.6, 1.0, boxstyle="round,pad=0.1", facecolor="#DCFCE7", edgecolor="#16A34A", linewidth=1.5)
    ax.add_patch(c_buck)
    ax.text(7.3, 1.05, "LM2596 Buck Step-Down", ha='center', va='center', fontsize=9.8, fontweight='bold', color="#15803D")
    ax.text(7.3, 0.65, "12V -> 5.0V 2A Regulated Bus", ha='center', va='center', fontsize=8.5, color="#166534")

    c_payload = patches.FancyBboxPatch((9.1, 0.5), 2.5, 2.0, boxstyle="round,pad=0.1", facecolor="#ECFDF5", edgecolor="#059669", linewidth=1.8)
    ax.add_patch(c_payload)
    ax.text(10.35, 2.1, "Car Sensing Mast Payload", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#065F46")
    ax.text(10.35, 1.25, "• ESP32 MCU (Odometry PID)\n• Dual Optical Encoders (1.02 mm/tick)\n• YDLIDAR X2 or TF-Luna ToF\n• Telescoping Mast (0.2--2.2m)",
            ha='center', va='center', fontsize=8.8, color="#064E3B", linespacing=1.25)

    # Car Wiring Arrows
    ax.annotate("", xy=(3.05, 1.45), xytext=(2.65, 1.45), arrowprops=dict(arrowstyle="->", color="#D97706", lw=2.2, mutation_scale=14))
    ax.text(2.85, 1.65, "12V", fontsize=8.5, fontweight='bold', color="#D97706")

    ax.annotate("", xy=(5.95, 2.0), xytext=(5.55, 1.7), arrowprops=dict(arrowstyle="->", color="#C2410C", lw=2.0, mutation_scale=14))
    ax.annotate("", xy=(5.95, 0.9), xytext=(5.55, 1.2), arrowprops=dict(arrowstyle="->", color="#D97706", lw=2.0, mutation_scale=14))

    ax.annotate("", xy=(9.05, 1.3), xytext=(8.65, 0.9), arrowprops=dict(arrowstyle="->", color="#16A34A", lw=2.2, mutation_scale=14))
    ax.text(8.85, 1.3, "5.0V", fontsize=9, fontweight='bold', color="#16A34A")

    plt.tight_layout()
    out_path = os.path.join(assets_dir, "flowchart_power_wiring.png")
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Generated {out_path}")

# -------------------------------------------------------------
# FLOWCHART 5: 7-PHASE TESTING & ROADMAP (ENHANCED)
# -------------------------------------------------------------
def create_flowchart_testing_roadmap():
    fig, ax = plt.subplots(figsize=(13, 5.5), dpi=300)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 5.5)
    ax.axis('off')

    phases = [
        ("Phase 1: Design", "CAD Mounts\nPin Schematics\nBudget Sign-off", 0.3, 3.2, "#F1F5F9", "#0F172A"),
        ("Phase 2: Bench Test", "YDLIDAR X2 UART\nTilt Sensor Int\n5V UBEC Load", 2.1, 3.2, "#DBEAFE", "#1E40AF"),
        ("Phase 3: Sensor Fusion", "Tilt Compensation\nTwo-point Calibration\nFreeRTOS Driver", 3.9, 3.2, "#FEF3C7", "#D97706"),
        ("Phase 4: Airframe / Car", "F450 Frame / 4WD Car\nSilicone Isolator\nPixhawk Config", 5.7, 3.2, "#E0E7FF", "#4338CA"),
        ("Phase 5: Ground UI", "PLY Forge WebGL\nUDP Point Buffer\nAutomated Audit", 7.5, 3.2, "#F0FDFA", "#0D9488"),
        ("Phase 6: Field Trials", "Car Corridor Sweep\nTethered Hover\nSpall Verification", 9.3, 3.2, "#FCE7F3", "#BE185D"),
        ("Phase 7: Final Demo", "Faculty Demo\nLongitudinal Baseline\nFull Report Archive", 11.1, 3.2, "#DCFCE7", "#15803D")
    ]

    for title, desc, x, y, bg, fg in phases:
        rect = patches.FancyBboxPatch((x, y), 1.6, 1.9, boxstyle="round,pad=0.1", facecolor=bg, edgecolor=fg, linewidth=1.8)
        ax.add_patch(rect)
        ax.text(x + 0.8, y + 1.45, title, ha='center', va='center', fontsize=9.8, fontweight='bold', color=fg)
        ax.text(x + 0.8, y + 0.7, desc, ha='center', va='center', fontsize=8.8, color="#1E293B", linespacing=1.25)

    # Horizontal progression arrows
    for i in range(len(phases) - 1):
        x_from = phases[i][2] + 1.62
        x_to = phases[i+1][2] - 0.02
        ax.annotate("", xy=(x_to, 4.15), xytext=(x_from, 4.15),
                    arrowprops=dict(arrowstyle="->", color="#1E3A8A", lw=2.2, mutation_scale=14))

    # Milestones banner below with LARGE, READABLE METRICS
    m_box = patches.FancyBboxPatch((0.3, 0.35), 12.4, 2.4, boxstyle="round,pad=0.12", facecolor="#F8FAFC", edgecolor="#1E3A8A", linewidth=2.0)
    ax.add_patch(m_box)
    ax.text(6.5, 2.35, "VERIFIED QUANTITATIVE MILESTONES & ACCEPTANCE CRITERIA", ha='center', va='center',
            fontsize=12, fontweight='bold', color="#1E3A8A")

    criteria_left = [
        "• Static Distance Accuracy: MAE ≤ ±0.5 cm, RMSE ≤ ±0.75 cm (Current Bench: RMSE = ±0.02 cm)",
        "• Tilt Compensation Efficacy: Residual error ≤ ±0.5 cm across 0° to 20° dynamic pitch/roll angles",
        "• Vibration Damping Attenuation: ≥ 18 dB attenuation across 150--250 Hz motor harmonics via silicone mounts"
    ]
    criteria_right = [
        "• Smart 4WD Car Odometry Drift: ≤ 1.0 cm linear drift per 5.0 m traverse at 5.0 cm/s creeping velocity",
        "• Defect Segmentation Performance: Precision ≥ 90%, Recall ≥ 85% for spalls ≥ 3.5 cm and cracks ≥ 1.5 cm",
        "• Mission Endurance: Continuous UAV flight ≥ 14.0 mins; Continuous Smart 4WD Ground Car survey ≥ 2.5 hours"
    ]

    for i, c in enumerate(criteria_left):
        ax.text(0.6, 1.8 - i*0.5, c, ha='left', va='center', fontsize=9.5, fontweight='bold', color="#1E293B")

    for i, c in enumerate(criteria_right):
        ax.text(6.6, 1.8 - i*0.5, c, ha='left', va='center', fontsize=9.5, fontweight='bold', color="#1E293B")

    plt.tight_layout()
    out_path = os.path.join(assets_dir, "flowchart_testing_roadmap.png")
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Generated {out_path}")

if __name__ == "__main__":
    create_flowchart_system_architecture()
    create_flowchart_aerial_acquisition()
    create_flowchart_ground_analytics()
    create_flowchart_power_wiring()
    create_flowchart_testing_roadmap()
    print("All enhanced flowcharts generated successfully!")
