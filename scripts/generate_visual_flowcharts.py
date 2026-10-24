import os
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.stdout.reconfigure(encoding='utf-8')

assets_dir = r"c:\Users\nisar\OneDrive\Desktop\TF_LUNA_PROJECT\reports\assets"
os.makedirs(assets_dir, exist_ok=True)

# -------------------------------------------------------------
# FLOWCHART 1: COMPLETE END-TO-END SYSTEM ARCHITECTURE
# -------------------------------------------------------------
def create_flowchart_system_architecture():
    fig, ax = plt.subplots(figsize=(12, 4.5), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4.5)
    ax.axis('off')

    # Background column bands
    cols = [
        ("TARGET STRUCTURE", 0.2, 2.2, "#F1F5F9", "#0F172A"),
        ("EMBEDDED SENSING", 2.6, 2.2, "#EFF6FF", "#1E3A8A"),
        ("TELEMETRY & LOG", 5.0, 2.0, "#F0FDFA", "#0D9488"),
        ("GROUND ANALYTICS", 7.2, 2.3, "#FEF3C7", "#D97706"),
        ("3D TWIN & REPORT", 9.7, 2.1, "#ECFDF5", "#059669")
    ]

    for title, x, w, bg, fg in cols:
        rect = patches.FancyBboxPatch((x, 0.2), w, 4.1, boxstyle="round,pad=0.1",
                                      facecolor=bg, edgecolor=fg, linewidth=1.5, alpha=0.9)
        ax.add_patch(rect)
        ax.text(x + w/2, 4.05, title, ha='center', va='center', fontsize=9, fontweight='bold', color=fg)

    # Sub-boxes inside columns
    # Col 1: Target
    b1 = patches.FancyBboxPatch((0.4, 2.2), 1.8, 1.4, boxstyle="round,pad=0.08", facecolor="#FFFFFF", edgecolor="#64748B", linewidth=1.2)
    ax.add_patch(b1)
    ax.text(1.3, 2.9, "Concrete Facade\nBridge Piers / Columns\nRoom Envelope", ha='center', va='center', fontsize=7.5, color="#1E293B")

    b1_def = patches.FancyBboxPatch((0.4, 0.5), 1.8, 1.4, boxstyle="round,pad=0.08", facecolor="#FEE2E2", edgecolor="#E11D48", linewidth=1.2)
    ax.add_patch(b1_def)
    ax.text(1.3, 1.2, "Surface Defects:\n• Spall Cavity (±3.5cm)\n• Bulge / Buckle (-3.5cm)\n• Cracks / Mortar gaps", ha='center', va='center', fontsize=7.5, color="#991B1B", fontweight='bold')

    # Col 2: Sensing
    b2_tf = patches.FancyBboxPatch((2.8, 2.7), 1.8, 1.0, boxstyle="round,pad=0.08", facecolor="#DBEAFE", edgecolor="#2563EB", linewidth=1.2)
    ax.add_patch(b2_tf)
    ax.text(3.7, 3.2, "TF-Luna 850nm dToF\n(1D Point, 100 Hz, <5g)", ha='center', va='center', fontsize=7.5, color="#1E40AF", fontweight='bold')

    b2_yd = patches.FancyBboxPatch((2.8, 1.55), 1.8, 1.0, boxstyle="round,pad=0.08", facecolor="#E0E7FF", edgecolor="#4F46E5", linewidth=1.2, linestyle='--')
    ax.add_patch(b2_yd)
    ax.text(3.7, 2.05, "YDLIDAR X2 (Planned)\n(2D 360°, 3kHz, 7 Hz)", ha='center', va='center', fontsize=7.5, color="#3730A3", fontweight='bold')

    b2_mcu = patches.FancyBboxPatch((2.8, 0.4), 1.8, 1.0, boxstyle="round,pad=0.08", facecolor="#FFFFFF", edgecolor="#0284C7", linewidth=1.2)
    ax.add_patch(b2_mcu)
    ax.text(3.7, 0.9, "ESP32 MCU + DFRobot Tilt\nChecksum + Calibration:\ny = 1.0228x + 3.20 cm", ha='center', va='center', fontsize=7.2, color="#0369A1")

    # Col 3: Telemetry
    b3_uart = patches.FancyBboxPatch((5.15, 2.4), 1.7, 1.2, boxstyle="round,pad=0.08", facecolor="#FFFFFF", edgecolor="#0D9488", linewidth=1.2)
    ax.add_patch(b3_uart)
    ax.text(6.0, 3.0, "Active Telemetry:\nUSB-UART 115200\nCSV Timestamp Stream", ha='center', va='center', fontsize=7.5, color="#0F766E")

    b3_udp = patches.FancyBboxPatch((5.15, 0.7), 1.7, 1.2, boxstyle="round,pad=0.08", facecolor="#CCFBF1", edgecolor="#0F766E", linewidth=1.2, linestyle='--')
    ax.add_patch(b3_udp)
    ax.text(6.0, 1.3, "Planned Airborne:\nWi-Fi 802.11 UDP\nPort 5005 Broadcast", ha='center', va='center', fontsize=7.5, color="#115E59", fontweight='bold')

    # Col 4: Ground Analytics
    b4_base = patches.FancyBboxPatch((7.35, 2.4), 2.0, 1.2, boxstyle="round,pad=0.08", facecolor="#FFFFFF", edgecolor="#D97706", linewidth=1.2)
    ax.add_patch(b4_base)
    ax.text(8.35, 3.0, "Rolling Baseline & Residual:\nΔd = d_meas - d_ref\nNoise Floor Filter (±2.5cm)", ha='center', va='center', fontsize=7.2, color="#92400E")

    b4_rule = patches.FancyBboxPatch((7.35, 0.7), 2.0, 1.2, boxstyle="round,pad=0.08", facecolor="#FFFBEB", edgecolor="#B45309", linewidth=1.2)
    ax.add_patch(b4_rule)
    ax.text(8.35, 1.3, "Defect Classifier Rules:\n• Δd ≥ +3.5cm → Spall Cavity\n• Δd ≤ -3.5cm → Bulge\n• |Δd| ≥ 1.5cm → Crack Peak", ha='center', va='center', fontsize=7.0, color="#78350F", fontweight='bold')

    # Col 5: 3D Twin & Report
    b5_ply = patches.FancyBboxPatch((9.85, 2.4), 1.8, 1.2, boxstyle="round,pad=0.08", facecolor="#FFFFFF", edgecolor="#059669", linewidth=1.2)
    ax.add_patch(b5_ply)
    ax.text(10.75, 3.0, "3D Room Mesh (.PLY)\n9,969 Points Labeled:\nAlmari (+65cm) / Gate (-60cm)", ha='center', va='center', fontsize=7.0, color="#065F46", fontweight='bold')

    b5_ui = patches.FancyBboxPatch((9.85, 0.7), 1.8, 1.2, boxstyle="round,pad=0.08", facecolor="#D1FAE5", edgecolor="#047857", linewidth=1.2)
    ax.add_patch(b5_ui)
    ax.text(10.75, 1.3, "PLY Forge WebGL Engine\n5-Tab Operations UI\nPDF Audit Report", ha='center', va='center', fontsize=7.2, color="#064E3B")

    # Connective Arrows
    arrow_props = dict(arrowstyle="->", color="#1E3A8A", lw=2, mutation_scale=15)
    ax.annotate("", xy=(2.7, 3.2), xytext=(2.3, 3.2), arrowprops=arrow_props)
    ax.annotate("", xy=(2.7, 2.05), xytext=(2.3, 2.05), arrowprops=arrow_props)
    ax.annotate("", xy=(5.05, 3.0), xytext=(4.7, 3.0), arrowprops=arrow_props)
    ax.annotate("", xy=(5.05, 1.3), xytext=(4.7, 1.1), arrowprops=arrow_props)
    ax.annotate("", xy=(7.25, 3.0), xytext=(6.9, 3.0), arrowprops=arrow_props)
    ax.annotate("", xy=(9.75, 3.0), xytext=(9.4, 3.0), arrowprops=arrow_props)
    ax.annotate("", xy=(9.75, 1.3), xytext=(9.4, 1.3), arrowprops=arrow_props)

    plt.tight_layout()
    out_path = os.path.join(assets_dir, "flowchart_system_architecture.png")
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Generated {out_path}")

