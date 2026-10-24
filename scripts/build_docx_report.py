import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=110, right=110):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def generate_docx(filename="BACSE291_RESEARCH_PROGRESS_REPORT_AND_FUTURE_WORK_PLAN.docx"):
    doc = docx.Document()

    # Set 0.75-inch margins
    for s in doc.sections:
        s.top_margin = Inches(0.75)
        s.bottom_margin = Inches(0.75)
        s.left_margin = Inches(0.75)
        s.right_margin = Inches(0.75)

    NAVY = RGBColor(27, 54, 93)      # #1B365D
    TEAL = RGBColor(0, 130, 150)     # #008296
    DARK = RGBColor(40, 44, 52)      # #282C34
    MUTED = RGBColor(100, 110, 120)  # #646E78

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = NAVY
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = TEAL
        return p

    def add_body(text, bold_prefix=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = "Calibri"
            r_pre.font.size = Pt(10)
            r_pre.font.bold = True
            r_pre.font.color.rgb = DARK
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.font.color.rgb = DARK
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2.5)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = "Calibri"
            r_pre.font.size = Pt(9.5)
            r_pre.font.bold = True
            r_pre.font.color.rgb = DARK
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.color.rgb = DARK
        return p

    def add_callout(text, title="KEY ARCHITECTURAL CONCEPT:"):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        set_cell_background(cell, "F0F9FF")
        set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r_t = p.add_run(f"📌 {title}\n")
        r_t.font.name = "Arial"
        r_t.font.size = Pt(9.5)
        r_t.font.bold = True
        r_t.font.color.rgb = NAVY
        r_b = p.add_run(text)
        r_b.font.name = "Calibri"
        r_b.font.size = Pt(9)
        r_b.font.color.rgb = DARK
        doc.add_paragraph().paragraph_format.space_after = Pt(3)

    # ==================================================================================
    # COVER PAGE
    # ==================================================================================
    vit_logo_path = "reports/assets/vit_logo.png"
    if os.path.exists(vit_logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_after = Pt(4)
        p_logo.add_run().add_picture(vit_logo_path, width=Inches(1.8))

    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_after = Pt(2)
    r = p_inst.add_run("VELLORE INSTITUTE OF TECHNOLOGY (VIT), VELLORE")
    r.font.name = "Arial"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = NAVY

    p_sch = doc.add_paragraph()
    p_sch.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sch.paragraph_format.space_after = Pt(8)
    r = p_sch.add_run("School of Computer Science and Engineering (SCOPE) & School of Civil Engineering (SCE)\nBACSE291 – Innovative Design Project · Fall Semester 2026")
    r.font.name = "Calibri"
    r.font.size = Pt(10)
    r.font.color.rgb = MUTED

    p_t = doc.add_paragraph()
    p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t.paragraph_format.space_after = Pt(4)
    r = p_t.add_run("AI IN STRUCTURAL HEALTH MONITORING FOR PREDICTIVE MAINTENANCE AND CONTINUOUS SAFETY ASSURANCE")
    r.font.name = "Arial"
    r.font.size = Pt(16)
    r.font.bold = True
    r.font.color.rgb = NAVY

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(12)
    r = p_sub.add_run("Comprehensive Research Progress Report & Future Work Plan\n(Review 1 to Review 3 Synthesis, Subsystem Architecture & Milestone R1 Roadmap)")
    r.font.name = "Arial"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = TEAL

    # Meta Table
    m_tbl = doc.add_table(rows=2, cols=2)
    m_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_items = [
        [("PROJECT IDENTIFIER", "15377IDP01 (Aerial Subsystem) & 15377IDP02 (Ground Analytics)"), ("COURSE", "BACSE291 – Innovative Design Project (Fall 2026)")],
        [("PROJECT GUIDE", "Dr. N. Senthil Kumar, Ph.D (IITM), Assoc. Prof. Gr. 2 (SCE)"), ("MILESTONE", "Progress Review & Future Engineering Plan (Rev. R0)")]
    ]
    for r_idx, row_c in enumerate(meta_items):
        for c_idx, (lbl, val) in enumerate(row_c):
            cell = m_tbl.cell(r_idx, c_idx)
            set_cell_background(cell, "F8FAFC")
            set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            r_lbl = p.add_run(f"{lbl}: ")
            r_lbl.font.size = Pt(8.5)
            r_lbl.font.bold = True
            r_lbl.font.color.rgb = NAVY
            r_val = p.add_run(val)
            r_val.font.size = Pt(8.5)
            r_val.font.color.rgb = DARK

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Team Members Table
    p_tm = doc.add_paragraph()
    p_tm.paragraph_format.space_before = Pt(4)
    p_tm.paragraph_format.space_after = Pt(3)
    r = p_tm.add_run("PROJECT RESEARCH TEAM (ALL 5 MEMBERS ACROSS SUBSYSTEMS 1 & 2):")
    r.font.name = "Arial"
    r.font.size = Pt(10)
    r.font.bold = True
    r.font.color.rgb = NAVY

    tm_tbl = doc.add_table(rows=6, cols=6)
    tm_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tm_headers = ["S.No", "Student Name", "Register No.", "School", "Subsystem & Role", "Assigned Work Package"]
    for c_idx, h in enumerate(tm_headers):
        cell = tm_tbl.cell(0, c_idx)
        set_cell_background(cell, "1B365D")
        set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor(255, 255, 255)

    team_data = [
        ("1", "Nisargkumar Piyushkumar Joshi", "25BCE0594", "SCOPE", "Subsystem 2 Lead (Ground Analytics)", "Linear regression calibration (y=1.0228x+3.20), 3D WebGL engine & spatial metrology"),
        ("2", "Aryan Pranit Mithari", "25BAI0115", "SCOPE", "Subsystem 2 (Ground Analytics)", "Baseline deviation (Δd) calculation, serial pipeline & anomaly detection rules"),
        ("3", "Mudit Gupta", "25BA0110", "SCOPE", "Subsystem 2 (Ground Analytics)", "Geometric defect classification (cavity, bulge, crack-like) & .PLY point cloud export"),
        ("4", "Priyam Sharma", "25BAI0159", "SCOPE", "Subsystem 1 (Aerial Sensing)", "TF-Luna ToF rangefinding payload, MCU hardware wiring & power regulation"),
        ("5", "Ayushman Kaushik", "25BCE0927", "SCOPE", "Subsystem 1 (Aerial Sensing)", "9-byte UART binary frame parser, checksum verification & wireless telemetry link")
    ]
    for r_idx, (sno, nm, reg, sch, sub, wp) in enumerate(team_data):
        bg = "FFFFFF" if r_idx % 2 == 0 else "F8FAFC"
        for c_idx, val in enumerate([sno, nm, reg, sch, sub, wp]):
            cell = tm_tbl.cell(r_idx + 1, c_idx)
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 2, 3] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.size = Pt(8)
            r.font.color.rgb = DARK
            if c_idx == 1:
                r.font.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_callout(
        "This progress report presents the completed milestones, ongoing engineering investigations, and future research work for our Innovative Design Project. The system integrates a lightweight 850nm ToF Micro-LiDAR on an ESP-32 microcontroller with a ground analytics DSP engine and 3D WebGL digital twin platform. Key achievements to date include hardware bench acquisition at 60-100 Hz, sub-centimeter linear calibration (y = 1.0228x + 3.20 cm, R² = 1.0000), 4-wall sequential room twin reconstruction (9,969 vertices), and real-time classification of planar walls, Almari inward bulges, and Gate recesses. The next phase focuses on ADXL345 dynamic tilt compensation, 2D 360° LiDAR integration, wireless UDP telemetry, dynamic coordinate tracking from initial datum (0,0,0), and a dual-platform deployment strategy (drone payload with smart ground car contingency).",
        "EXECUTIVE SUMMARY & FACULTY EVALUATION SCOPE:"
    )

    doc.add_page_break()

    # ==================================================================================
    # SECTION 2: PROJECT OVERVIEW
    # ==================================================================================
    add_h1("2. Project Overview & Research Motivation")
    add_body("Civil infrastructure worldwide—including highway bridges, concrete columns, retaining walls, tunnels, and residential complexes—is subjected to continuous structural fatigue caused by environmental weathering, seismic vibrations, ground settlement, and heavy cyclic loads. Structural Health Monitoring (SHM) is the discipline of tracking physical integrity over time to detect early-stage damage before catastrophic collapse occurs.")
    add_body("The Traditional Inspection Bottleneck: Current industrial civil inspection relies predominantly on manual visual observation and physical measuring tapes, often requiring personnel to deploy hazardous scaffolding, cherry-pickers, or rope-access rigs. This practice has three fatal weaknesses: (1) High Danger & Cost: Inspecting high-altitude facades or bridge piers is labor-intensive and life-threatening; (2) Human Parallax & Sag Error: Measuring tapes sag and bend over spans exceeding 3 meters, introducing random errors of ±2 to 5 cm; and (3) Depth Blindness: Optical cameras and human visual inspections capture 2D surface discoloration and hairline cracks but cannot quantify 3D metric volume loss, subsurface cavities, plaster delamination bulges, or structural wall tilt.")
    add_body("Our Engineering Objective: We develop an autonomous, cost-effective robotic metrology and digital twin pipeline that captures millimeter-accurate physical distance at up to 100 Hz, executes real-time sensor calibration, computes planar wall deviations (Δd), isolates structural anomalies, and renders interactive 3D WebGL point clouds (.PLY/.OBJ) with zero server dependencies.")

    # ==================================================================================
    # SECTION 3: WORK COMPLETED PREVIOUSLY
    # ==================================================================================
    add_h1("3. Work Completed Previously (Review 1 Through Review 3)")
    add_body("Across earlier evaluation reviews (Review 1 through Review 3), the team successfully established the theoretical foundation, physical sensing hardware, mathematical calibration, and 3D digital twin visualization pipeline:")
    add_bullet(" Conducted a comprehensive survey of 25 peer-reviewed papers (SCI/Scopus indexed) across UAV inspection, Time-of-Flight ranging, and vibration isolation. Formulated five core research gaps and decomposed the project into Subsystem 1 (Aerial Payload) and Subsystem 2 (Ground Analytics).", "Review 1 — Literature Survey & Scoping:")
    add_bullet(" Built the benchtop sensing rig combining an ESP-32 DevKit MCU with the Benewake TF-Luna 850nm ToF LiDAR over hardware UART (Serial2). Programmed binary frame decoding with 9-byte modular checksum verification. Derived the exact linear regression calibration model: Calibrated Distance = 1.0228 × Raw + 3.20 cm (R² = 1.0000, RMSE = ±0.02 cm), resolving the intrinsic optical casing delay.", "Review 2 — Hardware Bench Prototyping & Calibration:")
    add_bullet(" Engineered continuous_multi_point_scanner.py, executing sequential wall scanning across North, East, South, and West baselines. Reconstructed a watertight 4.80m × 4.80m room digital twin comprising 9,969 points (room_mesh.ply and room_mesh.obj). Created the standalone Three.js WebGL viewer (real_scan_3d_viewer.html) with toggleable 3D dimension banners and feature callouts.", "Review 3 — Sequential 4-Wall Scanning & 3D Twin Extrusion:")

    # Photos
    hw_img = "reports/assets/hardware_bench_setup.png"
    dr_img = "reports/assets/drone_airframe.png"
    if os.path.exists(hw_img) and os.path.exists(dr_img):
        pic_tbl = doc.add_table(rows=1, cols=2)
        pic_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        pic_tbl.cell(0, 0).paragraphs[0].add_run().add_picture(hw_img, width=Inches(2.8))
        pic_tbl.cell(0, 1).paragraphs[0].add_run().add_picture(dr_img, width=Inches(2.3))
        p_c = doc.add_paragraph()
        p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p_c.add_run("Figure 1: Hardware Bench Assembly (ESP-32 + TF-Luna UART) [Left] | Figure 2: Carbon Fiber Quadcopter Airframe [Right]")
        r.font.size = Pt(8)
        r.font.italic = True
        r.font.color.rgb = MUTED

    # ==================================================================================
    # SECTION 4: CURRENT WORK IN PROGRESS
    # ==================================================================================
    add_h1("4. Current Work in Progress")
    add_body("At present, both subsystems are actively tackling specific signal-processing and embedded hardware refinements to elevate the system from laboratory bench validation to robust physical operation:")
    add_bullet(" During physical testing, manually sliding the sensor along a wall surface introduces mechanical hand jitter of approximately ±2 to 3 cm. Because true civil defects (such as shallow concrete spalling or plaster delamination) often manifest at depths of 2.5 to 3.5 cm, raw thresholding causes false anomaly triggers. We are actively refining an 8-sample rolling median filter (N = 8) combined with multi-pass spatial persistence gating (requiring ≥ 12 consecutive anomalous pulses) to eliminate sliding noise.", "1. Resolving Sliding Noise vs. Defect Sensitivity Overlap:")
    add_bullet(" Currently, the system reliably identifies macro-architectural elements: Normal Wall baseline (Cyan, |Δd| < 15 cm), Almari/Wardrobe inward protrusions (Orange, Δd ≤ -15 cm), and Gate/Doorway outward recesses (Green, Δd ≥ +15 cm). Work is in progress to distinguish fine structural cracks and spalling from standard architectural mouldings using reflected optical signal strength (flux amplitude).", "2. Enhancing Feature Discrimination (Macro vs. Micro):")
    add_bullet(" To eliminate distance stretching caused by sensor pitch and roll tilt (d_true = d_meas · cos(θ_tilt)), we are breadboarding the ADXL345 digital accelerometer over I2C to stream real-time tilt angles and dynamic motor vibration data into the ESP-32 telemetry frame.", "3. ADXL345 3-Axis Accelerometer / Tilt Sensor Integration:")
    add_bullet(" Transitioning from wired USB-serial CSV logging to real-time wireless Wi-Fi UDP streaming from the ESP-32 aerial payload to the ground station receiver.", "4. Wireless Telemetry Link Implementation:")

    # Status Table
    st_tbl = doc.add_table(rows=8, cols=4)
    st_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    st_headers = ["Subsystem Activity", "Target Scope", "Engineering Status", "Supporting Evidence"]
    for c_idx, h in enumerate(st_headers):
        cell = st_tbl.cell(0, c_idx)
        set_cell_background(cell, "1B365D")
        set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor(255, 255, 255)

    st_rows = [
        ("UART Checksum Parsing", "Subsystem 1 (Aerial)", "COMPLETED", "tf_luna_code.ino running at 115200 baud"),
        ("Linear Regression Calibration", "Subsystem 2 (Ground)", "COMPLETED", "y = 1.0228x + 3.20 cm (R² = 1.0000, ±0.02 cm)"),
        ("4-Wall Room Twin Extrusion", "Subsystem 2 (Ground)", "COMPLETED", "9,969-point room_mesh.ply with Three.js viewer"),
        ("Sliding Jitter vs Defect Tuning", "Subsystem 2 (Ground)", "IN PROGRESS", "Median filter N=8 + 12-sample cluster threshold"),
        ("ADXL345 Tilt & Vibration Sensor", "Subsystem 1 (Aerial)", "IN PROGRESS", "I2C driver integration for pitch/roll Euler correction"),
        ("Wireless Wi-Fi / UDP Telemetry", "Subsystems 1 & 2", "IN PROGRESS", "UDP packet framing with sequence numbers"),
        ("Flight & Rover Field Testing", "Subsystems 1 & 2", "PLANNED", "Tethered flight & embedded smart car rover tests")
    ]
    for r_idx, (act, sc, st, ev) in enumerate(st_rows):
        bg = "FFFFFF" if r_idx % 2 == 0 else "F8FAFC"
        for c_idx, val in enumerate([act, sc, st, ev]):
            cell = st_tbl.cell(r_idx + 1, c_idx)
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=50, bottom=50, left=70, right=70)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 2 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.size = Pt(7.5)
            r.font.color.rgb = DARK
            if c_idx == 0:
                r.font.bold = True
            if c_idx == 2:
                r.font.bold = True
                if val == "COMPLETED": r.font.color.rgb = RGBColor(5, 150, 105)
                elif val == "IN PROGRESS": r.font.color.rgb = RGBColor(217, 119, 6)
                else: r.font.color.rgb = RGBColor(27, 54, 93)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # ==================================================================================
    # SECTION 5: IDENTIFIED RESEARCH GAPS
    # ==================================================================================
    add_h1("5. Identified Research Gaps (Literature Synthesis)")
    add_body("Synthesizing the 25 peer-reviewed papers examined during Review 1 reveals five distinct research gaps that directly justify our project's hardware, calibration, and algorithmic architecture:")
    add_bullet(" Commercial Terrestrial Laser Scanners (TLS) and multi-beam LiDARs offer sub-millimeter precision but weigh > 1.2 kg and cost $15,000 to $30,000, making them completely impractical for low-cost micro-drones. Our response is a sub-5g, < $25 single-point ToF LiDAR (TF-Luna) coupled with algorithmic 3D spatial extrusion.", "Gap 1: Cost & Weight Bottleneck in 3D Structural LiDAR [Ref: Papers 2, 5, 11, 19]:")
    add_bullet(" Low-cost ToF sensors exhibit internal optical casing offsets (~3 to 4 cm) and blind zones (< 20 cm) due to physical emitter-receiver lens parallax. Existing studies often ignore this housing bias. Our response is a dual-point linear regression model (y = 1.0228x + 3.20 cm, R² = 1.0000) running directly in firmware with automated blind-zone warning triggers.", "Gap 2: Optical Zero-Point Bias & Parallax Drift in Low-Cost ToF [Ref: Papers 10, 14, 17, 22]:")
    add_bullet(" Computer vision algorithms (CNNs, YOLOv8) segment surface cracks effectively from RGB images but cannot quantify physical depth or volumetric cavity loss. Furthermore, cameras fail under poor illumination, shadows, and featureless concrete surfaces. Our response uses metric LiDAR distance as the primary ground-truth signal.", "Gap 3: Sensor Blindness in Vision-Only Defect Detection [Ref: Papers 1, 3, 7, 8, 18]:")
    add_bullet(" When a sensor is mounted on an aerial platform, propeller vibrations introduce high-frequency noise spikes, while quadcopter pitch and roll tilt angles (θ_tilt) artificially stretch the measured distance (d_meas = d_true / cos(θ_tilt)). Our response incorporates passive silicone damping pads and ADXL345 digital tilt telemetry to apply trigonometric Euler correction.", "Gap 4: Dynamic Vibration & Angular Tilt Distortion [Ref: Papers 4, 5, 6, 24]:")
    add_bullet(" Most low-cost scanners assume the sensor remains at a static origin. When the operator or robot moves through space, points collapse into overlapping clusters. Our response implements dynamic origin tracking from an initial datum (0,0,0) to spatial displacement coordinates (X, Y, Z).", "Gap 5: Static Origin Assumption vs. Dynamic Spatial Translation [Ref: Papers 13, 20, 25]:")

    # ==================================================================================
    # SECTION 6: PROPOSED SOLUTION & TECHNICAL DESIGN
    # ==================================================================================
    add_h1("6. Proposed Solution & Technical System Design")
    add_body("Our system employs a modular, dual-subsystem architecture designed to acquire, calibrate, transmit, and visualize 3D structural condition data in real time:")

    add_callout(
        "1. SENSING PAYLOAD (Team 1): Benewake TF-Luna (850nm ToF) + ADXL345 (3-Axis Tilt/Vibration) wired to ESP-32 DevKit MCU via UART & I2C.\n"
        "2. ON-CHIP PROCESSING: 9-byte binary parsing, checksum validation, linear regression calibration (y = 1.0228x + 3.20 cm), and 8-sample moving average filter.\n"
        "3. TELEMETRY LINK: USB-Serial stream (current bench) transitioning to ESP-32 Wi-Fi UDP wireless transmission.\n"
        "4. GROUND ANALYTICS (Team 2): Baseline planar fitting, deviation computation (Δd), rule-based structural anomaly tagging (cavity, bulge, crack-like).\n"
        "5. 3D METROLOGY & DIGITAL TWIN: Sequential 4-wall spatial extrusion into 9,969-point .PLY/.OBJ models rendered in Three.js WebGL with dimension callouts.",
        "SUBSYSTEM ARCHITECTURE & DATA FLOW PIPELINE:"
    )

    add_h2("6.1 Dynamic Coordinate Tracking Model (Guide's Core Principle)")
    add_body("A critical conceptual requirement emphasized during project evaluation is the mathematical formulation of sensor motion. When moving, sliding, or dragging the scanner across physical space, the system must not assume that every reading originates from a stationary center. Instead, the sensor's own spatial trajectory must be dynamically tracked from an initial datum of (0, 0, 0):")

    add_callout(
        "1. INITIAL ORIGIN DATUM (t = 0): At the start of scanning, the initial physical position is defined as the absolute World Origin:\n"
        "   P_sensor(0) = [X₀, Y₀, Z₀]ᵀ = [0.000, 0.000, 0.000]ᵀ\n\n"
        "2. TRANSLATION VECTOR (t > 0): As the scanner is dragged, moved, or flown across physical axes:\n"
        "   P_sensor(t) = P_sensor(0) + ΔT(t) = [0 + ΔX(t),  0 + ΔY(t),  0 + ΔZ(t)]ᵀ\n"
        "   where ΔX(t) is lateral displacement along wall width, ΔY(t) is vertical elevation/height, and ΔZ(t) is longitudinal depth.\n\n"
        "3. GLOBAL TARGET POINT TRANSFORMATION: For calibrated distance d(t) at azimuth angle θ and tilt angles (pitch φ, roll ψ from ADXL345):\n"
        "   P_target, global(t) = P_sensor(t) + R_tilt(φ, ψ) · [d(t) · sin(θ),  d(t) · sin(φ),  d(t) · cos(θ)]ᵀ\n\n"
        "Significance: Dynamic origin tracking ensures that points mapped during a continuous sweep are placed at their true global coordinates, preventing point cloud collapse and preserving metric realism.",
        "DYNAMIC COORDINATE DISPLACEMENT & PROJECTION FORMULATION:"
    )

    add_h2("6.2 Dual-Platform Deployment Strategy: Primary Drone vs. Embedded Smart Ground Rover")
    add_body("To guarantee experimental success and eliminate single-point operational failure, we adopt a dual-platform strategy: (1) Primary Aerial Platform: A custom carbon fiber quadcopter UAV designed for elevated facade and high-altitude bridge pier inspection, featuring a silicone-damped sensor mount; (2) Contingency Embedded Ground Platform: If indoor safety regulations, hover turbulence, or GPS-denied aerodynamic drift impede flight, the identical embedded LiDAR + ADXL345 + ESP32 payload is mounted onto an Autonomous Smart Ground Car (4WD Robotic Rover) equipped with optical wheel encoders. The rover executes dead-reckoning odometry to measure exact displacement (ΔX, ΔZ) along the floor baseline, validating the dynamic coordinate transformation model with zero risk of drone crash.")

    # 3D Twin image
    twin_img = "reports/room_mesh_3d_model.png"
    if os.path.exists(twin_img):
        p_tw = doc.add_paragraph()
        p_tw.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_tw.add_run().add_picture(twin_img, width=Inches(5.8))
        p_c = doc.add_paragraph()
        p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p_c.add_run("Figure 3: Actual 3D Digital Twin Point Cloud (9,969 vertices) rendered in Three.js WebGL, showing orthogonal Cyan baseline walls (4.8m × 4.8m), inward-bulging Almari (Orange, 65 cm Bahar), and outward-recessed Gate (Green, 60 cm Andar).")
        r.font.size = Pt(8)
        r.font.italic = True
        r.font.color.rgb = MUTED

    # ==================================================================================
    # SECTION 7: WORK PLANNED FOR THE FUTURE
    # ==================================================================================
    add_h1("7. Work Planned for the Future (Milestone R1 Roadmap)")
    add_body("To advance the research from our validated baseline to an end-to-end autonomous inspection platform, the work is structured into five sequential phases:")
    add_bullet(" Implement I2C drivers for the ADXL345 sensor on ESP-32. Program real-time trigonometric Euler angle correction: d_true = d_meas · cos(θ_tilt). Apply digital bandpass filtering to isolate propeller vibration signatures (100–300 Hz) from physical structural deviations.", "Phase 1: ADXL345 Dynamic Tilt Compensation & Vibration Filtering:")
    add_bullet(" Procure and integrate a 2D 360° rotating laser range scanner (YDLIDAR X4 / LD06 / RPLiDAR A1). In contrast to manual sequential wall sweeping, a 2D LiDAR captures full 360° room cross-sections at 5.5–10 Hz (3,000–5,000 pts/sec), enabling instantaneous planar room closure and 2D SLAM occupancy grid generation.", "Phase 2: Sensor Upgrade to 2D 360° Scanning LiDAR (TF-Luna + YDLIDAR Hybrid):")
    add_bullet(" Establish low-latency wireless UDP packet streaming over ESP-32 Wi-Fi. Incorporate 16-bit packet sequence numbering to detect and report packet drop percentages directly to the ground station dashboard.", "Phase 3: Wireless UDP Telemetry Link Handoff:")
    add_bullet(" Conduct comparative scanning trials across laboratory test walls with simulated defects. Evaluate scanning accuracy, point density, and vibration rejection on: (a) the embedded smart ground car rover, and (b) the tethered quadcopter UAV payload.", "Phase 4: Experimental Field Testing on Dual Platforms (Rover & Drone):")
    add_bullet(" Develop cloud/local historical database integration to compare dated scan point clouds of the same physical structure over time, computing time-series deterioration trends (Δd progression) for predictive maintenance decision support.", "Phase 5: Longitudinal Predictive Maintenance Analytics:")

    # ==================================================================================
    # SECTION 8: TIMELINE & MILESTONES TABLE
    # ==================================================================================
    add_h1("8. Timeline and Milestones Table")
    add_body("The research execution plan spans a 12-week schedule aligned with university evaluation stages:")

    gantt_tbl = doc.add_table(rows=7, cols=6)
    gantt_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    g_headers = ["Phase", "Core Activity / Milestone", "Subsystem", "Status", "Planned Period", "Expected Deliverable"]
    for c_idx, h in enumerate(g_headers):
        cell = gantt_tbl.cell(0, c_idx)
        set_cell_background(cell, "1B365D")
        set_cell_margins(cell, top=60, bottom=60, left=70, right=70)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor(255, 255, 255)

    g_data = [
        ("P1", "Literature Survey & 25-Paper Review", "Joint (Team 1 & 2)", "Completed", "Weeks 1–2", "Review 1 Presentation & Gap Analysis Table"),
        ("P2", "TF-Luna UART & Linear Calibration (y=1.0228x+3.20)", "Team 1 (Aerial)", "Completed", "Weeks 3–4", "Bench firmware, ring buffer, calibration.json"),
        ("P3", "4-Wall Room Twin Extrusion & WebGL Viewer", "Team 2 (Ground)", "Completed", "Weeks 5–6", "9,969-pt room_mesh.ply, Three.js HTML suite"),
        ("P4", "Sliding Noise Reduction & ADXL345 Tilt Setup", "Joint (Team 1 & 2)", "In Progress", "Weeks 7–8", "ADXL345 I2C driver, persistence filter, R0 Doc"),
        ("P5", "2D 360° LiDAR Integration & Wireless UDP", "Team 1 (Aerial)", "Planned", "Weeks 9–10", "YDLIDAR turret mount, Wi-Fi UDP packet parser"),
        ("P6", "Dual-Platform Testing (Car Rover & Drone Flights)", "Joint (Team 1 & 2)", "Planned", "Weeks 11–12", "Field metrology validation, final report & demo")
    ]
    for r_idx, (p_id, act, sub, st, per, deliv) in enumerate(g_data):
        bg = "FFFFFF" if r_idx % 2 == 0 else "F8FAFC"
        for c_idx, val in enumerate([p_id, act, sub, st, per, deliv]):
            cell = gantt_tbl.cell(r_idx + 1, c_idx)
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=50, bottom=50, left=70, right=70)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 3, 4] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.size = Pt(7.5)
            r.font.color.rgb = DARK
            if c_idx == 0: r.font.bold = True
            if c_idx == 3:
                r.font.bold = True
                if val == "Completed": r.font.color.rgb = RGBColor(5, 150, 105)
                elif val == "In Progress": r.font.color.rgb = RGBColor(217, 119, 6)
                else: r.font.color.rgb = RGBColor(27, 54, 93)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # ==================================================================================
    # SECTION 9: CHALLENGES & RISKS
    # ==================================================================================
    add_h1("9. Challenges, Risks & Mitigation Strategies")
    
    r_tbl = doc.add_table(rows=5, cols=3)
    r_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    r_headers = ["Observed Challenge / Anticipated Risk", "Impact on System", "Practical Technical Mitigation Strategy"]
    for c_idx, h in enumerate(r_headers):
        cell = r_tbl.cell(0, c_idx)
        set_cell_background(cell, "1B365D")
        set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor(255, 255, 255)

    r_data = [
        ("Propeller Vibration Interference: High-frequency motor oscillations (>100 Hz) cause distance jitter.", "False defect classification spikes in distance telemetry.", "Dual-stage mechanical silicone damping mount + ADXL345 accelerometer bandpass filtering + digital rolling median (N=8)."),
        ("Angular Pitch/Roll Tilt Distortion: Drone or rover tilt stretches beam distance (d/cosθ).", "False wall recession error and distorted room twin bounding box.", "Real-time Euler angle trigonometric correction via ADXL345 tilt angles: d_true = d_meas · cosθ_tilt."),
        ("Indoor Aerodynamic Drift & GPS Loss: Inability to fly safely in narrow indoor corridors.", "Risk of drone collision and discontinuous coordinate tracking.", "Dual-Platform Contingency: Mount identical embedded sensing rig on 4WD smart car rover with optical wheel encoders for safe ground scanning."),
        ("Optical Blind Zone (<20 cm): TF-Luna lens parallax causes inaccurate readings at close range.", "Erroneous near-zero measurements when approaching structural surface.", "Firmware automated blind-zone warning + software standoff boundary control holding platform at a safe 1.0 m distance.")
    ]
    for r_idx, (ch, imp, mit) in enumerate(r_data):
        bg = "FFFFFF" if r_idx % 2 == 0 else "F8FAFC"
        for c_idx, val in enumerate([ch, imp, mit]):
            cell = r_tbl.cell(r_idx + 1, c_idx)
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=50, bottom=50, left=70, right=70)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.size = Pt(7.5)
            r.font.color.rgb = DARK
            if c_idx == 0: r.font.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # ==================================================================================
    # SECTION 10: EXPECTED OUTCOMES & BUDGET
    # ==================================================================================
    add_h1("10. Expected Outcomes & Comprehensive Project Budget (Bill of Materials)")
    add_body("Intended Final Deliverables: (1) A flight-tested aerial payload and ground rover capable of millimeter-accurate facade ranging; (2) An autonomous coordinate transformation pipeline tracking displacement from initial (0,0,0) datum; (3) A 3D WebGL digital twin platform classifying planar walls, furniture bulges, and door recesses; and (4) An automated CSV/PLY/OBJ export suite for civil structural inspection reporting.")
    add_h2("Itemized Project Hardware Budget & Component Sourcing Breakdown:")

    bg_tbl = doc.add_table(rows=14, cols=7)
    bg_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    b_headers = ["S.No", "Hardware Component / Module", "Technical Specifications / Purpose", "Qty", "Unit (₹)", "Total (₹)", "Procurement Status"]
    for c_idx, h in enumerate(b_headers):
        cell = bg_tbl.cell(0, c_idx)
        set_cell_background(cell, "1B365D")
        set_cell_margins(cell, top=60, bottom=60, left=60, right=60)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(7.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    b_rows = [
        ("1", "Benewake TF-Luna LiDAR", "850nm NIR ToF Rangefinder, 0.2–8m, 100Hz, UART", "1", "2,200", "2,200", "Procured / Working"),
        ("2", "ESP32-WROOM-32 MCU", "Dual-core 240MHz, 4MB Flash, Hardware UART, Wi-Fi/BLE", "2", "450", "900", "Procured / Working"),
        ("3", "2D 360° Scanning LiDAR", "YDLIDAR X4 / LD06 / RPLiDAR A1 (360° sweep, 3–5k pts/s)", "1", "7,800", "7,800", "To Procure (Phase 2)"),
        ("4", "ADXL345 Tilt & Vibration Sensor", "3-Axis Digital Accelerometer, ±16g, I2C/SPI, 13-bit", "1", "250", "250", "Procured / In Testing"),
        ("5", "Carbon Fiber Drone Frame", "220–250mm FPV quadcopter airframe, 3K carbon fiber", "1", "2,200", "2,200", "Procured / Assembled"),
        ("6", "Brushless Drone Motors & ESC", "4x 2205 2300KV motors + 4-in-1 30A BLHeli_S ESC", "1 set", "4,500", "4,500", "Procured / Mounted"),
        ("7", "Flight Controller Module", "F4 V3S Plus with Betaflight / iNav, OSD, Barometer", "1", "3,200", "3,200", "To Procure (Phase 4)"),
        ("8", "High-Capacity LiPo Battery", "3S / 4S 1500–2200mAh 75C High-discharge LiPo pack", "1", "1,800", "1,800", "To Procure (Phase 4)"),
        ("9", "LiPo Balance Charger", "iMAX B6 80W Digital Multi-chemistry balance charger", "1", "1,400", "1,400", "To Procure (Phase 4)"),
        ("10", "Smart Car Rover Chassis Kit", "4WD robotic chassis + 4x geared DC motors + L298N driver", "1 set", "1,600", "1,600", "To Procure (Fallback)"),
        ("11", "Optical Wheel Speed Encoders", "Dual optical slotted disc encoders for dead-reckoning odometry", "2", "150", "300", "To Procure (Fallback)"),
        ("12", "Silicone Dampers & Hardware", "Vibration-isolation rubber grommets, standoffs, wiring", "1 set", "550", "550", "Procured / Working"),
        ("—", "TOTAL ESTIMATED BUDGET:", "Complete Dual-Subsystem Hardware (Drone + Rover + Sensing)", "—", "—", "₹ 26,900", "Academic Allocation")
    ]
    for r_idx, (sno, comp, spec, qty, ucost, tot, st) in enumerate(b_rows):
        bg = "FFFFFF" if r_idx % 2 == 0 else "F8FAFC"
        if r_idx == len(b_rows) - 1: bg = "EDF2F7"
        for c_idx, val in enumerate([sno, comp, spec, qty, ucost, tot, st]):
            cell = bg_tbl.cell(r_idx + 1, c_idx)
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=40, bottom=40, left=50, right=50)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 3, 4, 5, 6] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.size = Pt(7.5)
            r.font.color.rgb = DARK
            if c_idx == 1 or r_idx == len(b_rows) - 1: r.font.bold = True
            if c_idx == 6:
                if "Procured" in val: r.font.color.rgb = RGBColor(5, 150, 105)
                elif "To Procure" in val: r.font.color.rgb = RGBColor(217, 119, 6)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # ==================================================================================
    # SECTION 11: CONCLUSION
    # ==================================================================================
    add_h1("11. Conclusion & Immediate Next Steps")
    add_body("This progress report establishes the verified engineering milestones achieved to date across Review 1 through Review 3 for our Innovative Design Project (BACSE291). By integrating the Benewake TF-Luna 850nm ToF Micro-LiDAR with an ESP-32 microcontroller and a ground analytics DSP engine, we have demonstrated sub-centimeter linear calibration (y = 1.0228x + 3.20 cm, R² = 1.0000), 4-wall sequential digital twin reconstruction (9,969 vertices), and real-time classification of planar walls, Almari inward bulges, and Gate recesses.")
    add_body("Immediate Next Steps: (1) Complete ADXL345 tilt and vibration filter testing on the benchtop rig; (2) Implement the dynamic coordinate displacement model updating position vector (ΔX, ΔY, ΔZ) from initial datum (0,0,0); (3) Procure the 2D 360° scanning LiDAR and battery components; and (4) Validate scanning precision on the embedded smart car rover before progressing to tethered quadcopter flight trials.")

    # ==================================================================================
    # SECTION 12: ACADEMIC REFERENCES
    # ==================================================================================
    add_h1("12. Academic References (Literature Base)")
    refs = [
        "[1] S. Feroz and S. Abu Dabous, 'UAV-based remote sensing applications for bridge condition assessment,' Remote Sensing, vol. 13, no. 9, p. 1809, 2021. https://doi.org/10.3390/rs13091809",
        "[2] P. J. Sanchez-Cuevas et al., 'Robotic system for inspection by contact of bridge beams using UAVs,' Sensors, vol. 19, no. 2, p. 305, 2019. https://doi.org/10.3390/s19020305",
        "[3] S.-P. Kao et al., 'Bridge crack inspection efficiency of an unmanned aerial vehicle system with a laser ranging module,' Sensors, vol. 22, no. 12, p. 4469, 2022. https://doi.org/10.3390/s22124469",
        "[4] S. E. Park, S.-H. Eem, and H. Jeon, 'Concrete crack detection and quantification using deep learning and structured light,' Constr. Build. Mater., vol. 252, p. 119096, 2020.",
        "[5] T.-A. Teo and C.-C. Yang, 'Evaluating the accuracy and quality of an iPad Pro's built-in lidar for 3D indoor mapping,' Dev. Built Environ., vol. 14, p. 100169, 2023.",
        "[6] J. Fu et al., 'Design and experimental study on vibration reduction of an UAV Lidar using rubber material,' Actuators, vol. 11, no. 12, p. 345, 2022.",
        "[7] M. Abdulkarem et al., 'Wireless sensor network for structural health monitoring: A contemporary review of technologies, challenges, and future direction,' Struct. Health Monit., vol. 19, no. 3, pp. 693–735, 2020.",
        "[8] Benewake (Beijing) Co., Ltd., 'TF-Luna LiDAR Module Datasheet & Operating Manual,' Benewake Technical Documentation, 2023.",
        "[9] M. Azimi, A. D. Eslamlou, and G. Pekcan, 'Data-driven structural health monitoring and damage detection through deep learning: State-of-the-art review,' Sensors, vol. 20, no. 10, p. 2778, 2020.",
        "[10] B. F. Spencer et al., 'Advances in artificial intelligence for structural health monitoring: A comprehensive review,' KSCE J. Civ. Eng., vol. 29, no. 3, p. 100203, 2025.",
        "[11] C.-Z. Dong and F. N. Catbas, 'A review of computer vision–based structural health monitoring at local and global levels,' Struct. Health Monit., vol. 20, no. 2, pp. 692–743, 2021.",
        "[12] J. Chen and Y. K. Cho, 'CrackEmbed: Point feature embedding for crack segmentation from disaster site point clouds with anomaly detection,' Adv. Eng. Informatics, vol. 52, p. 101550, 2022.",
        "[13] H. Zhang et al., 'Detection of RC spalling damage and quantification of its key properties from 3D point cloud,' KSCE J. Civ. Eng., vol. 26, pp. 2023–2035, 2022.",
        "[14] Z. Sun et al., 'Approach towards the development of digital twin for structural health monitoring of civil infrastructure: A comprehensive review,' Sensors, vol. 25, no. 1, p. 59, 2025.",
        "[15] F. Shahrivar et al., 'AI-based remaining useful life prediction for civil infrastructure: Methods, challenges, and future research directions,' Artif. Intell. Rev., vol. 59, p. 138, 2026."
    ]
    for r in refs:
        add_bullet(r)

    doc.save(filename)
    print(f"Successfully generated DOCX report: {filename}")

if __name__ == '__main__':
    generate_docx()
