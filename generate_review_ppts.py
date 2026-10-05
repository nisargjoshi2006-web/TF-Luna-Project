"""
Generates the two official Review 1 PowerPoint presentations (.pptx):
PPT 1: Team 1 (Priyam & Ayushman) - Drone & Aerial Sensing Subsystem
PPT 2: Team 2 (Nisarg, Mudit, Aryan) - Ground Station, 3D Metrology & AI Analysis
"""

import os
import sys
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# VIT Brand Colors & Theme
NAVY_BLUE = RGBColor(16, 44, 87)       # Primary Header Blue
DARK_BG = RGBColor(10, 15, 25)         # Dark Architectural Theme
WHITE = RGBColor(255, 255, 255)
LIGHT_BLUE = RGBColor(0, 180, 216)     # Cyan Accent
ORANGE = RGBColor(255, 107, 53)        # Highlight Accent
GRAY_TEXT = RGBColor(180, 190, 205)
CARD_BG = RGBColor(22, 33, 62)         # Slide card background


def apply_slide_background(slide, color=DARK_BG):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_header(slide, title_text, category_text="BACSE291 - Innovative Design Project | First Review | Fall 2026"):
    # Header bar container
    tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_cat = tf.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(11)
    p_cat.font.bold = True
    p_cat.font.color.rgb = LIGHT_BLUE

    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = WHITE


def add_card(slide, left, top, width, height, title, items, border_color=LIGHT_BLUE):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = CARD_BG
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.5)

    tx_box = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), width - Inches(0.4), height - Inches(0.4))
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_title = tf.paragraphs[0]
    p_title.text = title
    p_title.font.size = Pt(15)
    p_title.font.bold = True
    p_title.font.color.rgb = border_color

    for item in items:
        p = tf.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(12)
        p.font.color.rgb = WHITE
        p.space_before = Pt(6)


def create_title_slide(prs, project_title, sub_title, team_members, guide_name="Dr. Senthil Kumar N (Associate Professor Grade 2, SCE)"):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(slide)

    # University & Course Header
    tb_univ = slide.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.7), Inches(0.8))
    tf_u = tb_univ.text_frame
    p_u = tf_u.paragraphs[0]
    p_u.text = "VELLORE INSTITUTE OF TECHNOLOGY (VIT) - CHENNAI"
    p_u.font.size = Pt(14)
    p_u.font.bold = True
    p_u.font.color.rgb = LIGHT_BLUE

    p_u2 = tf_u.add_paragraph()
    p_u2.text = "School of Computer Science and Engineering | BACSE291 - Innovative Design Project | Fall 2026"
    p_u2.font.size = Pt(11)
    p_u2.font.color.rgb = GRAY_TEXT

    # Project Title
    tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(2.0))
    tf_t = tb_title.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = project_title
    p_t.font.size = Pt(26)
    p_t.font.bold = True
    p_t.font.color.rgb = WHITE

    p_sub = tf_t.add_paragraph()
    p_sub.text = sub_title
    p_sub.font.size = Pt(16)
    p_sub.font.color.rgb = ORANGE
    p_sub.space_before = Pt(8)

    # Team Members Card
    add_card(slide, Inches(0.8), Inches(4.2), Inches(6.0), Inches(2.6), "TEAM DETAILS", team_members, border_color=LIGHT_BLUE)

    # Guide Card
    add_card(slide, Inches(7.1), Inches(4.2), Inches(5.4), Inches(2.6), "PROJECT GUIDE & EVALUATION", [
        f"Guide: {guide_name}",
        "Review Stage: First Review (Review 1)",
        "System Scope: Phase 1 & 2 Integrated Framework",
        "Target Application: Civil Infrastructure & SHM"
    ], border_color=ORANGE)