# -------------------------------------------------------------
# FLOWCHART 2: AERIAL ACQUISITION STATE MACHINE (TEAM 1)
# -------------------------------------------------------------
def create_flowchart_aerial_acquisition():
    fig, ax = plt.subplots(figsize=(10, 4.2), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.2)
    ax.axis('off')

    # Step boxes
    steps = [
        ("1. Boot & Init", "ESP32 GPIOs, UART1,\nUART2, I2C / Tilt pin", 0.5, 2.6, "#F1F5F9", "#0F172A"),
        ("2. Frame Sync", "Scan UART buffer for\n0x59 0x59 preamble", 2.3, 2.6, "#DBEAFE", "#1E40AF"),
        ("3. Ingest Bytes", "Read 9 bytes:\nDist_L/H, Amp_L/H, Temp", 4.1, 2.6, "#DBEAFE", "#1E40AF"),
        ("4. Checksum Check", "Is (Σ B0..B7)&0xFF\n== Byte 8?", 6.0, 2.6, "#FEF3C7", "#B45309"),
        ("5. Drop & Resync", "Corrupt frame discarded;\nflush buffer", 6.0, 0.6, "#FEE2E2", "#DC2626"),
        ("6. Two-Point Cal", "y = 1.0228·x + 3.20cm\n(RMSE ±0.02 cm)", 8.0, 2.6, "#ECFDF5", "#059669"),
        ("7. Tilt Compensation", "Sample pitch/roll θ:\nd_true = d_cal · cos(θ)", 8.0, 1.2, "#D1FAE5", "#047857"),
        ("8. Filter & Broadcast", "Median filter (N=5);\nUDP socket / USB CSV", 4.1, 0.6, "#CCFBF1", "#0D9488")
    ]

    for title, desc, x, y, bg, fg in steps:
        rect = patches.FancyBboxPatch((x, y), 1.6, 1.15, boxstyle="round,pad=0.08", facecolor=bg, edgecolor=fg, linewidth=1.4)
        ax.add_patch(rect)
        ax.text(x + 0.8, y + 0.85, title, ha='center', va='center', fontsize=7.5, fontweight='bold', color=fg)
        ax.text(x + 0.8, y + 0.38, desc, ha='center', va='center', fontsize=6.5, color="#1E293B")

    # Arrows
    arr = dict(arrowstyle="->", color="#1E3A8A", lw=1.8, mutation_scale=12)
    ax.annotate("", xy=(2.25, 3.17), xytext=(2.15, 3.17), arrowprops=arr)
    ax.annotate("", xy=(4.05, 3.17), xytext=(3.95, 3.17), arrowprops=arr)
    ax.annotate("", xy=(5.95, 3.17), xytext=(5.75, 3.17), arrowprops=arr)
    ax.annotate("", xy=(7.95, 3.17), xytext=(7.65, 3.17), arrowprops=arr)
    ax.text(7.8, 3.3, "VALID", fontsize=6.5, fontweight='bold', color="#059669")

    # Checksum failure arrow
    ax.annotate("", xy=(6.8, 1.8), xytext=(6.8, 2.55), arrowprops=dict(arrowstyle="->", color="#DC2626", lw=1.8, mutation_scale=12))
    ax.text(6.9, 2.15, "FAIL", fontsize=6.5, fontweight='bold', color="#DC2626")
    ax.annotate("", xy=(3.1, 2.55), xytext=(5.95, 1.17), arrowprops=dict(arrowstyle="->", color="#DC2626", lw=1.2, linestyle=':', connectionstyle="arc3,rad=0.3"))

    # Cal to Tilt, Tilt to Filter
    ax.annotate("", xy=(8.8, 2.4), xytext=(8.8, 2.55), arrowprops=arr)
    ax.annotate("", xy=(7.95, 1.17), xytext=(5.75, 1.17), arrowprops=arr)
    ax.annotate("", xy=(4.1, 1.8), xytext=(4.1, 2.55), arrowprops=dict(arrowstyle="->", color="#059669", lw=1.5, linestyle='--', connectionstyle="arc3,rad=-0.2"))

    plt.tight_layout()
    out_path = os.path.join(assets_dir, "flowchart_aerial_acquisition.png")
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Generated {out_path}")

