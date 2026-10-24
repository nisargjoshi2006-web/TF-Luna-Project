import os
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.stdout.reconfigure(encoding='utf-8')
assets_dir = r"c:\Users\nisar\OneDrive\Desktop\TF_LUNA_PROJECT\reports\assets"
os.makedirs(assets_dir, exist_ok=True)

def create_car_architecture_diagram():
    fig, ax = plt.subplots(figsize=(12, 5.2), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5.2)
    ax.axis('off')

    # Title Banner
    t_rect = patches.FancyBboxPatch((0.2, 4.5), 11.6, 0.6, boxstyle="round,pad=0.08", facecolor="#0F172A", edgecolor="#1E3A8A", linewidth=1.5)
    ax.add_patch(t_rect)
    ax.text(6.0, 4.8, "CONTINGENCY PLATFORM: SMART 4WD ROBOTIC CAR SCANNING ARCHITECTURE & ODOMETRY", ha='center', va='center', fontsize=9.5, fontweight='bold', color="#FFFFFF")

    # 3 Main Pillars
    # Pillar 1: Why Car vs Drone
    p1 = patches.FancyBboxPatch((0.3, 0.4), 3.6, 3.9, boxstyle="round,pad=0.1", facecolor="#F8FAFC", edgecolor="#64748B", linewidth=1.4)
    ax.add_patch(p1)
    ax.text(2.1, 4.05, "1. WHY THE 4WD ROBOTIC CAR?", ha='center', va='center', fontsize=8.5, fontweight='bold', color="#0F172A")
    why_text = (
        "• Indoor Flight Restrictions:\n"
        "  Drones restricted in indoor corridors,\n"
        "  classrooms, and GPS-denied basements.\n\n"
        "• Eliminates Prop-Wash Turbulence:\n"
        "  Drones flying <1.5m from walls experience\n"
        "  severe ground/wall aerodynamic suction.\n"
        "  The car provides zero aerodynamic suction.\n\n"
        "• Eliminates Hand-Sliding Jitter:\n"
        "  Manual sliding caused ~2–3 cm jitter.\n"
        "  Car moves at exact constant speed (5 cm/s).\n\n"
        "• Unlimited Scan Duration:\n"
        "  Drone flight = 14–18 mins per LiPo battery.\n"
        "  Ground car runs 2–3 hours on 12V Li-ion pack."
    )
    ax.text(0.5, 2.2, why_text, ha='left', va='center', fontsize=7.2, color="#334155", linespacing=1.4)

    # Pillar 2: Hardware Setup on Car
    p2 = patches.FancyBboxPatch((4.2, 0.4), 3.6, 3.9, boxstyle="round,pad=0.1", facecolor="#EFF6FF", edgecolor="#2563EB", linewidth=1.4)
    ax.add_patch(p2)
    ax.text(6.0, 4.05, "2. CAR HARDWARE CONFIGURATION", ha='center', va='center', fontsize=8.5, fontweight='bold', color="#1E40AF")
    hw_text = (
        "• 4WD Robotic Chassis:\n"
        "  Four high-torque DC gear motors (1:48)\n"
        "  with dual-plate acrylic/aluminum deck.\n\n"
        "• Dual Optical Wheel Encoders:\n"
        "  20-slot slotted photo-interrupter disks\n"
        "  measuring exact linear distance traveled: ΔX.\n\n"
        "• Motor Driver & MCU:\n"
        "  L298N / TB6612FNG Dual H-Bridge\n"
        "  PWM-driven by ESP32 for cruise control.\n\n"
        "• Telescoping Sensor Mast:\n"
        "  Rigid vertical aluminum mast holding TF-Luna\n"
        "  and YDLIDAR X2 at fixed heights (0.5m–2.0m)."
    )
    ax.text(4.4, 2.2, hw_text, ha='left', va='center', fontsize=7.2, color="#1E3A8A", linespacing=1.4)

    # Pillar 3: Mathematical Mapping & Scan Workflow
    p3 = patches.FancyBboxPatch((8.1, 0.4), 3.6, 3.9, boxstyle="round,pad=0.1", facecolor="#ECFDF5", edgecolor="#059669", linewidth=1.4)
    ax.add_patch(p3)
    ax.text(9.9, 4.05, "3. SCANNING & ODOMETRY WORKFLOW", ha='center', va='center', fontsize=8.5, fontweight='bold', color="#065F46")
    math_text = (
        "• Origin Benchmark:\n"
        "  Car initializes at corner datum: (0, 0, Z0).\n\n"
        "• Dynamic Encoder Trajectory:\n"
        "  X(t) = N_ticks · (π · D_wheel / 20 slots)\n"
        "  Tracks position along the wall continuously.\n\n"
        "• Precise Wall Point Cloud:\n"
        "  X = X_encoder(t)\n"
        "  Y = d_meas(t) · cos(θ_tilt)  [Distance to wall]\n"
        "  Z = Z_mast (or stepped via vertical lift)\n\n"
        "• Result: Zero-jitter, millimeter-precision\n"
        "  2D facade profile & watertight 3D mesh!"
    )
    ax.text(8.3, 2.2, math_text, ha='left', va='center', fontsize=7.2, color="#064E3B", linespacing=1.4)

    # Inter-Pillar Connective Arrows
    ax.annotate("", xy=(4.1, 2.3), xytext=(3.95, 2.3), arrowprops=dict(arrowstyle="->", color="#1E3A8A", lw=2, mutation_scale=12))
    ax.annotate("", xy=(8.0, 2.3), xytext=(7.85, 2.3), arrowprops=dict(arrowstyle="->", color="#059669", lw=2, mutation_scale=12))

    plt.tight_layout()
    out_path = os.path.join(assets_dir, "flowchart_smart_car_operation.png")
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Generated {out_path}")

if __name__ == "__main__":
    create_car_architecture_diagram()
