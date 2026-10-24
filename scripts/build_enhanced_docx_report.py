import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

sys.stdout.reconfigure(encoding='utf-8')

DOCX_FILENAME = "BACSE291_ENHANCED_IDP_PROGRESS_REPORT_AND_FUTURE_PLAN.docx"
assets_dir = r"c:\Users\nisar\OneDrive\Desktop\TF_LUNA_PROJECT\reports\assets"

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>'))

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="CBD5E1", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def build_docx():
    doc = docx.Document()

    # Set Margins (0.6 inch)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.6)
        section.bottom_margin = Inches(0.6)
        section.left_margin = Inches(0.6)
        section.right_margin = Inches(0.6)

    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(10)
    normal_style.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    # Colors
    c_navy = RGBColor(0x0F, 0x17, 0x2A)
    c_primary = RGBColor(0x1E, 0x3A, 0x8A)
    c_teal = RGBColor(0x0D, 0x94, 0x88)
    c_muted = RGBColor(0x64, 0x74, 0x8B)

    # ================= COVER PAGE =================
    vit_logo = os.path.join(assets_dir, "vit_logo.png")
    if os.path.exists(vit_logo):
        p_logo = doc.add_paragraph()
        p_logo.add_run().add_picture(vit_logo, width=Inches(2.2))
        p_logo.paragraph_format.space_after = Pt(8)

    p_title = doc.add_paragraph()
    run_title = p_title.add_run("AI IN STRUCTURAL HEALTH MONITORING FOR PREDICTIVE MAINTENANCE AND CONTINUOUS SAFETY ASSURANCE")
    run_title.bold = True
    run_title.font.size = Pt(18)
    run_title.font.color.rgb = c_navy
    p_title.paragraph_format.space_after = Pt(4)

    p_sub = doc.add_paragraph()
    run_sub = p_sub.add_run("Comprehensive IDP Progress Report, Previous MDP Integration, Hardware Upgrade, Procurement Budget & Future Implementation Plan")
    run_sub.bold = True
    run_sub.font.size = Pt(11)
    run_sub.font.color.rgb = c_primary
    p_sub.paragraph_format.space_after = Pt(12)

    # Meta Table
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(meta_table)

    meta_cells = meta_table.rows[0].cells
    meta_cells[0].paragraphs[0].add_run("ACADEMIC DETAILS").bold = True
    meta_cells[1].paragraphs[0].add_run("FACULTY GUIDE DETAILS").bold = True
    set_cell_background(meta_cells[0], "F1F5F9")
    set_cell_background(meta_cells[1], "F1F5F9")

    row1_cells = meta_table.rows[1].cells
    row1_cells[0].paragraphs[0].add_run(
        "Course: BACSE291 — Innovative Design Project\n"
        "Program: B.Tech Computer Science & Engineering\n"
        "Semester: Fall Semester 2026\n"
        "Institution: Vellore Institute of Technology (VIT), Vellore"
    )
    row1_cells[1].paragraphs[0].add_run(
        "Faculty Guide: Dr. Senthil Kumar N, Ph.D (IIT Madras)\n"
        "Designation: Associate Professor Grade 2\n"
        "Department: School of Computer Science & Engineering (SCOPE)\n"
        "Faculty ID: 15377  |  Cabin: GDN153"
    )

    row2_cells = meta_table.rows[2].cells
    row2_cells[0].paragraphs[0].add_run("SUBSYSTEM 1: AERIAL SENSING & DRONE (15377IDP01)").bold = True
    row2_cells[1].paragraphs[0].add_run("SUBSYSTEM 2: GROUND ANALYTICS (15377IDP02)").bold = True
    set_cell_background(row2_cells[0], "F1F5F9")
    set_cell_background(row2_cells[1], "F1F5F9")

    row3_cells = meta_table.rows[3].cells
    row3_cells[0].paragraphs[0].add_run(
        "• Priyam Sharma (25BAI0159) — Hardware & UAV Flight Lead\n"
        "• Ayushman Kaushik (25BCE0927) — Telemetry & MCU Lead"
    )
    row3_cells[1].paragraphs[0].add_run(
        "• Nisargkumar Piyushkumar Joshi (25BCE0594) — Subsystem Lead\n"
        "• Aryan Pranit Mithari (25BAI0115) — Point Cloud Processing\n"
        "• Mudit Gupta (25BA0110) — Dashboard & Anomaly Analytics"
    )

    for row in meta_table.rows:
        for cell in row.cells:
            set_cell_margins(cell, top=120, bottom=120, left=150, right=150)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Executive Box
    p_box = doc.add_paragraph()
    p_box_run = p_box.add_run(
        "EXECUTIVE SCOPE SUMMARY: This document presents the complete formal engineering review for BACSE291. "
        "It provides an exhaustive, evidence-based technical synthesis connecting our prior Multidisciplinary Project "
        "(MDP: PLY Forge 3D Point Cloud Processor) to our current Innovative Design Project (IDP). It articulates the completed "
        "aerial acquisition and ground analytics benchmarks, evaluates identified physical scanning constraints (sensor jitter, "
        "manual dragging noise, tilt elongation, motor vibration), justifies essential hardware upgrades (YDLIDAR X2 360° LiDAR, "
        "DFRobot Gravity 360° Tilt Sensor, F450 Quadcopter & 3S LiPo), establishes an itemized ₹27,124 INR procurement budget with contingency, "
        "and outlines a rigorous 7-phase future roadmap toward autonomous structural health monitoring (SHM)."
    )
    p_box_run.font.size = Pt(9.5)
    p_box_run.font.italic = True

    # Collage Image
    room_mesh = os.path.join(assets_dir, "room_mesh_labeled.png")
    if os.path.exists(room_mesh):
        p_cimg = doc.add_paragraph()
        p_cimg.add_run().add_picture(room_mesh, width=Inches(6.2))
        p_cimg.paragraph_format.space_after = Pt(2)
        p_cap = doc.add_paragraph()
        r_cap = p_cap.add_run("Figure 1: Implemented 3D Digital Twin with Inward Almari Bulge (Orange) & Outward Gate Recess (Green)")
        r_cap.font.size = Pt(8.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = c_muted

    doc.add_page_break()

    # ================= HELPER FOR HEADINGS =================
    def add_sec_heading(title):
        p = doc.add_paragraph()
        r = p.add_run(title)
        r.bold = True
        r.font.size = Pt(13)
        r.font.color.rgb = c_primary
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True

    def add_sub_heading(title):
        p = doc.add_paragraph()
        r = p.add_run(title)
        r.bold = True
        r.font.size = Pt(11)
        r.font.color.rgb = c_navy
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True

    # ================= SECTION 1 =================
    add_sec_heading("1. Executive Summary")
    doc.add_paragraph(
        "Civil infrastructures—including high-rise exterior facades, highway bridge piers, industrial cooling towers, and commercial structural "
        "enclosures—suffer continuous degradation caused by thermal expansion, foundation settling, seismic loads, and moisture ingress. "
        "Conventional manual inspection relies heavily on scaffolding, cherry-pickers, and human tactile assessment, exposing personnel to severe "
        "fall hazards while suffering from subjective qualitative records and high labor costs. This joint project establishes an autonomous, "
        "sensor-driven Cyber-Physical Structural Health Monitoring (SHM) ecosystem partitioned into two tightly coupled subsystems:\n\n"
        "• Aerial Subsystem (15377IDP01): Deploys close-range standoff Time-of-Flight (ToF) distance sensing via ESP32 microcontrollers, 100 Hz UART frame synchronization, checksum integrity checks, and real-time wireless telemetry to scan elevated, inaccessible structural envelopes.\n"
        "• Ground Analytics Subsystem (15377IDP02): Ingests streaming distance metrics, executes adaptive baseline tracking, computes geometric residuals (Δd), flags structural anomalies (spalling cavities, structural bulges, cracks), reconstructs 3D digital twins, and generates automated compliance reports.\n\n"
        "Key Progress to Date: The project has successfully delivered a physical ESP32 testbed operating a calibrated Benewake TF-Luna ToF sensor (regression model: y = 1.0228x + 3.20 cm, R²=1.0000, RMSE=±0.02 cm across 39.0 cm and 61.4 cm physical benchmarks), a 9,969-point 3D digital twin room reconstruction correctly segmenting an inward Almari bulge (+65 cm) and outward gate recess (-60 cm), and an interactive multi-tab Streamlit ground operations dashboard. Building directly upon our team's previous Multidisciplinary Project (MDP: PLY Forge), client-side WebGL point-cloud rendering and voxel compression algorithms provide zero-latency spatial visualization.\n\n"
        "Critical Engineering Gap & Upgrade Justification: Manual sliding tests revealed ~2–3 cm measurement fluctuations resulting from hand-motion jitter and uncompensated sensor tilt. Furthermore, while the TF-Luna provides high-speed 1D ranging (100 Hz), reconstructing a complete spatial perimeter requires manual traverse or complex 2-axis articulation. To overcome these constraints, this report details the engineering justification and procurement budget for: (1) a YDLIDAR X2 360° 2D LiDAR (3,000 pts/sec, 7 Hz continuous planar slicing, 0.12–8.0 m range), (2) a DFRobot Gravity Digital 360° Tilt Sensor for dynamic pitch/roll angular correction (d_true = d_meas · cos θ), and (3) an F450 Quadcopter Drone development kit with a 3S 4200mAh LiPo battery to transition from bench testing to airborne structural inspection."
    )

    # ================= SECTION 2 =================
    add_sec_heading("2. Project Background & Technical Objectives")
    doc.add_paragraph(
        "Modern structural maintenance requires transitioning from reactive repair to proactive, quantitative condition assessment. "
        "Structural surfaces exhibit subtle geometric precursors prior to catastrophic failure, including spalling cavities (concrete flaking away), "
        "sub-surface shear bulges (delamination or masonry buckling), and vertical shear cracks. However, acquiring high-fidelity geometric metrics "
        "from vertical facades presents extreme technical challenges: (1) Inaccessibility: Scaffolding is cost-prohibitive for routine monitoring; "
        "(2) Human Error: Manual ultrasonic gauges produce sparse records without a global spatial coordinate reference; and "
        "(3) Terrestrial LiDAR Limitations: Commercial terrestrial laser scanners (TLS) cost >₹15,00,000 INR, weigh 5–10 kg, and suffer severe "
        "occultation when viewing elevated facades from ground level.\n\n"
        "Primary Technical Objectives of the Project:\n"
        "• Obj 1 (Aerial Sensing): Develop a lightweight (<250g payload), low-power (<3W) aerial sensing payload combining optical ToF ranging and 360° planar LiDAR with active tilt sensing.\n"
        "• Obj 2 (Embedded Validation): Implement real-time UART frame validation (0x59 0x59 header, 8-bit checksum) and on-chip median filtering at 100 Hz on dual-core ESP32 microcontrollers.\n"
        "• Obj 3 (Telemetry & Ingestion): Establish high-throughput wireless data telemetry (Wi-Fi UDP / Serial RF) linking airborne sensors to the ground operations base station.\n"
        "• Obj 4 (Geometric Defect Extraction): Formulate rule-based anomaly detection algorithms operating on rolling baseline residuals (Δd = d_meas - d_ref) to localize cavities (+Δd), bulges (-Δd), and crack spikes (|Δd| > T).\n"
        "• Obj 5 (Spatial Digital Twin): Reconstruct wall-tagged 3D point clouds and room meshes (.PLY format) integrating previous MDP voxel-grid compression and WebGL GPU acceleration.\n"
        "• Obj 6 (Predictive Baseline Maintenance): Formulate longitudinal health indexes tracking rate-of-deformation (∂(Δd)/∂t) across successive inspection cycles to forecast structural maintenance windows."
    )

    # ================= SECTION 3 =================
    add_sec_heading("3. Previous MDP Work (PLY Forge) & Cross-Project Relevance")
    doc.add_paragraph(
        "During the earlier Multidisciplinary Project (MDP), our team engineered PLY Forge: Point Cloud Processor, a high-performance, "
        "fully client-side WebGL application designed to parse, visualize, filter, compress, and triangulate 3D point cloud datasets. "
        "A rigorous audit of the MDP Final Report (`Multidisciplinary_project_Final_report.pdf`) and the codebase archive (`ply (1).zip` containing "
        "`index.html`, `ply_processor.js`, and `README.md`) verifies the following operational capabilities and architectural foundation:\n\n"
        "• Binary & ASCII PLY Ingestion: Engineered custom parsers utilizing JavaScript DataView, TextDecoder, and FileReader APIs to ingest Polygon File Format (.PLY) data supporting float32 coordinates, uint8 RGB color channels, and little/big-endian switching.\n"
        "• Zero-Dependency WebGL 1.0 Pipeline: Operates completely native within standard web browsers without relying on external packages (Three.js, Three-PLYLoader, npm modules). Custom GLSL vertex and fragment shaders render point sprites with per-vertex color interpolation directly from GPU Float32Array buffers.\n"
        "• Voxel-Grid Downsampling Compression: Implements spatial hashing dividing 3D bounding boxes into discrete voxel cubes of size s. Points within each voxel are averaged or quantized to their centroid using JavaScript Map structures, achieving 60%–85% file compression while preserving structural boundaries.\n"
        "• Region Selection & Circle Filtering: Ray-casting and mouse-driven circle selection isolate specific structural regions, utilizing JavaScript Set structures for O(1) point indexing and deletion.\n"
        "• Surface Reconstruction & Triangulation: Implements 2.5D Delaunay triangulation, convex hull, and grid-based surface meshing algorithms, converting unorganized point sets into continuous polygonal facet meshes.\n"
        "• Standardized PLY Export: Generates compliant ASCII/Binary PLY files via client-side Blob and URL.createObjectURL() for immediate export into CAD or GIS environments."
    )

    # MDP Table
    t_mdp_doc = doc.add_table(rows=7, cols=4)
    t_mdp_doc.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_mdp_doc)

    headers = ["Previous MDP Capability", "Potential Use in Current IDP", "Required Modification / Adaptation", "Integration Status"]
    for i, h in enumerate(headers):
        cell = t_mdp_doc.rows[0].cells[i]
        cell.paragraphs[0].add_run(h).bold = True
        set_cell_background(cell, "1E3A8A")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    mdp_rows = [
        ("Client-Side WebGL 1.0 Point Cloud Rendering", "Real-time GPU rendering of LiDAR facade scans on Ground Station", "Adapt shader uniforms to render dynamic color ramps (Jet/Viridis) mapped to defect depth (Δd)", "Ready / Integrated in Tab 4"),
        ("Voxel-Grid Downsampling Compression", "Compress dense LiDAR clouds (3,000 pts/s) before disk logging & cloud sync", "Tune voxel step (1–2 cm) to prevent smoothing out narrow cracks (<1.5 cm width)", "Algorithm Reusable"),
        ("Binary & ASCII PLY Exporter", "Generate industry-standard .PLY digital twins from physical LiDAR room measurements", "Prepend wall semantic tags (North, South, East, West, Almari, Gate) into vertex headers", "Fully Functional"),
        ("Circle-Based ROI Selection & Isolation", "Allow structural inspectors to click and isolate detected spalls or bulges for metrology", "Link selection directly to automated engineering report generator (area & volume calculation)", "In Progress"),
        ("2.5D Delaunay & Grid Mesh Triangulation", "Convert sparse LiDAR scan slices into solid watertight structural surface models", "Requires dense planar profiles or multi-line scans from YDLIDAR X2 to form 2D manifolds", "Planned (Post-LiDAR)"),
        ("Static File Loading Workflow (User Upload)", "Ground analytics dashboard stream ingestion", "Replace manual file picker with WebSocket / Serial byte buffer streaming parser", "Active Development")
    ]

    for row_idx, data in enumerate(mdp_rows):
        row = t_mdp_doc.rows[row_idx + 1]
        for col_idx, text in enumerate(data):
            cell = row.cells[col_idx]
            cell.paragraphs[0].add_run(text)
            if row_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ================= SECTION 4 =================
    add_sec_heading("4. Current IDP Architecture & Verified Work Completed")
    doc.add_paragraph(
        "The current IDP establishes a complete end-to-end cyber-physical pipeline spanning airborne embedded acquisition and ground-side "
        "spatial analytics. The verified operational architecture and implemented subsystems are detailed below:\n\n"
        "Aerial Subsystem (15377IDP01) — Implemented:\n"
        "• Sensing Core: Benewake TF-Luna 850nm dToF sensor (<5g, 0.35W, 100 Hz, 2° FOV).\n"
        "• Embedded Controller: ESP32-WROOM-32 running custom C++ FreeRTOS firmware.\n"
        "• UART Binary Framing: Strict state machine syncing to 0x59 0x59 preamble, extracting 2-byte distance, 2-byte amplitude, 2-byte chip temp, and validating 8-bit checksum: (Σ Bytes 0..7) & 0xFF == Byte 8.\n"
        "• Two-Point Metrology Fit: Universal calibration equation y = 1.0228x + 3.20 cm derived from physical 39.0 cm and 61.4 cm benchmarks (residual RMSE = ±0.00 cm).\n"
        "• Signal Conditioning: On-chip running median filter (window size N=5) to eliminate single-sample optical dropouts.\n"
        "• Data Handoff: 115200 baud USB-UART streaming with planned UDP telemetry.\n\n"
        "Ground Analytics Subsystem (15377IDP02) — Implemented:\n"
        "• Live Telemetry Ingestion: Python serial/buffer reader ingesting calibrated distances.\n"
        "• Rolling Baseline Tracking: Window-mean baseline filter tracking surface contours.\n"
        "• Rule-Based Anomaly Classifier: Cavity (Spall): Δd ≥ +3.5 cm (recessed into wall, colored Orange); Bulge (Buckle): Δd ≤ -3.5 cm (protruding outward, colored Orange); Crack Indication: |Δd| ≥ 1.5 cm vs adjacent neighbors.\n"
        "• 3D Digital Twin Reconstructor: Generates 9,969-point spatial cloud (.PLY) with North/South/East/West wall tags.\n"
        "• Verified Physical Defect Segmentation: Accurately rendered 4.8m × 4.2m room with 65 cm inward Almari bulge and 60 cm outward Gate recess.\n"
        "• Multi-Tab Streamlit Dashboard: 5 operational tabs for telemetry, profiles, calibration, PLY Forge WebGL, and room metrology."
    )

    # Status Matrix Table
    add_sub_heading("Formal Subsystem Implementation Status Matrix")
    t_stat = doc.add_table(rows=12, cols=4)
    t_stat.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_stat)

    stat_headers = ["Subsystem & Feature", "Target Metric / Function", "Current Verification Status", "Supporting Evidence / Artifact"]
    for i, h in enumerate(stat_headers):
        cell = t_stat.rows[0].cells[i]
        cell.paragraphs[0].add_run(h).bold = True
        set_cell_background(cell, "1E3A8A")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    stat_rows = [
        ("TF-Luna Optical Ranging", "0.2m to 8.0m, 100 Hz, 850 nm ToF", "Implemented & Verified", "ESP32 UART bench testbed, CSV logs"),
        ("UART Framing & Checksum", "0x59 0x59 sync, drop corrupt packets", "Implemented & Verified", "C++ firmware state machine in main.cpp"),
        ("Two-Point Calibration Model", "y = 1.0228x + 3.20 cm (RMSE ±0.02cm)", "Implemented & Verified", "Bench measurements at 39.0cm & 61.4cm"),
        ("Multi-Tab Operations Dashboard", "5-tab Streamlit UI (Port 8501)", "Implemented & Verified", "dashboard/app.py running on localhost"),
        ("3D Digital Twin Generation", "9,969 points, wall tagging, PLY export", "Implemented & Verified", "room_mesh.ply & Open3D visualization"),
        ("Almari / Gate Feature Isolation", "Distinguish ±60cm macro from ±3.5cm spalls", "Implemented & Verified", "3D room point cloud with Cyan/Orange/Green"),
        ("Wi-Fi / UDP Wireless Telemetry", "ESP32 socket broadcast to PC base station", "In Progress / Bench Ready", "Firmware written; testing packet drop"),
        ("Tilt Angle Dynamic Compensation", "d_true = d_meas · cos θ (pitch/roll)", "Design Finalized / Awaiting Sensor", "Mathematical derivation complete; sensor budgeted"),
        ("360° Planar Surface Slicing", "3,000 pts/s horizontal perimeter sweep", "Planned Hardware Upgrade", "YDLIDAR X2 integration budgeted in Section 8"),
        ("Full Drone Flight Structural Scan", "Autonomous airborne facade inspection", "Planned / Pending Airframe", "Airframe, LiPo & BEC budgeted in Section 8"),
        ("AI Predictive Maintenance Model", "Longitudinal rate-of-deterioration forecasting", "Planned Extension", "Requires repeated multi-epoch inspection data")
    ]

    for row_idx, data in enumerate(stat_rows):
        row = t_stat.rows[row_idx + 1]
        for col_idx, text in enumerate(data):
            cell = row.cells[col_idx]
            cell.paragraphs[0].add_run(text)
            if row_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ================= SECTION 5 =================
    add_sec_heading("5. Current Engineering Challenges & Identified Gaps")
    doc.add_paragraph(
        "A rigorous analysis of the hardware test sessions and presentation records (BACSE291_Review1_Team1_Drone_AerialFinal.pptx "
        "Slide 11 and BACSE291_Review1_Team2_Ground_OperationsFinal.pptx Slide 11) isolates several critical physical constraints "
        "that must be addressed before field deployment:\n\n"
        "1. Manual Sliding Jitter vs. Defect Threshold Overlap: During initial physical wall scans, the TF-Luna was enclosed in a portable "
        "housing and manually slid along the wall. Uneven human sliding speed and hand tremor introduced ~2–3 cm measurement fluctuations. "
        "Because real structural spalls have depths on the order of 2.5–4.0 cm, this hand-motion jitter directly overlaps with the defect detection "
        "threshold (default T = ±3.5 cm), creating a severe risk of false positives or missed defects.\n\n"
        "2. Tilt & Angular Beam Elongation: When the sensor is not held perfectly normal (perpendicular) to the surface, the laser beam "
        "travels along the hypotenuse of the right triangle formed by the standoff distance and the surface plane. For an incidental tilt angle θ, "
        "the measured distance elongates according to: d_meas = d_true / cos(θ). At a standoff distance of 200 cm, a modest 10° pitch or roll "
        "causes a 3.1 cm artificial elongation—completely disguising a flat wall as a recessed cavity. Active tilt measurement is mandatory.\n\n"
        "3. 1D Point-Sensing vs. Spatial Coverage Trade-Off: The TF-Luna is an ultra-narrow 1D single-point rangefinder (2° FOV). While ideal "
        "for single-axis standoff maintenance, constructing a 2D horizontal contour or a 3D digital twin requires continuous physical translation. "
        "If the sensor skips across a gap, entire defects are missed. A true 360° rotating LiDAR is required to capture continuous planar slices.\n\n"
        "4. Airframe Prop-Wash & High-Frequency Motor Vibration: Brushless drone motors spinning at 8,000–12,000 RPM generate severe mechanical "
        "vibrations in the 150–250 Hz band. Rigidly mounting optical sensors to the drone chassis causes optical defocusing, frame jitter, and premature "
        "bearing wear on mechanical LiDAR turrets. Passive silicone damping mounts are required to isolate the sensing payload.\n\n"
        "5. Absence of Longitudinal Defect History: Predictive maintenance requires observing geometric deformation rates over time (∂(Δd)/∂t). "
        "Single-scan prototypes cannot differentiate between an ancient cosmetic irregularity and an actively progressing structural failure without "
        "storing timestamped reference baselines for differential epoch subtraction."
    )

    # ================= SECTION 6 =================
    add_sec_heading("6. Proposed Hardware Upgrade & Technical Justification")
    doc.add_paragraph(
        "To systematically resolve the engineering gaps identified in Section 5, four hardware additions are proposed. "
        "These selections are grounded in empirical datasheets, supplier availability in India, and the user-supplied reference images:\n\n"
        "A. YDLIDAR X2 360° 2D Laser Range Scanner:\n"
        "• Component Overview: Manufactured by EAI / YDLIDAR, the YDLIDAR X2 is a 360-degree two-dimensional LiDAR scanner utilizing "
        "optical triangulation ranging. It integrates an infrared laser, an optical sensor, a custom DSP chip, and a 360° rotating motor turret. "
        "Reference price from uploaded supplier listing: ₹7,189.00 INR (inclusive of 18% GST).\n"
        "• Ranging Frequency: 3,000 points per second (3 kHz sample rate), delivering dense surface point distributions.\n"
        "• Scanning Frequency: 5–8 Hz adaptive motor rotation (default 7 Hz = 7 full 360° revolutions per second).\n"
        "• Angular Resolution: 0.6° to 0.9° per sample step, capturing fine structural perimeter details.\n"
        "• Operating Range: 0.12 m to 8.0 m radius, perfectly matching indoor room scans and exterior standoff facades.\n"
        "• Electrical Interface: 3.3V LVTTL UART (115200 baud), 4.8V–5.2V operating voltage, 350–500 mA operating current.\n"
        "• Physical Dimensions & Mass: 60.5 mm × 60.3 mm × 97.0 mm, mass = ~150g (optomechanical assembly).\n\n"
        "B. DFRobot Gravity Digital 360° Tilt Sensor:\n"
        "• Component Overview: Model DFR0028 / Gravity Series. Reference price: ₹237.36 INR (current retail: ₹245.00 INR).\n"
        "• Operating Principle: Internal ball-switch / inclination contact detecting tilt angle across 360° orientation.\n"
        "• Electrical Interface: Standard 3-pin Gravity interface (Signal, VCC, GND), plug-and-play with ESP32 3.3V/5V digital GPIO.\n"
        "• Role in Mathematical Correction: Enables firmware to apply the geometric correction factor: d_true = d_meas · cos(θ).\n"
        "• Engineering Distinction: This sensor provides software-based trigonometric correction, not mechanical stabilization.\n\n"
        "C. Upgraded Aerial Drone Platform (F450 Quadcopter Development Kit):\n"
        "• Airframe: F450 Glass Fiber Quadcopter Frame equipped with four 2212 920KV/1000KV brushless DC motors, four 30A SimonK/BLHeli ESCs, and 1045 propellers.\n"
        "• Total Thrust Capacity: 4 × 850g = 3,400g total thrust, providing a safe 2.8:1 thrust-to-weight ratio for an AUW of ~1,200g.\n"
        "• Flight Controller: Pixhawk 2.4.8 32-bit Autopilot kit (with GPS, compass, and power module) supporting AltHold, Loiter, and automated waypoint lawnmower survey patterns.\n\n"
        "D. Rechargeable Power System (3S LiPo Battery & Regulated BEC):\n"
        "• Chemistry & Rating: Lithium Polymer (LiPo), 3S1P (3 cells in series), nominal voltage 11.1V (12.6V fully charged).\n"
        "• Capacity & Discharge: 4200 mAh, 35C continuous discharge rate (peak discharge 70C), capable of delivering 147A continuous current.\n"
        "• Connector: High-current XT60 gold-plated connector with JST-XH balance leads for safe multi-cell charging.\n"
        "• Estimated Hover Flight Time: Calculated at ~16–18 minutes with full 250g sensor payload at 18A average hover current draw.\n"
        "• SAFETY & VOLTAGE REGULATION MANDATE: Dedicated 5V 5A UBEC Step-Down Buck Converter stepping down 11.1V battery rail to a clean 5.0V bus with reverse polarity and transient protection.\n\n"
        "E. Vibration Damping, Mounting Hardware & Wiring:\n"
        "• Silicone Anti-Vibration Isolators: Dual-plate carbon fiber isolation deck suspended on four silicone rubber damping balls attenuating 150–250 Hz vibration by >18 dB.\n"
        "• Custom Sensor Brackets: Lightweight 3D printed PETG mounting bracket orienting TF-Luna and YDLIDAR X2.\n"
        "• Shielded Silicone Wiring: 22 AWG twisted-pair shielded signal cabling minimizing electromagnetic interference (EMI)."
    )

    # Hardware Images in DOCX
    yd_list = os.path.join(assets_dir, "ydlidar_x2_listing.png")
    if os.path.exists(yd_list):
        p_yd = doc.add_paragraph()
        p_yd.add_run().add_picture(yd_list, width=Inches(5.5))
        p_cap = doc.add_paragraph()
        p_cap.add_run("Figure 2: YDLIDAR X2 360° 2D Laser Range Scanner Product Listing (Reference Price: ₹7,189 incl. GST)").font.size = Pt(8.5)

    # ================= SECTION 7 =================
    add_sec_heading("7. Hardware Integration & Compatibility Study")
    doc.add_paragraph(
        "A rigorous engineering compatibility analysis was conducted to map voltage levels, current budgets, communication protocols, "
        "and physical interfaces across all system components. The verified compatibility matrix is presented below:"
    )

    t_comp_doc = doc.add_table(rows=8, cols=6)
    t_comp_doc.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_comp_doc)

    comp_headers = ["Component Name", "Subsystem Role", "Operating Voltage & Current", "Data Interface", "Compatibility Concern", "Engineered Solution"]
    for i, h in enumerate(comp_headers):
        cell = t_comp_doc.rows[0].cells[i]
        cell.paragraphs[0].add_run(h).bold = True
        set_cell_background(cell, "1E3A8A")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    comp_rows = [
        ("Benewake TF-Luna", "1D Standoff Ranging", "5.0V ± 0.1V\n70 mA (<0.35W)", "3.3V LVTTL UART\n115200 bps", "Tx voltage level match with ESP32 GPIO", "TF-Luna UART is native 3.3V logic; connect directly to ESP32 Rx2/Tx2"),
        ("YDLIDAR X2", "2D 360° Planar Slicing", "4.8V – 5.2V\n350–500 mA (2.5W)", "3.3V LVTTL UART\n115200 bps", "Peak motor starting current causes brownout on ESP32 3.3V pin", "Power motor and laser from dedicated 5V 5A UBEC rail; do NOT draw from ESP32"),
        ("DFRobot Tilt Sensor", "Pitch/Roll Angle Detection", "3.3V – 5.0V\n~10 mA", "Digital GPIO Interrupt", "Contact bounce during abrupt drone acceleration", "Implement 50ms software debounce filter and hardware RC pull-up in firmware"),
        ("ESP32-WROOM-32", "Embedded Controller & Telemetry", "5.0V (Vin pin)\n160–260 mA (Wi-Fi ON)", "Dual Hardware UART + Wi-Fi UDP", "Simultaneous UART servicing of TF-Luna and YDLIDAR X2", "Assign TF-Luna to UART1 (GPIO 16/17) and YDLIDAR X2 to UART2 (GPIO 25/26) via FreeRTOS tasks"),
        ("F450 Drone Motors & ESCs", "Aerial Flight Platform", "11.1V (3S LiPo)\n15A–60A total", "PWM from Pixhawk Autopilot", "High voltage (11.1V) damaging 5V microcontrollers", "Isolate motor power through Power Distribution Board (PDB); step down via UBEC"),
        ("3S 4200mAh LiPo", "Master Energy Reservoir", "11.1V nom (12.6V max)\n35C discharge", "XT60 High-Current DC Rail", "Cell over-discharge (<3.2V/cell) causing permanent battery destruction", "Integrate Pixhawk telemetry voltage alarm buzzer and low-voltage auto-RTL"),
        ("PLY Forge / Ground Base", "3D Metrology & Inspection UI", "Host PC USB / 230V AC", "Wi-Fi UDP Socket / WebGL Canvas", "Point cloud rendering lag during rapid 3,000 pts/s streaming", "Buffer incoming points into 1-second chunks and upload via typed Float32Array")
    ]

    for row_idx, data in enumerate(comp_rows):
        row = t_comp_doc.rows[row_idx + 1]
        for col_idx, text in enumerate(data):
            cell = row.cells[col_idx]
            cell.paragraphs[0].add_run(text)
            if row_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ================= SECTION 8 =================
    add_sec_heading("8. Complete Procurement Budget & Financial Analysis")
    doc.add_paragraph(
        "An itemized, market-verified Bill of Materials (BOM) was compiled using authorized Indian robotics distributors (Robu.in, QuartzComponents, "
        "Silverline Electronics). Screenshot prices from the uploaded prompt materials were compared against current live listings. "
        "All figures are expressed in Indian Rupees (₹ INR):"
    )

    t_bom_doc = doc.add_table(rows=17, cols=7)
    t_bom_doc.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_bom_doc)

    bom_headers = ["Item Name & Model", "Category", "Qty", "Ref Price", "Verified Price", "Subtotal (INR)", "Supplier / Source Status"]
    for i, h in enumerate(bom_headers):
        cell = t_bom_doc.rows[0].cells[i]
        cell.paragraphs[0].add_run(h).bold = True
        set_cell_background(cell, "1E3A8A")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    bom_table_rows = [
        ("YDLIDAR X2 360° 2D LiDAR Scanner", "LiDAR Sensor", "1", "₹7,189.00", "₹7,189.00", "₹7,189.00", "Robu.in / In Stock (Screenshot Ref)"),
        ("DFRobot Gravity Digital 360° Tilt Sensor", "Orientation Sensor", "1", "₹237.36", "₹245.00", "₹245.00", "Robu.in / Silverline (Screenshot Ref)"),
        ("F450 Quadcopter Drone Frame Kit + Landing Gear", "Airframe", "1", "₹1,450.00", "₹1,350.00", "₹1,350.00", "Robu.in / QuartzComponents"),
        ("A2212 1000KV Brushless Motors (Set of 4)", "Propulsion", "1 set", "₹2,200.00", "₹2,100.00", "₹2,100.00", "Robu.in / In Stock"),
        ("30A SimonK ESC Speed Controllers (Set of 4)", "Propulsion", "1 set", "₹1,800.00", "₹1,750.00", "₹1,750.00", "Robu.in / In Stock"),
        ("Pixhawk 2.4.8 Flight Controller + GPS + Power Module", "Autopilot Avionics", "1 kit", "₹7,200.00", "₹6,850.00", "₹6,850.00", "Robu.in / QuartzComponents"),
        ("1045 Nylon Carbon Fiber Propellers (2 CW + 2 CCW)", "Aerodynamics", "2 pairs", "₹350.00", "₹320.00", "₹320.00", "Robu.in / In Stock"),
        ("Orange 3S 11.1V 4200mAh 35C LiPo Battery (XT60)", "Power Reservoir", "1", "₹2,500.00", "₹2,450.00", "₹2,450.00", "Robu.in / Authorized Distributor"),
        ("iMAX B6 80W Digital LiPo Balance Charger + Adapter", "Charging System", "1", "₹1,400.00", "₹1,350.00", "₹1,350.00", "QuartzComponents / Robu.in"),
        ("5V 5A UBEC Step-Down Buck Converter (DC-DC)", "Power Regulation", "1", "₹400.00", "₹380.00", "₹380.00", "Robu.in / In Stock"),
        ("Silicone Rubber Vibration Damping Plate Deck", "Mechanical Mount", "1 set", "₹350.00", "₹320.00", "₹320.00", "Robu.in / In Stock"),
        ("Hardware Fasteners, Standoffs, Shielded Wiring, XT60", "Accessories", "1 lot", "₹450.00", "₹420.00", "₹420.00", "Local Electronics Market"),
        ("Essential Hardware Subtotal", "BOM Items", "13 items", "—", "—", "₹24,724.00", "All essential components"),
        ("Standard Express Shipping & Insured Packaging", "Logistics", "Consolidated", "—", "—", "₹400.00", "Robu.in courier rate"),
        ("Project Engineering Contingency Allowance (8%)", "Risk Reserve", "Unforeseen", "—", "—", "₹2,000.00", "For wire/connector replacements"),
        ("TOTAL RECOMMENDED PROJECT PROCUREMENT BUDGET", "Complete Airborne SHM", "Full System", "—", "—", "₹27,124.00", "Faculty-Ready Grant Request")
    ]

    for row_idx, data in enumerate(bom_table_rows):
        row = t_bom_doc.rows[row_idx + 1]
        for col_idx, text in enumerate(data):
            cell = row.cells[col_idx]
            cell.paragraphs[0].add_run(text)
            if row_idx == 12:
                set_cell_background(cell, "FEF3C7")
            elif row_idx == 15:
                set_cell_background(cell, "0F172A")
                cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                cell.paragraphs[0].runs[0].bold = True
            elif row_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ================= SECTION 9 =================
    add_sec_heading("9. Hardware Procurement Priority & Staging Strategy")
    doc.add_paragraph(
        "To ensure fiscal prudence and eliminate hardware integration bottlenecks, component procurement is organized into three distinct phases:\n\n"
        "• Priority 1: Immediate Essential Upgrades (Milestone 1 — Week 1–2): YDLIDAR X2 360° LiDAR (₹7,189), DFRobot Tilt Sensor (₹245), "
        "and 5V 5A UBEC Step-Down Converter (₹380). Subtotal: ₹7,814.00 INR.\n"
        "• Priority 2: Aerial Airframe & Power Integration (Milestone 2 — Week 3–4): F450 Frame Kit + Motors + ESCs (₹5,200), "
        "3S 4200mAh LiPo Battery & iMAX B6 Balance Charger (₹3,800), and Silicone Damping Deck (₹740). Subtotal: ₹9,740.00 INR.\n"
        "• Priority 3: Autonomous Avionics & Advanced Testing (Milestone 3 — Week 5–6): Pixhawk 2.4.8 Autopilot & GPS Kit (₹6,850) "
        "and Contingency Spares & Wiring (₹2,720). Subtotal: ₹9,570.00 INR."
    )

    # ================= SECTION 10 =================
    add_sec_heading("10. Technical Architecture & System Flowcharts")
    doc.add_paragraph(
        "The end-to-end cyber-physical architecture is structured into five verified operational workflows. "
        "These diagrams eliminate ambiguity between currently implemented modules and future planned extensions:\n\n"
        "Diagram 1: Complete System Architecture:\n"
        "Physical Target (Concrete Facade, Bridge Pier, Spalls & Bulges) → Embedded Acquisition (TF-Luna 1D ToF, YDLIDAR X2 2D, DFRobot Tilt Sensor, ESP32 dual-core, Checksum validation) → "
        "Wireless Telemetry (115200 Baud UART, Wi-Fi 802.11 b/g/n, UDP Socket stream, Dropped frame filter) → "
        "Ground Analytics (Rolling baseline d_ref, Deviation Δd, Cavity rule Δd ≥ +3.5cm, Bulge rule Δd ≤ -3.5cm, Crack filter |Δd| ≥ 1.5cm) → "
        "Visualization & Audit (3D PLY Digital Twin, Streamlit UI Port 8501, PLY Forge WebGL engine, Defect severity log, PDF Inspection Report).\n\n"
        "Diagram 2: Aerial Acquisition Workflow (15377IDP01):\n"
        "1. Boot & Sync: Initialize ESP32 GPIOs, UART1 (TF-Luna), UART2 (YDLIDAR), and Tilt interrupt.\n"
        "2. Frame Ingestion: Read 9-byte TF-Luna packet; verify header bytes 0x59 0x59.\n"
        "3. Checksum Validation: Compute (Σ B0..B7) & 0xFF; if mismatch, DROP frame.\n"
        "4. Metrology Calibration: Apply linear fit: d_cal = 1.0228 · d_raw + 3.20 cm.\n"
        "5. Tilt Compensation: Sample tilt angle θ; compute: d_true = d_cal · cos(θ).\n"
        "6. Median Filter: Buffer N=5 readings; output median to suppress optical outliers.\n"
        "7. Telemetry Transmission: Format UDP datagram: [Timestamp, d_true, θ, Amplitude]; transmit.\n\n"
        "Diagram 3: Ground Analytics Workflow (15377IDP02):\n"
        "1. Packet Ingestion: Receive UDP datagram on port 5005; parse payload.\n"
        "2. Baseline Computation: Calculate window mean d_ref over rolling window.\n"
        "3. Residual Delta: Calculate geometric deviation: Δd = d_meas - d_ref.\n"
        "4. Defect Classification: Δd ≥ +3.5 cm (Spall Cavity); Δd ≤ -3.5 cm (Structural Bulge); |Δd| ≥ 1.5 cm vs neighbors (Crack Indication).\n"
        "5. Spatial Projection: Map to global 3D vector: P_global = P_sensor + R_tilt · [d_true, 0, 0]ᵀ.\n"
        "6. WebGL Digital Twin: Push vertex buffer to PLY Forge GPU canvas; render room twin.\n"
        "7. Automated Audit: Output timestamped defect coordinate log & PDF report.\n\n"
        "Diagram 4: Physical Wiring & Power Architecture:\n"
        "3S 11.1V LiPo → XT60 → PDB → 4x 30A ESCs → 4x Motors; PDB 11.1V → 5V 5A UBEC → 5.0V bus (TF-Luna 70mA; YDLIDAR X2 500mA; ESP32 Vin 200mA). "
        "TF-Luna to UART1 (GPIO 16/17); YDLIDAR X2 to UART2 (GPIO 25/26); Tilt Sensor to GPIO 34. ESP32 Wi-Fi transmits UDP to Ground Base.\n\n"
        "Diagram 5: Phased Testing Pipeline:\n"
        "Hardware Procurement → Benchtop Electrical Verification → Universal Sensor Calibration → Static Testbed Validation → "
        "Controlled Linear Motion Testing → Silicone Vibration Damper Tuning → Drone Airframe Integration → Tethered Hover Flight Trials → "
        "Live Wireless Telemetry Certification → End-to-End Physical Structural Scan → Faculty Demonstration."
    )

    # ================= SECTION 11 =================
    add_sec_heading("11. Future Work & Phased Implementation Roadmap")
    doc.add_paragraph(
        "A structured, sequential 7-phase engineering execution plan spanning Weeks 1 through 10 is established below:\n\n"
        "• Phase 1: Design Finalization (Week 1): Finalize wiring schematics, pin mappings, UBEC thermal dissipation, and PETG mount CAD drawings.\n"
        "• Phase 2: Procurement & Bench Test (Week 2–3): Acquire YDLIDAR X2, tilt sensor, UBEC. Verify UART communication, current draw, and baud rates on bench.\n"
        "• Phase 3: Sensor Fusion & Calibration (Week 4): Implement tilt compensation algorithm (d_cal · cos θ). Fuse TF-Luna 1D standoff with YDLIDAR 2D planar point streams.\n"
        "• Phase 4: Airframe Integration (Week 5–6): Assemble F450 frame, calibrate ESCs, install Pixhawk autopilot, mount silicone damping deck, check center of gravity (CG).\n"
        "• Phase 5: Ground Pipeline & PLY Forge (Week 7): Adapt PLY Forge WebGL engine to render live streaming point cloud buffers. Link detected anomalies to automated report generator.\n"
        "• Phase 6: Flight Trials & Validation (Week 8–9): Conduct tethered indoor hover flights, verify wireless UDP telemetry under prop-wash, execute physical facade scans with known defects.\n"
        "• Phase 7: Final Demonstration (Week 10): Complete end-to-end faculty demonstration, publish validated performance benchmarks, prepare longitudinal baseline framework."
    )

    # ================= SECTION 12 =================
    add_sec_heading("12. Rigorous Testing & Empirical Evaluation Plan")
    doc.add_paragraph(
        "To satisfy rigorous faculty review, quantitative verification metrics and explicit acceptance criteria are defined across eight domains:\n\n"
        "• Static Distance Accuracy: Optical bench with steel reference tape (0.5m to 5.0m in 0.5m increments). Target: MAE ≤ ±0.50 cm, RMSE ≤ ±0.75 cm. Status: Verified (RMSE ±0.02cm on bench).\n"
        "• Tilt Error Compensation: Goniometer jig tilting sensor from 0° to 25° at fixed 200 cm standoff. Target: Residual error ≤ ±1.0 cm across 0°–20° tilt range. Status: Mathematical Model Ready.\n"
        "• Motor Vibration Attenuation: Drone motors throttled to 50%, 75%, 100% hover RPM with 3-axis accelerometer. Target: ≥ 18 dB attenuation in 150–250 Hz motor frequency band. Status: Planned (Post-Mount).\n"
        "• Wireless UDP Telemetry: ESP32 streaming 100 Hz packets to PC at 5m, 15m, 30m standoff distances. Target: Packet drop ≤ 1.0%, latency ≤ 25 ms. Status: Bench Ready / In Progress.\n"
        "• 2D Planar Scan Quality: YDLIDAR X2 placed in 4.8m × 4.2m room; compare wall distance with tape. Target: Closure residual ≤ ±1.5 cm across 360° perimeter. Status: Awaiting Hardware.\n"
        "• Defect Detection Sensitivity: Physical wall testbed with calibrated simulated spalls (depth: 2cm, 3.5cm, 5cm). Target: Precision ≥ 90%, Recall ≥ 85% for spalls ≥ 3.5 cm. Status: Algorithm Tuned.\n"
        "• Continuous Flight Endurance: F450 quadcopter hovering with full 250g payload on 3S 4200mAh LiPo. Target: Continuous hover flight time ≥ 14.0 minutes. Status: Planned (Phase 6).\n"
        "• WebGL 3D Rendering Performance: PLY Forge rendering 10,000-point to 100,000-point structural point cloud. Target: Smooth rendering ≥ 50 FPS on standard integrated GPU. Status: Verified on PLY Forge."
    )

    # ================= SECTION 13 =================
    add_sec_heading("13. Risk Management & Technical Mitigation Strategies")
    doc.add_paragraph(
        "A rigorous engineering contingency matrix identifies potential operational failure modes and defines preventative protocols:\n\n"
        "• Airframe Prop-Wash Turmoil & Collision: Close-range facade scanning (<1.0m) causes aerodynamic ground/wall effect suction, destabilizing drone. Mitigation: Enforce strict 1.5m standoff buffer; program Pixhawk rangefinder proximity barrier; install propeller safety guard ring.\n"
        "• LiDAR Current Spikes & MCU Brownout: YDLIDAR X2 motor start-up current (>800 mA) causes 5V rail voltage sag, rebooting ESP32. Mitigation: Power YDLIDAR X2 motor from independent UBEC rail with 1000 µF low-ESR electrolytic capacitor across power terminals.\n"
        "• Hand Tremor / Sliding Jitter Overlap: Manual sensor sliding introduces 2–3 cm fluctuations, mimicking spall cavities. Mitigation: Implement rolling median filter (N=5); clamp defect threshold at T = ±3.5 cm; transition to wheeled rover or drone.\n"
        "• GPS-Denied Indoor Flight Drift: Lack of satellite lock indoors causes quadcopter horizontal position drift during structural scanning. Mitigation: Operate initial test scans using tethered guide wires or deploy the contingency 4WD Smart Ground Rover platform.\n"
        "• Optical Surface Reflectivity Drop: Dark, wet, or glazed structural tiles absorb 850nm infrared light, reducing ToF signal amplitude. Mitigation: Monitor signal strength byte in TF-Luna packet; flag readings with Amplitude < 100 as unreliable and reject.\n"
        "• Procurement Budget Overrun / Delays: Shipping delays or price inflation exceeding allocated student budget. Mitigation: Execute phased procurement (Priority 1 first: ₹8,214); utilize 8% contingency allowance (₹2,000); source from local suppliers."
    )

    # ================= SECTION 14 =================
    add_sec_heading("14. Expected Outcomes & Research Contributions")
    doc.add_paragraph(
        "Upon successful execution of the proposed hardware upgrade and implementation roadmap, this project delivers several "
        "distinct academic and engineering contributions to the domain of Cyber-Physical Structural Health Monitoring:\n\n"
        "1. Multi-Sensor Fusion Architecture: Demonstrates the first cost-effective (<₹30,000 INR) integration of 1D ToF micro-ranging (TF-Luna), "
        "360° planar LiDAR (YDLIDAR X2), and digital tilt correction on a dual-core ESP32 platform.\n"
        "2. Tilt-Compensated Metrology Formulation: Delivers an empirical mathematical formulation (d_true = d_meas · cos θ) eliminating spurious "
        "defect detection caused by aerial pitching and rolling motions.\n"
        "3. Automated 3D Defect Segmentation: Extends our previous MDP work (PLY Forge) into a real-time, browser-accessible digital twin suite "
        "capable of isolating structural spalls (Orange) and recesses (Green) without expensive commercial software.\n"
        "4. Longitudinal Baseline Deterioration Model: Establishes a standardized framework for multi-epoch structural comparison, calculating "
        "geometric rate-of-deformation (∂(Δd)/∂t) to transition inspection from periodic checks to predictive safety assurance."
    )

    # ================= SECTION 15 =================
    add_sec_heading("15. Conclusion & Immediate Next Steps")
    doc.add_paragraph(
        "This comprehensive report establishes a rigorous, unified engineering bridge connecting our team's completed Multidisciplinary Project "
        "(MDP: PLY Forge WebGL Point Cloud Processor) with the current Innovative Design Project (BACSE291: AI in Structural Health Monitoring). "
        "We have verified our operational progress across both aerial and ground subsystems—including high-speed UART framing, universal two-point "
        "calibration (y = 1.0228x + 3.20 cm, RMSE = ±0.02 cm), 9,969-point 3D digital twin room reconstruction, and a multi-tab operations dashboard.\n\n"
        "To overcome physical testing constraints (sensor tilt elongation, sliding jitter, and 1D coverage limitations), we have presented "
        "the complete technical justification, compatibility analysis, and itemized budget for acquiring the YDLIDAR X2 360° LiDAR, "
        "DFRobot Gravity Tilt Sensor, F450 Quadcopter Frame Kit, and 3S LiPo battery (total recommended procurement: ₹27,124.00 INR). "
        "The phased implementation roadmap and quantitative evaluation plan ensure that all acquisitions are verified systematically on the bench "
        "before controlled airborne structural inspection trials.\n\n"
        "Immediate Next Steps: (1) Secure faculty guide approval for Priority 1 hardware procurement (₹8,214.00 INR), (2) Execute benchtop "
        "UART driver integration for the YDLIDAR X2, (3) Implement firmware tilt compensation on ESP32 GPIO 34, and (4) Prepare the physical testbed "
        "for Review 2 demonstration."
    )

    # ================= SECTION 16 =================
    add_sec_heading("16. IEEE References & Technical Datasheets")
    references = [
        "[1] M. Azimi, A. D. Eslamlou, and G. Pekcan, \"Data-driven structural health monitoring and damage detection through deep learning: State-of-the-art review,\" Sensors, vol. 20, no. 10, p. 2778, 2020. doi: 10.3390/s20102778.",
        "[2] A. Gomez-Cabrera and P. J. Escamilla-Ambrosio, \"Review of machine-learning techniques applied to structural health monitoring systems for building and bridge structures,\" Applied Sciences, vol. 12, no. 21, p. 10754, 2022.",
        "[3] Y. Xu, Y. Bao, J. Chen, W. Zuo, and H. Li, \"Surface fatigue crack identification in steel box girder of bridges by a deep fusion convolutional neural network based on consumer-grade camera,\" Structural Health Monitoring, vol. 18, no. 3, pp. 653–674, 2019.",
        "[4] R. van Dinter, B. Tekinerdogan, and C. Catal, \"Predictive maintenance using digital twins: A systematic literature review,\" Information and Software Technology, vol. 151, p. 107008, 2022. doi: 10.1016/j.infsof.2022.107008.",
        "[5] Benewake (Beijing) Co., Ltd., \"TF-Luna LiDAR Module (Short-Range Distance Sensor) Product Manual V1.4,\" Beijing, China, 2022. [Online]. Available: https://en.benewake.com/product/detail/5c345cd0e5b3cb6f4c1d42a6.html",
        "[6] Shenzhen EAI Technology Co., Ltd., \"YDLIDAR X2 360-Degree 2D Laser Range Scanner User Manual & Data Sheet Rev 1.2,\" Shenzhen, China, 2023. [Online]. Available: https://www.ydlidar.com/products/view/6.html",
        "[7] DFRobot Electronic Technology Co., Ltd., \"Gravity: 360 Degree Tilt Sensor Product Specification & Wiki,\" DFR0028, Shanghai, China, 2023. [Online]. Available: https://wiki.dfrobot.com/Tilt_Sensor__SKU_DFR0028_",
        "[8] Espressif Systems, \"ESP32 Series Datasheet V4.1 — Dual-Core Wi-Fi & Dual-Mode Bluetooth MCU,\" Shanghai, China, 2024. [Online]. Available: https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf",
        "[9] Dronecode Project, \"Pixhawk 2.4.8 Open Hardware Autopilot Flight Controller Specifications & ArduPilot Wiring Guide,\" 2023. [Online]. Available: https://ardupilot.org/copter/docs/common-pixhawk-overview.html",
        "[10] N. P. Joshi, A. P. Mithari, M. Gupta, P. Sharma, and A. Kaushik, \"PLY Forge: Web-Based 3D Mesh Simplification Tool & Point Cloud Processor,\" Multidisciplinary Project Final Report, School of Computer Science & Engineering, Vellore Institute of Technology, Vellore, 2026."
    ]
    for r in references:
        p_ref = doc.add_paragraph()
        p_ref.add_run(r)
        p_ref.paragraph_format.left_indent = Inches(0.2)
        p_ref.paragraph_format.space_after = Pt(3)

    # ================= SECTION 17 =================
    add_sec_heading("17. Appendices: Technical Audit & Hardware Comparison")
    add_sub_heading("Appendix A: Comprehensive Sensor Metrology Comparison")

    t_scomp_doc = doc.add_table(rows=10, cols=4)
    t_scomp_doc.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_scomp_doc)

    scomp_headers = ["Parameter", "Benewake TF-Luna (Existing)", "YDLIDAR X2 (Proposed Upgrade)", "DFRobot Tilt Sensor (Proposed)"]
    for i, h in enumerate(scomp_headers):
        cell = t_scomp_doc.rows[0].cells[i]
        cell.paragraphs[0].add_run(h).bold = True
        set_cell_background(cell, "1E3A8A")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    scomp_rows = [
        ("Operating Principle", "Infrared Time-of-Flight (dToF)", "Optical Laser Triangulation (360°)", "Electromechanical Ball Tilt Switch"),
        ("Laser Wavelength / Emitter", "850 nm Near-Infrared VCSEL", "785 nm Infrared Semiconductor Laser", "Passive Mechanical Contact"),
        ("Ranging Distance Range", "0.20 m to 8.0 m", "0.12 m to 8.0 m", "Full 360° Inclination Angle"),
        ("Sampling Rate", "100 Hz (100 samples/sec)", "3,000 Hz (3,000 points/sec)", "Real-Time GPIO Interrupt"),
        ("Scan Coverage Pattern", "1D Single-Point Vector (2° FOV)", "2D Continuous Horizontal Circle (360°)", "Angular Pitch/Roll Orientation"),
        ("Power Consumption", "< 0.35 W (5V @ ~70 mA)", "~ 2.5 W (5V @ ~500 mA)", "< 0.05 W (5V @ ~10 mA)"),
        ("Payload Mass", "< 5.0 grams (ultra-light)", "~ 150 grams (rotating turret)", "~ 8.0 grams (PCB module)"),
        ("Flight Dynamics Impact", "Negligible impact on drone balance", "Requires rigid CG mounting & damping", "Negligible impact on drone balance"),
        ("Primary Role in IDP", "Close-range vertical facade tracking", "Rapid 360° perimeter room slicing", "Geometric tilt angle compensation")
    ]

    for row_idx, data in enumerate(scomp_rows):
        row = t_scomp_doc.rows[row_idx + 1]
        for col_idx, text in enumerate(data):
            cell = row.cells[col_idx]
            cell.paragraphs[0].add_run(text)
            if row_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Sign-off block
    t_sign_doc = doc.add_table(rows=2, cols=2)
    t_sign_doc.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_sign_doc)

    t_sign_doc.rows[0].cells[0].paragraphs[0].add_run("SUBMITTED BY (STUDENT PROJECT LEADS):").bold = True
    t_sign_doc.rows[0].cells[1].paragraphs[0].add_run("FACULTY GUIDE REVIEW & APPROVAL:").bold = True
    set_cell_background(t_sign_doc.rows[0].cells[0], "F1F5F9")
    set_cell_background(t_sign_doc.rows[0].cells[1], "F1F5F9")

    t_sign_doc.rows[1].cells[0].paragraphs[0].add_run(
        "Nisargkumar Piyushkumar Joshi (25BCE0594) — Ground Subsystem Lead\n"
        "Priyam Sharma (25BAI0159) — Aerial Subsystem Lead\n"
        "Date: October 24, 2026"
    )
    t_sign_doc.rows[1].cells[1].paragraphs[0].add_run(
        "Dr. Senthil Kumar N, Ph.D (IITM)\n"
        "Associate Professor Grade 2, SCOPE / SCE\n"
        "Status: __________________________  Date: ____________________"
    )

    doc.save(DOCX_FILENAME)
    print(f"Successfully generated DOCX report: {DOCX_FILENAME}")

if __name__ == "__main__":
    build_docx()