# -------------------------------------------------------------
# FLOWCHART 3: GROUND ANALYTICS & DEFECT DECISION TREE
# -------------------------------------------------------------
def create_flowchart_ground_analytics():
    fig, ax = plt.subplots(figsize=(11, 4.6), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4.6)
    ax.axis('off')

    # Start: Ingestion
    p1 = patches.FancyBboxPatch((0.4, 2.7), 1.9, 1.2, boxstyle="round,pad=0.08", facecolor="#EFF6FF", edgecolor="#2563EB", linewidth=1.4)
    ax.add_patch(p1)
    ax.text(1.35, 3.55, "Data Ingestion", ha='center', va='center', fontsize=8, fontweight='bold', color="#1E40AF")
    ax.text(1.35, 3.05, "Receive d_true(t), θ, Amp\nfrom USB / UDP stream", ha='center', va='center', fontsize=7, color="#1E293B")

    # Step 2: Baseline
    p2 = patches.FancyBboxPatch((2.7, 2.7), 2.1, 1.2, boxstyle="round,pad=0.08", facecolor="#F0FDFA", edgecolor="#0D9488", linewidth=1.4)
    ax.add_patch(p2)
    ax.text(3.75, 3.55, "Baseline Tracking", ha='center', va='center', fontsize=8, fontweight='bold', color="#0F766E")
    ax.text(3.75, 3.05, "Calculate rolling window mean\nd_ref = Mean(window N=15)\nΔd = d_meas - d_ref", ha='center', va='center', fontsize=6.8, color="#1E293B")

    # Decision Diamond (represented as polygon or styled box)
    p3 = patches.FancyBboxPatch((5.2, 2.5), 2.2, 1.6, boxstyle="round,pad=0.1", facecolor="#FEF3C7", edgecolor="#B45309", linewidth=1.5)
    ax.add_patch(p3)
    ax.text(6.3, 3.75, "Defect Threshold Rules", ha='center', va='center', fontsize=8, fontweight='bold', color="#78350F")
    ax.text(6.3, 3.1, "Evaluate Residual Δd:\n1. Is Δd ≥ +3.5 cm?\n2. Is Δd ≤ -3.5 cm?\n3. Is |Δd| ≥ 1.5 cm vs nbrs?", ha='center', va='center', fontsize=6.8, color="#1E293B")

    # Outcomes: Cavity, Bulge, Crack, Normal
    outcomes = [
        ("Spall Cavity (Orange)", "Δd ≥ +3.5cm\nRecessed into wall surface", 8.2, 3.4, "#FFEDD5", "#C2410C"),
        ("Structural Bulge (Orange)", "Δd ≤ -3.5cm\nProtruding outward (Buckle)", 8.2, 2.2, "#FFEDD5", "#C2410C"),
        ("Crack Indication (Gold)", "|Δd| ≥ 1.5cm vs neighbors\nIsolated depth spike", 8.2, 1.0, "#FEF9C3", "#A16207"),
        ("Uniform Wall (Cyan)", "|Δd| < 2.5cm\nWithin normal structural band", 5.2, 0.4, "#CFFAFE", "#0891B2")
    ]

    for title, desc, x, y, bg, fg in outcomes:
        rect = patches.FancyBboxPatch((x, y), 2.4, 0.95, boxstyle="round,pad=0.08", facecolor=bg, edgecolor=fg, linewidth=1.3)
        ax.add_patch(rect)
        ax.text(x + 1.2, y + 0.68, title, ha='center', va='center', fontsize=7.2, fontweight='bold', color=fg)
        ax.text(x + 1.2, y + 0.3, desc, ha='center', va='center', fontsize=6.3, color="#1E293B")

    # Connectors
    arr = dict(arrowstyle="->", color="#1E3A8A", lw=1.8, mutation_scale=12)
    ax.annotate("", xy=(2.65, 3.3), xytext=(2.35, 3.3), arrowprops=arr)
    ax.annotate("", xy=(5.15, 3.3), xytext=(4.85, 3.3), arrowprops=arr)

    # Branches to outcomes
    ax.annotate("", xy=(8.15, 3.85), xytext=(7.45, 3.5), arrowprops=dict(arrowstyle="->", color="#C2410C", lw=1.5, mutation_scale=10))
    ax.annotate("", xy=(8.15, 2.65), xytext=(7.45, 3.3), arrowprops=dict(arrowstyle="->", color="#C2410C", lw=1.5, mutation_scale=10))
    ax.annotate("", xy=(8.15, 1.45), xytext=(7.45, 3.0), arrowprops=dict(arrowstyle="->", color="#A16207", lw=1.5, mutation_scale=10))
    ax.annotate("", xy=(6.3, 1.4), xytext=(6.3, 2.45), arrowprops=dict(arrowstyle="->", color="#0891B2", lw=1.5, mutation_scale=10))

    plt.tight_layout()
    out_path = os.path.join(assets_dir, "flowchart_ground_analytics.png")
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Generated {out_path}")