# ==============================================================================
# 1. BUILD PPT 1: TEAM 1 (DRONE & AERIAL SENSING SUBSYSTEM)
# ==============================================================================
def generate_ppt_team1(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Slide 1: Title
    create_title_slide(
        prs,
        "AI IN STRUCTURAL HEALTH MONITORING FOR PREDICTIVE MAINTENANCE",
        "Subsystem 1: Autonomous Aerial Drone Carrier & Standoff Distance LiDAR Sensing",
        [
            "Priyam Sharma (25BAI0159) - Drone Hardware & LiDAR Gimbal Mount",
            "Ayushman Kaushik (25BCE0927) - Telemetry Link & Grid Scan Flight Trajectory",
            "In Collaboration with Ground Team: Nisarg, Mudit, Aryan"
        ]
    )

    # Slide 2: Problem Statement & Motivation
    s2 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s2)
    add_header(s2, "Problem Statement: The Need for Aerial Infrastructure Inspection")
    add_card(s2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), "Limitations of Manual Inspection", [
        "Dangerous & Inaccessible: Tall building facades, bridge columns, and ornamental pillars cannot be reached without scaffolding or ladders.",
        "Manual Hand-Drag Jitter: Ground tests showed dragging a sensor box introduces 2-3 cm manual tremors and inconsistent speeds.",
        "Discontinuous Coverage: Manual point-checks leave major blind spots on structural surfaces.",
        "Slow & High Labor Cost: Requires multiple technicians and days of setup time."
    ], border_color=ORANGE)
    add_card(s2, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8), "Proposed Aerial Solution", [
        "Autonomous Aerial Robotic Carrier: Quadcopter drone carries the ToF LiDAR to any elevation.",
        "Vibration-Isolated Sensor Mount: Eliminates motor oscillations and sliding friction.",
        "Safe Standoff Distance Hold: Maintains a steady 1-meter gap from walls during flight.",
        "Wireless Real-Time Telemetry: Streams distance and flux data directly to ground analytics."
    ], border_color=LIGHT_BLUE)

    # Slide 3: Standoff Navigation - The Bat Analogy
    s3 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s3)
    add_header(s3, "Aerial Sensing Strategy: The Bat-Inspired 1-Meter Standoff Hold")
    add_card(s3, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), "Why 1-Meter Standoff Distance?", [
        "Bat Navigation Principle: Just as bats fly safely without colliding by echolocating nearby surfaces, the drone maintains a precise barrier from the wall.",
        "Prevents Memory Overload: Scanning from far away (5m+) captures irrelevant background clutter, overloading memory and databases.",
        "Optimal Optical Signal: The TF-Luna 850nm laser achieves maximum SNR and ±1cm precision within the 1-3m range.",
        "Active Collision Avoidance: If the drone drifts closer than 0.8m, the flight loop automatically repels back to 1.0m."
    ], border_color=LIGHT_BLUE)
    add_card(s3, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8), "Operational Sequence", [
        "1. Directional Orientation: User points drone heading toward target structure (e.g. wall or SJT ornamental column).",
        "2. Controlled Approach: Drone flies forward until proximity detection registers d = 1.0 meter.",
        "3. Scan Trigger: High-speed 100 Hz LiDAR data recording begins automatically.",
        "4. Continuous Contour Hold: Drone traverses horizontally while keeping distance constant."
    ], border_color=ORANGE)

    # Slide 4: Drone Architecture & Hardware Integration
    s4 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s4)
    add_header(s4, "Drone Hardware Integration & Sensor Payload")
    add_card(s4, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), "Hardware Avionics & Mount (Priyam)", [
        "Drone Frame: F450 / Custom Lightweight Quadcopter airframe.",
        "Flight Controller: Pixhawk / Betaflight with altitude and position hold capabilities.",
        "LiDAR Mount: 3D-printed forward-facing gimbal mount with silicone vibration isolation dampers.",
        "Power System: Step-down DC-DC buck converter providing clean, regulated 5V DC from 3S LiPo battery.",
        "Sensor: TF-Luna Time-of-Flight LiDAR (850nm, 100Hz, UART 115200 baud)."
    ], border_color=LIGHT_BLUE)
    add_card(s4, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8), "Telemetry Link & Flight Logic (Ayushman)", [
        "Wireless Data Link: ESP32 onboard transceiver broadcasting high-speed UDP telemetry over Wi-Fi.",
        "Telemetry Frame: [Timestamp, Distance (cm), Optical Flux, Drone Barometric Altitude].",
        "Onboard Black-Box Logging: MicroSD card backup to guarantee zero packet loss during transmission.",
        "Ground Link Interface: Streams raw frames directly to Nisarg's 3D Point Cloud Generator."
    ], border_color=ORANGE)

    # Slide 5: Autonomous Raster Flight Path
    s5 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s5)
    add_header(s5, "Flight Path Planning: Autonomous Vertical & Horizontal Raster Scanning")
    add_card(s5, Inches(0.8), Inches(1.8), Inches(11.6), Inches(4.8), "Raster 'Lawnmower' Trajectory Algorithm", [
        "Layer 1 (Horizontal Pass): Drone maintains height Y = 1.0m, sweeping left-to-right across the wall at a constant 0.2 m/s.",
        "Vertical Step-Up: Reaching the wall boundary, the drone climbs by ΔY = 15 cm to the next elevation level.",
        "Layer 2 (Return Pass): Sweeps right-to-left at Y = 1.15m, collecting the next parallel slice of structural telemetry.",
        "Continuous Multi-Layer Cloud: Repeating this pattern produces a uniform 2D/3D matrix across the entire structure surface.",
        "Obstacle Avoidance Fallback: If an unexpected surface protrusion is detected (< 0.6m), drone hovers and signals an alert."
    ], border_color=LIGHT_BLUE)

    # Slide 6: Literature Review - Aerial Inspection
    s6 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s6)
    add_header(s6, "Literature Review: UAV Structural Inspection & Standoff Sensing")
    add_card(s6, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), "Reviewed Studies", [
        "Azimi et al. (2020): Surveyed UAV-based vision SHM; identified battery constraints and lighting dependence as primary challenges.",
        "Park, Eem & Jeon (2020): Tested laser structured light on UAVs for crack width estimation; noted pose jitter affects measurement accuracy.",
        "Teo & Yang (2023): Evaluated mobile LiDAR; showed dynamic motion errors grow up to 1-2 cm without dedicated standoff hold."
    ], border_color=LIGHT_BLUE)
    add_card(s6, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8), "Research Gaps Addressed by Subsystem 1", [
        "Gap 1 (Motion Stability): Handheld scanners suffer from unsteady tremors; our drone platform maintains constant speed and standoff.",
        "Gap 2 (Accessibility): Ground sensors cannot inspect elevated structures; UAV carrier reaches full vertical spans.",
        "Gap 3 (Sensor Fusion Efficiency): Standoff control prevents collecting unnecessary points, optimizing flight endurance."
    ], border_color=ORANGE)

    # Slide 7: Phase 1 Objectives & Progress
    s7 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s7)
    add_header(s7, "Subsystem 1 Status & Collaborative Next Steps")
    add_card(s7, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), "Current Completed Progress", [
        "✓ Sensor bench testing & UART serial communication established at 115200 baud.",
        "✓ WiFi UDP telemetry bridge validated for transmitting 100Hz packets wirelessly.",
        "✓ Standoff distance hold logic verified using distance threshold feedback.",
        "✓ Collaboration pipeline established with Ground Team (Nisarg, Mudit, Aryan)."
    ], border_color=LIGHT_BLUE)
    add_card(s7, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8), "Next Steps towards Final Review", [
        "• Field mounting on drone airframe with vibration silicone dampening.",
        "• Outdoor flight trials against campus structures (e.g. SJT building facade/pillars).",
        "• Future Sensor Upgrade: Integration of 360° rotating LiDAR (YDLIDAR X2) funded under university student grant.",
        "• Direct streaming integration with the 5-Tab Streamlit Dashboard."
    ], border_color=ORANGE)

    prs.save(output_path)
    print(f"[OK] Successfully generated PPT 1: {output_path}")


