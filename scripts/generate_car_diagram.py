import os
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.stdout.reconfigure(encoding='utf-8')
assets_dir = r"c:\Users\nisar\OneDrive\Desktop\TF_LUNA_PROJECT\reports\assets"
os.makedirs(assets_dir, exist_ok=True)

plt.rcParams['font.sans-serif'] = 'Arial', 'DejaVu Sans', 'Helvetica'
plt.rcParams['font.family'] = 'sans-serif'

def create_car_architecture_diagram():
    fig, ax = plt.subplots(figsize=(13, 5.8), dpi=300)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 5.8)
    ax.axis('off')

    # Title Banner
    t_rect = patches.FancyBboxPatch((0.2, 5.0), 12.6, 0.65, boxstyle="round,pad=0.1", facecolor="#0F172A", edgecolor="#1E3A8A", linewidth=2.0)
    ax.add_patch(t_rect)
    ax.text(6.5, 5.32, "CONTINGENCY PLATFORM: SMART 4WD ROBOTIC CAR SCANNING ARCHITECTURE & ODOMETRY",
            ha='center', va='center', fontsize=12, fontweight='bold', color="#FFFFFF")

    # 3 Main Pillars
    # Pillar 1: Why Car vs Drone
    p1 = patches.FancyBboxPatch((0.3, 0.35), 3.9, 4.45, boxstyle="round,pad=0.12", facecolor="#F8FAFC", edgecolor="#64748B", linewidth=1.8)
    ax.add_patch(p1)
    ax.text(2.25, 4.45, "1. WHY THE 4WD ROBOTIC CAR?", ha='center', va='center', fontsize=11, fontweight='bold', color="#0F172A")
    why_text = (
        "• Indoor Flight Restrictions:\n"
        "  Drones restricted in indoor corridors,\n"
        "  classrooms, and GPS-denied basements.\n\n"
        "• Eliminates Prop-Wash Turbulence:\n"
        "  Drones flying <1.5m from walls experience\n"
        "  severe wall aerodynamic suction forces.\n"
        "  The car operates with zero prop-wash risk.\n\n"
        "• Eliminates Hand-Sliding Jitter:\n"
        "  Manual sliding caused ~2--3 cm noise.\n"
        "  Car moves at exact constant speed (5 cm/s).\n\n"
        "• Extended Survey Duration:\n"
        "  Drone flight = 14--16 mins per LiPo battery.\n"
        "  Ground car runs 2--3 hours continuously."
    )
    ax.text(0.55, 2.4, why_text, ha='left', va='center', fontsize=9.2, color="#334155", linespacing=1.35)

    # Pillar 2: Hardware Setup on Car
    p2 = patches.FancyBboxPatch((4.5, 0.35), 3.9, 4.45, boxstyle="round,pad=0.12", facecolor="#EFF6FF", edgecolor="#2563EB", linewidth=1.8)
    ax.add_patch(p2)
    ax.text(6.45, 4.45, "2. HARDWARE SETUP ON CAR", ha='center', va='center', fontsize=11, fontweight='bold', color="#1E40AF")
    hw_text = (
        "• 4WD Chassis & Drive Train:\n"
        "  4x DC gear motors (1:48 gear ratio)\n"
        "  with 65mm high-traction rubber wheels.\n\n"
        "• Dual Optical Speed Encoders:\n"
        "  20-slot slotted photo-interrupter disks\n"
        "  mounted on rear wheels for exact odometry.\n\n"
        "• L298N / TB6612FNG Motor Driver:\n"
        "  Dual H-bridge driven by ESP32 PWM pins\n"
        "  for closed-loop PID constant speed (5 cm/s).\n\n"
        "• Telescoping Sensor Mast:\n"
        "  Aluminum mast holds TF-Luna / YDLIDAR X2\n"
        "  at adjustable heights (0.2m to 2.2m elevation)."
    )
    ax.text(4.75, 2.4, hw_text, ha='left', va='center', fontsize=9.2, color="#1E3A8A", linespacing=1.35)

    # Pillar 3: Workflow & Formulas
    p3 = patches.FancyBboxPatch((8.7, 0.35), 4.0, 4.45, boxstyle="round,pad=0.12", facecolor="#ECFDF5", edgecolor="#059669", linewidth=1.8)
    ax.add_patch(p3)
    ax.text(10.7, 4.45, "3. SCANNING & ODOMETRY WORKFLOW", ha='center', va='center', fontsize=11, fontweight='bold', color="#065F46")
    workflow_text = (
        "• Datum Initialization:\n"
        "  Origin defined at wall start: P(0) = (0, 0, Z0).\n\n"
        "• Linear Displacement per Tick:\n"
        "  ΔX = N_ticks · [π · D_wheel / 20 slots]\n"
        "  (where D=6.5 cm  -->  ~1.02 mm / tick resolution).\n\n"
        "• Point Coordinate Formulation:\n"
        "  X_point = X_encoder(t)  [integrated distance]\n"
        "  Y_point = d_meas(t) · cos(θ_tilt)  [standoff]\n"
        "  Z_point = Z_mast  [elevation band]\n\n"
        "• Multi-Height Raster Scanning:\n"
        "  Step mast height in 10--20 cm increments\n"
        "  to reconstruct dense 3D digital twin cloud."
    )
    ax.text(8.95, 2.4, workflow_text, ha='left', va='center', fontsize=9.2, color="#064E3B", linespacing=1.35)

    plt.tight_layout()
    out_path = os.path.join(assets_dir, "flowchart_smart_car_operation.png")
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Generated {out_path}")

if __name__ == "__main__":
    create_car_architecture_diagram()