# -------------------------------------------------------------
# FLOWCHART 4: ELECTRICAL & POWER DISTRIBUTION
# -------------------------------------------------------------
def create_flowchart_power_wiring():
    fig, ax = plt.subplots(figsize=(10, 4.2), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.2)
    ax.axis('off')

    # Battery
    p_bat = patches.FancyBboxPatch((0.4, 2.3), 1.9, 1.4, boxstyle="round,pad=0.08", facecolor="#FEE2E2", edgecolor="#DC2626", linewidth=1.5)
    ax.add_patch(p_bat)
    ax.text(1.35, 3.2, "3S LiPo Battery", ha='center', va='center', fontsize=8.5, fontweight='bold', color="#991B1B")
    ax.text(1.35, 2.65, "11.1V Nominal (12.6V Max)\n4200 mAh, 35C Discharge\nXT60 Connector", ha='center', va='center', fontsize=6.8, color="#1E293B")

    # PDB
    p_pdb = patches.FancyBboxPatch((2.8, 2.3), 1.8, 1.4, boxstyle="round,pad=0.08", facecolor="#FEF3C7", edgecolor="#D97706", linewidth=1.4)
    ax.add_patch(p_pdb)
    ax.text(3.7, 3.2, "Power Dist. Board", ha='center', va='center', fontsize=8, fontweight='bold', color="#92400E")
    ax.text(3.7, 2.65, "11.1V High-Current Bus\n4x ESC Motor Feeds\nAuxiliary 11.1V Tap", ha='center', va='center', fontsize=6.8, color="#1E293B")

    # High voltage to Motors
    p_mot = patches.FancyBboxPatch((5.2, 2.7), 2.1, 1.2, boxstyle="round,pad=0.08", facecolor="#F1F5F9", edgecolor="#475569", linewidth=1.2)
    ax.add_patch(p_mot)
    ax.text(6.25, 3.55, "4x 30A ESCs & 2212 Motors", ha='center', va='center', fontsize=7.5, fontweight='bold', color="#1E293B")
    ax.text(6.25, 3.05, "11.1V Direct LiPo Power\nControlled by Pixhawk PWM\nAUW Thrust = 3,400g", ha='center', va='center', fontsize=6.5, color="#475569")

    # UBEC Step-Down
    p_bec = patches.FancyBboxPatch((2.8, 0.4), 1.8, 1.3, boxstyle="round,pad=0.08", facecolor="#DCFCE7", edgecolor="#16A34A", linewidth=1.4)
    ax.add_patch(p_bec)
    ax.text(3.7, 1.25, "5V 5A UBEC Regulator", ha='center', va='center', fontsize=8, fontweight='bold', color="#15803D")
    ax.text(3.7, 0.75, "Steps 11.1V down to 5.0V\nClean Ripple-Free Bus\nReverse-Polarity Protected", ha='center', va='center', fontsize=6.5, color="#1E293B")

    # Sensors on 5V Bus
    p_sens = patches.FancyBboxPatch((5.2, 0.4), 2.1, 1.8, boxstyle="round,pad=0.08", facecolor="#EFF6FF", edgecolor="#2563EB", linewidth=1.4)
    ax.add_patch(p_sens)
    ax.text(6.25, 1.85, "Regulated 5.0V Avionics Bus", ha='center', va='center', fontsize=7.5, fontweight='bold', color="#1E40AF")
    ax.text(6.25, 1.15, "• TF-Luna ToF (70mA)\n• YDLIDAR X2 Core (500mA)\n• ESP32 MCU (Vin pin, 200mA)\n• DFRobot Tilt Sensor (10mA)", ha='center', va='center', fontsize=6.8, color="#1E293B")

    # Ground Station Link
    p_gnd = patches.FancyBboxPatch((7.8, 1.0), 1.8, 1.8, boxstyle="round,pad=0.08", facecolor="#FAF5FF", edgecolor="#9333EA", linewidth=1.4)
    ax.add_patch(p_gnd)
    ax.text(8.7, 2.3, "Ground Base Station", ha='center', va='center', fontsize=8, fontweight='bold', color="#7E22CE")
    ax.text(8.7, 1.6, "Wi-Fi UDP Telemetry\n115200 Baud USB Logging\nStreamlit Dashboard\nPLY Forge 3D Mesh Engine", ha='center', va='center', fontsize=6.5, color="#1E293B")

    # Wire arrows
    ax.annotate("", xy=(2.75, 3.0), xytext=(2.35, 3.0), arrowprops=dict(arrowstyle="->", color="#DC2626", lw=2, mutation_scale=12))
    ax.text(2.55, 3.15, "11.1V", fontsize=6.5, fontweight='bold', color="#DC2626")

    ax.annotate("", xy=(5.15, 3.3), xytext=(4.65, 3.3), arrowprops=dict(arrowstyle="->", color="#DC2626", lw=2, mutation_scale=12))
    ax.text(4.9, 3.45, "11.1V", fontsize=6.5, fontweight='bold', color="#DC2626")

    ax.annotate("", xy=(3.7, 1.75), xytext=(3.7, 2.25), arrowprops=dict(arrowstyle="->", color="#DC2626", lw=1.8, mutation_scale=12))
    ax.text(3.8, 2.0, "11.1V Tap", fontsize=6.5, color="#DC2626")

    ax.annotate("", xy=(5.15, 1.0), xytext=(4.65, 1.0), arrowprops=dict(arrowstyle="->", color="#16A34A", lw=2, mutation_scale=12))
    ax.text(4.9, 1.15, "5.0V", fontsize=7, fontweight='bold', color="#16A34A")

    ax.annotate("", xy=(7.75, 1.9), xytext=(7.35, 1.9), arrowprops=dict(arrowstyle="->", color="#9333EA", lw=1.8, linestyle='--', mutation_scale=12))
    ax.text(7.55, 2.1, "UDP", fontsize=7, fontweight='bold', color="#9333EA")

    plt.tight_layout()
    out_path = os.path.join(assets_dir, "flowchart_power_wiring.png")
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Generated {out_path}")