# ==============================================================================
# 2. BUILD PPT 2: TEAM 2 (GROUND STATION, 3D METROLOGY & AI ANALYSIS)
# ==============================================================================
def generate_ppt_team2(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Slide 1: Title
    create_title_slide(
        prs,
        "AI IN STRUCTURAL HEALTH MONITORING FOR PREDICTIVE MAINTENANCE",
        "Subsystem 2: 3D Point Cloud Reconstruction, Architectural Metrology & AI Defect Analytics",
        [
            "Nisarg Joshi (25BCE0594) - 3D Point Cloud (.PLY) & Metrology Engine",
            "Mudit Gupta (25BA0110) - AI Geometric Classification & Defect Localization",
            "Aryan Mithari (25BAI0115) - 5-Tab Streamlit UI & Three.js WebGL Viewer",
            "Data Feed Provided by Drone Subsystem: Priyam & Ayushman"
        ]
    )

    # Slide 2: Problem Statement & Proposed Solution
    s2 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s2)
    add_header(s2, "Problem Statement: From Raw Distance Telemetry to 3D Insight")
    add_card(s2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), "The Challenge", [
        "Raw Telemetry is Just 1D Numbers: Streaming distance points without spatial context provides zero structural insight to civil inspectors.",
        "Manual Geometry Classification is Tedious: Determining whether an object is a flat wall, column, or damaged recess requires complex manual rules.",
        "Centimeter Inaccuracies: Uncalibrated ToF sensors exhibit fixed zero-point casing offsets and optical jitter.",
        "Need for Non-Destructive Metrology: Calculating building surface area and volume without manual measuring tapes."
    ], border_color=ORANGE)
    add_card(s2, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8), "Proposed Ground Solution", [
        "Real-Time 3D Digital Twinning: Transforms streaming telemetry into dense, color-coded 3D point clouds (.PLY).",
        "Automated Architectural Metrology: Instant calculation of Floor Area, Wall Area, Volume, and Perimeter.",
        "Dual-Parameter AI Defect Classifier: Identifies Cavities, Bulges, and Cracks using distance and optical flux.",
        "Interactive 60 FPS WebGL Dashboard: 5-tab suite with one-click camera snaps and ISO-compliant reports."
    ], border_color=LIGHT_BLUE)

    # Slide 3: System Pipeline & Data Flow
    s3 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s3)
    add_header(s3, "End-to-End System Pipeline & Subsystem Integration")
    add_card(s3, Inches(0.8), Inches(1.8), Inches(11.6), Inches(4.8), "Integrated 6-Stage Processing Pipeline", [
        "Stage 1: Drone Telemetry Ingestion -> Ground receiver parses incoming UDP frames at 100 Hz.",
        "Stage 2: Scientific Calibration & DSP -> Applies zero-offset model (y = 1.0x + 3.00 cm) and rolling median filter (N=8).",
        "Stage 3: 3D Point Cloud Synthesis (Nisarg) -> Projects polar telemetry into Cartesian coordinates (X, Y, Z) and exports .PLY files.",
        "Stage 4: Automated Metrology (Nisarg) -> Calculates Floor Area (15.12 m²), Wall Area (42.12 m²), and Room Volume (40.82 m³).",
        "Stage 5: AI Defect Classification (Mudit) -> Evaluates Δd and Flux Φ to flag Spalling, Bulging, and Fractures.",
        "Stage 6: Interactive WebGL Interface (Aryan) -> Renders 3D digital twin in Streamlit with floating N/S/E/W wall labels."
    ], border_color=LIGHT_BLUE)

    # Slide 4: Automated Architectural Metrology
    s4 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s4)
    add_header(s4, "Automated Architectural Metrology Formulation (Nisarg)")
    add_card(s4, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), "Mathematical Formulations", [
        "Floor Surface Area: A_floor = Width × Depth = 4.20m × 3.60m = 15.12 m² (162.8 sq ft)",
        "Wall Surface Area: A_wall = 2(Width + Depth) × Height = 2(4.20 + 3.60) × 2.70 = 42.12 m²",
        "Total Enclosed Area: A_total = 2(A_floor) + A_wall = 72.36 m²",
        "Enclosed Volume: V = A_floor × Height = 15.12 × 2.70 = 40.82 m³ (1,441.5 cu ft)",
        "Perimeter: P = 2(Width + Depth) = 15.60 meters"
    ], border_color=LIGHT_BLUE)
    add_card(s4, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8), "Individual Wall Breakdown", [
        "🧭 North Wall (Z = 3.60m): Span 4.20m × Height 2.70m = 11.34 m² (Window Recess Feature)",
        "🧭 South Wall (Z = 0.00m): Span 4.20m × Height 2.70m = 11.34 m² (Entrance Portal Trim)",
        "🧭 East Wall (X = 4.20m): Span 3.60m × Height 2.70m = 9.72 m² (Solid Masonry Boundary)",
        "🧭 West Wall (X = 0.00m): Span 3.60m × Height 2.70m = 9.72 m² (⚠️ Spalling Cavity Location)"
    ], border_color=ORANGE)

    # Slide 5: Multi-Defect Detection Engine
    s5 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s5)
    add_header(s5, "Multi-Defect SHM Detection Engine (Mudit)")
    add_card(s5, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), "Defect Classification Logic", [
        "🔴 Surface Cavity / Spalling: Distance increases by Δd >= +2.0 cm as laser travels into concrete loss depression.",
        "🟠 Surface Bulge / Delamination: Distance decreases by Δd <= -2.0 cm as plaster swells closer to sensor.",
        "🟡 Crack / Structural Fissure: Narrow split traps laser photons; Optical Signal Flux drops sharply (Φ < 600) with micro-jitter.",
        "🟢 Nominal Sound Surface: Measurements lie within ±1.0 cm structural tolerance baseline."
    ], border_color=ORANGE)
    add_card(s5, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8), "AI/ML Model Roadmap (Future Enhancement)", [
        "Geometric Surface Classification: Machine learning model trained to classify Point Cloud clusters into Planes (Walls), Cylinders (Pillars), and Spheres.",
        "Automatic Defect Segmentation: PointNet++ / DBSCAN clustering to segment irregular defect boundaries automatically.",
        "Predictive Deterioration Forecasting: Time-series analysis across dated scans to track deterioration rate and predict Remaining Useful Life (RUL)."
    ], border_color=LIGHT_BLUE)

    # Slide 6: Real Photo vs 3D Point Cloud Comparison
    s6 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s6)
    add_header(s6, "Visual Validation: Physical Structure vs. 3D Digital Twin")
    add_card(s6, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), "Physical Structural Reference", [
        "Physical Target: Test room / structural wall corridor (4.20m W × 3.60m D × 2.70m H).",
        "Ground Truth Verification: Measured with benchmark laser reference according to ISO 17123-4.",
        "Real Photography: Captures true material texture, wall boundaries, and physical cavity locations.",
        "Side-by-Side Validation: Allows evaluators to visually verify spatial reconstruction fidelity."
    ], border_color=LIGHT_BLUE)
    add_card(s6, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8), "Synthesized 3D Point Cloud", [
        "Density: 4,949+ spatial vertices with HSL rainbow height gradient.",
        "Floating 3D Wall Labels: Dynamic canvas billboard sprites facing camera (North, East, South, West).",
        "One-Click Camera Snaps: Instant preset views for inspecting individual walls or top-down floorplan.",
        "Defect Localization: Highlighted in bright red diamond markers in CAD inspection view."
    ], border_color=ORANGE)

    # Slide 7: 5-Tab Dashboard & UI
    s7 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s7)
    add_header(s7, "Interactive Streamlit Dashboard & WebGL Viewer (Aryan)")
    add_card(s7, Inches(0.8), Inches(1.8), Inches(11.6), Inches(4.8), "5 Specialized Inspection Modules", [
        "Tab 1: Live Telemetry & Defect Detector -> Real-time 100 Hz distance stream, calibration offset, and live anomaly alert badges.",
        "Tab 2: Linear Profile & Cavity Mapping -> 2D elevation depth contour with interactive range zoom and classified defect log table.",
        "Tab 3: Sensor Calibration & Metrology -> Verified linear regression curve (y = 1.0x + 3.00, R² = 0.9998) and ISO error distribution.",
        "Tab 4: PLY·FORGE 3D WebGL Suite -> Hardware-accelerated 60 FPS Three.js viewer with glowing circular particles and camera snaps.",
        "Tab 5: 3D Room Reconstruction & Metrology -> Complete 3D room, 4 wall breakdown cards, area/volume metrics, and 1-click report export."
    ], border_color=LIGHT_BLUE)

    # Slide 8: Literature Review - Point Clouds & AI
    s8 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s8)
    add_header(s8, "Literature Review: Point Cloud Processing & AI for SHM")
    add_card(s8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), "Reviewed Literature", [
        "Chen & Cho (2022) - CrackEmbed: Segmented crack regions directly in 3D point clouds using point-feature embedding.",
        "Zhang et al. (2022): Developed point-cloud coordinate calibration and rebar spalling quantification on RC columns.",
        "Spencer et al. (2025): Comprehensive review of AI for SHM, highlighting data-driven damage detection and deployment challenges."
    ], border_color=LIGHT_BLUE)
    add_card(s8, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8), "Research Gaps Addressed by Subsystem 2", [
        "Gap 1 (Cost): Replaces expensive multi-thousand dollar scanners with an accessible ToF/LiDAR framework.",
        "Gap 2 (Multi-Defect): Detects cavities, bulges, and cracks in one unified workflow rather than single-defect approaches.",
        "Gap 3 (Usability): Provides an interactive web-based 3D digital twin without requiring specialized CAD software."
    ], border_color=ORANGE)

    # Slide 9: Team Contributions & Summary
    s9 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s9)
    add_header(s9, "Summary of Subsystem 2 Contributions & Roadmap")
    add_card(s9, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), "Current Completed Milestones", [
        "✓ 3D point cloud generation pipeline (.PLY) fully functional with rainbow height gradient.",
        "✓ Automated architectural metrology engine calculating areas and volumes in real-time.",
        "✓ Rule-based multi-defect classifier detecting cavities, bulges, and crack indications.",
        "✓ 5-tab interactive Streamlit dashboard live and tested."
    ], border_color=LIGHT_BLUE)
    add_card(s9, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8), "Next Steps Towards Final Review", [
        "• Train Machine Learning surface classifier (PointNet / SVM) on physical scan clusters.",
        "• Ingest live wireless UDP telemetry stream directly from Team 1's Drone carrier.",
        "• Longitudinal scan comparison for automated deterioration tracking over time.",
        "• Validation against controlled artificial defects on campus test columns."
    ], border_color=ORANGE)

    prs.save(output_path)
    print(f"[OK] Successfully generated PPT 2: {output_path}")


if __name__ == "__main__":
    desktop = os.path.join(os.path.expanduser('~'), 'OneDrive', 'Desktop')
    ppt1_path = os.path.join(desktop, "Review1_PPT_Team1_Drone_Subsystem.pptx")
    ppt2_path = os.path.join(desktop, "Review1_PPT_Team2_Ground_AI_3D.pptx")
    
    generate_ppt_team1(ppt1_path)
    generate_ppt_team2(ppt2_path)
    print("All PowerPoint presentations generated successfully!")