# -------------------------------------------------------------
# FLOWCHART 5: PHASED TESTING & IMPLEMENTATION ROADMAP
# -------------------------------------------------------------
def create_flowchart_testing_roadmap():
    fig, ax = plt.subplots(figsize=(11, 4.2), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4.2)
    ax.axis('off')

    phases = [
        ("Phase 1: Design", "CAD Mounts\nPin Schematics\nBudget Sign-off", 0.3, 2.4, "#F1F5F9", "#0F172A"),
        ("Phase 2: Bench Test", "YDLIDAR X2 UART\nTilt Sensor Int\n5V UBEC Load", 1.8, 2.4, "#DBEAFE", "#1E40AF"),
        ("Phase 3: Sensor Fusion", "Tilt Compensation\nTwo-point Calibration\nFreeRTOS Driver", 3.3, 2.4, "#FEF3C7", "#D97706"),
        ("Phase 4: Airframe", "F450 Quadcopter\nSilicone Isolator\nPixhawk Config", 4.8, 2.4, "#E0E7FF", "#4338CA"),
        ("Phase 5: Ground UI", "PLY Forge WebGL\nUDP Point Buffer\nAutomated Audit", 6.3, 2.4, "#F0FDFA", "#0D9488"),
        ("Phase 6: Flight Trials", "Tethered Hover\nFacade Calibration\nSpall Verification", 7.8, 2.4, "#FCE7F3", "#BE185D"),
        ("Phase 7: Review & Demo", "Faculty Demo\nLongitudinal Baseline\nFull Report Archive", 9.3, 2.4, "#DCFCE7", "#15803D")
    ]

    for title, desc, x, y, bg, fg in phases:
        rect = patches.FancyBboxPatch((x, y), 1.35, 1.45, boxstyle="round,pad=0.08", facecolor=bg, edgecolor=fg, linewidth=1.4)
        ax.add_patch(rect)
        ax.text(x + 0.67, y + 1.15, title, ha='center', va='center', fontsize=6.8, fontweight='bold', color=fg)
        ax.text(x + 0.67, y + 0.55, desc, ha='center', va='center', fontsize=6.0, color="#1E293B")

    # Horizontal progression arrows
    for i in range(len(phases) - 1):
        x_from = phases[i][2] + 1.37
        x_to = phases[i+1][2] - 0.03
        ax.annotate("", xy=(x_to, 3.12), xytext=(x_from, 3.12),
                    arrowprops=dict(arrowstyle="->", color="#1E3A8A", lw=2, mutation_scale=12))

    # Milestones banner below
    m_box = patches.FancyBboxPatch((0.3, 0.4), 10.35, 1.4, boxstyle="round,pad=0.08", facecolor="#F8FAFC", edgecolor="#CBD5E1", linewidth=1.2)
    ax.add_patch(m_box)
    ax.text(5.5, 1.45, "VERIFIED MILESTONES & SCIENTIFIC ACCEPTANCE CRITERIA", ha='center', va='center', fontsize=8, fontweight='bold', color="#0F172A")
    ax.text(5.5, 0.85, "• Static Distance: MAE ≤ ±0.5 cm, RMSE ≤ ±0.75 cm (Current Bench: RMSE = ±0.02 cm)   |   • Tilt Residual: ≤ ±1.0 cm (0°–20°)\n• Motor Damping: ≥ 18 dB attenuation (150–250 Hz band)   |   • Telemetry: Packet Drop ≤ 1.0%, Latency ≤ 25 ms\n• Defect Sensitivity: Precision ≥ 90%, Recall ≥ 85% for spalls ≥ 3.5 cm   |   • Hover Flight Time: ≥ 14.0 minutes under payload", ha='center', va='center', fontsize=6.5, color="#334155")

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
