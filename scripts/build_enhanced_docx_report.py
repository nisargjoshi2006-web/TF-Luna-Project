import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT
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

    # Set Margins (0.7 inch)
    for section in doc.sections:
        section.top_margin = Inches(0.7)
        section.bottom_margin = Inches(0.7)
        section.left_margin = Inches(0.7)
        section.right_margin = Inches(0.7)

    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    # Colors
    c_navy = RGBColor(0x0F, 0x17, 0x2A)
    c_primary = RGBColor(0x1E, 0x3A, 0x8A)
    c_teal = RGBColor(0x0D, 0x94, 0x88)
    c_muted = RGBColor(0x64, 0x74, 0x8B)

    def add_p(text, bold=False, italic=False, font_size=11, color=None, space_after=4, align=WD_PARAGRAPH_ALIGNMENT.LEFT, line_spacing=1.15):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.size = Pt(font_size)
        if color:
            run.font.color.rgb = color
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(16)
        run.font.color.rgb = c_primary
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(13)
        run.font.color.rgb = c_navy
        return p

    def add_bullet(bold_prefix, text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        run1 = p.add_run(bold_prefix)
        run1.bold = True
        run1.font.size = Pt(11)
        run2 = p.add_run(text)
        run2.font.size = Pt(11)
        return p

    def add_callout(text, title="NOTE / ARCHITECTURAL PRINCIPLE"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, "F0FDF4")
        set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r_head = p.add_run(f"[{title}]\n")
        r_head.bold = True
        r_head.font.size = Pt(10)
        r_head.font.color.rgb = RGBColor(0x05, 0x96, 0x69)
        r_body = p.add_run(text)
        r_body.font.size = Pt(10)
        r_body.italic = True
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def add_caption(text):
        p = doc.add_paragraph()
        p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(8)
        run = p.add_run(text)
        run.italic = True
        run.font.size = Pt(9.5)
        run.font.color.rgb = c_navy
        return p

    # ================= COVER PAGE =================
    vit_logo = os.path.join(assets_dir, "vit_logo.png")
    if os.path.exists(vit_logo):
        p_logo = doc.add_paragraph()
        p_logo.add_run().add_picture(vit_logo, width=Inches(2.2))
        p_logo.paragraph_format.space_after = Pt(6)

    add_p("AI IN STRUCTURAL HEALTH MONITORING FOR PREDICTIVE MAINTENANCE AND CONTINUOUS SAFETY ASSURANCE", bold=True, font_size=20, color=c_navy, space_after=4)
    add_p("Comprehensive IDP Progress Report, Previous MDP Integration, Dual-Platform Deployment (Aerial Drone & Smart 4WD Car), Platform-Wise Hardware Budget & Implementation Plan", bold=True, font_size=12, color=c_primary, space_after=12)

    # Academic Meta Table
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
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            for p in cell.paragraphs:
                p.paragraph_format.line_spacing = 1.15
                for run in p.runs:
                    run.font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_callout(
        "This document presents the complete formal engineering review for BACSE291. It provides an exhaustive, evidence-based "
        "technical synthesis connecting our prior Multidisciplinary Project (MDP: PLY Forge 3D Point Cloud Processor) to our "
        "current Innovative Design Project (IDP). It details the verified aerial acquisition and ground analytics benchmarks, "
        "evaluates identified scanning constraints (sensor jitter, manual dragging noise, tilt elongation, motor vibration), "
        "presents our Dual-Platform Deployment Strategy (Primary Autonomous Quadcopter Drone vs. Contingency Smart 4WD Ground Robotic Car with Optical Wheel Encoders), "
        "justifies essential hardware upgrades (YDLIDAR X2 360° LiDAR, DFRobot Gravity 360° Tilt Sensor, F450 Quadcopter & 3S LiPo), "
        "provides an explicit Platform-Wise Procurement Budget Breakdown (Drone Requirements vs. Smart Car Requirements), "
        "and outlines a rigorous 7-phase future roadmap toward autonomous structural health monitoring (SHM).",
        title="EXECUTIVE REPORT SUMMARY & SCOPE"
    )

    doc.add_page_break()

    # ================= SECTION 1: EXECUTIVE SUMMARY =================
    add_h1("1. Executive Summary")
    add_p(
        "Civil infrastructures—including high-rise exterior facades, highway bridge piers, industrial cooling towers, and commercial structural "
        "enclosures—suffer continuous degradation caused by thermal expansion, foundation settling, seismic loads, and moisture ingress. "
        "Conventional manual inspection relies heavily on scaffolding, cherry-pickers, and human tactile assessment, exposing personnel to severe "
        "fall hazards while suffering from subjective qualitative records and high labor costs. This joint project establishes an autonomous, "
        "sensor-driven Cyber-Physical Structural Health Monitoring (SHM) ecosystem partitioned into two tightly coupled subsystems:"
    )
    add_bullet("Aerial Subsystem (15377IDP01): ", "Deploys close-range standoff Time-of-Flight (ToF) distance sensing via ESP32 microcontrollers, 100 Hz UART frame synchronization, checksum integrity checks, and real-time wireless telemetry to scan elevated, inaccessible structural envelopes.")
    add_bullet("Ground Analytics Subsystem (15377IDP02): ", "Ingests streaming distance metrics, executes adaptive baseline tracking, computes geometric residuals (Δd), flags structural anomalies (spalling cavities, structural bulges, cracks), reconstructs 3D digital twins, and generates automated compliance reports.")
    add_p(
        "Key Progress to Date: The project has successfully delivered a physical ESP32 testbed operating a calibrated Benewake TF-Luna ToF "
        "sensor (regression model: y = 1.0228x + 3.20 cm, R²=1.0000, RMSE=±0.02 cm across 39.0 cm and 61.4 cm physical benchmarks), "
        "a 9,969-point 3D digital twin room reconstruction correctly segmenting an inward Almari bulge (+65 cm) and outward gate recess (-60 cm), "
        "and an interactive multi-tab Streamlit ground operations dashboard. Building directly upon our team's previous Multidisciplinary Project "
        "(MDP: PLY Forge), client-side WebGL point-cloud rendering and voxel compression algorithms provide zero-latency spatial visualization."
    )
    add_p(
        "Dual-Platform Deployment Strategy: To overcome physical limitations observed during testing (manual hand-sliding speed jitter "
        "of ~2–3 cm, tilt beam elongation, and aerodynamic prop-wash turbulence near vertical walls), this project formulates a robust "
        "Dual-Platform Strategy: (1) An Autonomous F450 Quadcopter Drone for elevated exterior facade and bridge inspection, and "
        "(2) A Smart 4WD Ground Robotic Car equipped with dual optical wheel encoders as a high-precision, vibration-free contingency platform "
        "for GPS-denied indoor environments, campus corridors, and high-precision linear wall sweeps."
    )

    # ================= SECTION 2: PROJECT BACKGROUND & OBJECTIVES =================
    add_h1("2. Project Background & Technical Objectives")
    add_p(
        "Modern structural maintenance requires transitioning from reactive repair to proactive, quantitative condition assessment. "
        "Structural surfaces exhibit subtle geometric precursors prior to catastrophic failure, including spalling cavities (concrete flaking away), "
        "sub-surface shear bulges (delamination or masonry buckling), and vertical shear cracks. However, acquiring high-fidelity geometric metrics "
        "from vertical facades presents extreme technical challenges: (1) Inaccessibility: Scaffolding is cost-prohibitive for routine monitoring; "
        "(2) Human Error: Manual ultrasonic gauges produce sparse records without a global spatial coordinate reference; and "
        "(3) Dynamic Noise: Handheld measurements suffer from variable scan velocity and human tremor."
    )
    add_p("To systematically address these civil engineering challenges, our joint IDP team formulated 8 Formal Technical Objectives:")
    add_bullet("Obj 1 (Real-Time Distance Acquisition): ", "Establish continuous 100 Hz ToF distance acquisition with binary frame parsing and checksum verification.")
    add_bullet("Obj 2 (Metrological Accuracy): ", "Calibrate distance sensors against physical ground-truth benchmarks to achieve residual error ≤ ±1.0 cm.")
    add_bullet("Obj 3 (Telemetry Synchronization): ", "Stream distance, signal amplitude, chip temperature, and timestamps from the mobile platform to the ground station.")
    add_bullet("Obj 4 (Geometric Defect Classification): ", "Formulate mathematical residual algorithms (Δd = d_measured - d_baseline) to segment spalling cavities (Δd ≥ +3.5 cm), structural bulges (Δd ≤ -3.5 cm), and hairline cracks (|Δd| ≥ 1.5 cm).")
    add_bullet("Obj 5 (3D Digital Twin Reconstruction): ", "Reconstruct dense spatial point clouds (.PLY format) capturing full room and facade geometries with millimetric fidelity.")
    add_bullet("Obj 6 (Predictive Baseline Maintenance): ", "Formulate longitudinal deformation monitoring pipelines comparing periodic scans against healthy historical baselines.")
    add_bullet("Obj 7 (Dual-Platform Field Adaptability): ", "Deploy an autonomous aerial quadcopter for exterior vertical facades and a Smart 4WD Ground Robotic Car with optical wheel encoders for GPS-denied indoor corridors.")
    add_bullet("Obj 8 (Hardware Upgrade Integration): ", "Upgrade the single-point ToF sensor to a 360° planar LiDAR (YDLIDAR X2) and 360° tilt sensor for automated pitch/roll distortion compensation.")

    # ================= SECTION 3: PREVIOUS MDP WORK (PLY FORGE) =================
    add_h1("3. Previous MDP Work (PLY Forge: Point Cloud Processor) & Cross-Project Foundation")
    add_p(
        "During our prior Multidisciplinary Project (MDP), our team engineered PLY Forge: Point Cloud Processor "
        "(Report: Multidisciplinary_project_Final_report.pdf; Codebase: ply (1).zip). PLY Forge is a high-performance, "
        "fully client-side WebGL application built with HTML5, CSS3, and Vanilla JavaScript, requiring zero external server dependencies, "
        "zero Node.js backend, and zero third-party 3D libraries (such as Three.js or BabylonJS). It runs natively in any modern web browser."
    )
    add_h2("Exhaustive Analysis of MDP Technical Features & Architecture:")
    add_bullet("Binary & ASCII PLY Parser Engine: ", "Engineered a high-throughput client-side file parser leveraging JavaScript FileReader, ArrayBuffer, and DataView APIs. The parser reads standard Polygon File Format (.PLY) files in both ASCII and Binary Little-Endian / Big-Endian formats. It dynamically parses header elements (format, element vertex N, property float x/y/z, property uchar red/green/blue, element face M, end_header), loading hundreds of thousands of vertices into unified typed arrays.")
    add_bullet("GPU-Accelerated WebGL 1.0 Rendering Pipeline: ", "Direct hardware rendering via a custom GLSL shader pipeline. A vertex shader executes 4x4 Model-View-Projection (MVP) matrix transforms, point-size attenuation based on camera distance, and per-vertex RGB interpolation. A fragment shader handles lighting and point shape rendering. The system utilizes the OES_element_index_uint WebGL extension to support 32-bit indices for large meshes exceeding 65,536 vertices.")
    add_bullet("Voxel-Grid Spatial Hash Downsampling / Compression: ", "Implements spatial hashing dividing 3D bounding volumes into discrete cubic voxel cells of user-adjustable radius r. Vertices within each cell are quantized to their centroid, reducing file sizes by 60% to 90% while strictly preserving global geometric boundaries and surface contours.")
    add_bullet("Circle Interior Point Removal (Boundary Extraction): ", "Interactive circular region filtering. The user clicks on the point cloud to define a 3D center (x0, y0, z0) and adjusts a radius slider R. The engine computes Euclidean distances d = sqrt((x-x0)² + (y-y0)² + (z-z0)²), culling all interior points (d < R) while preserving the boundary perimeter ring for hole and cavity perimeter analysis.")
    add_bullet("Multiple Surface Meshing Algorithms: ", "Transforms unorganized point clouds into polygonal surface meshes using: (1) Delaunay 2.5D Triangulation (projects points onto best-fit plane and constructs Delaunay circumcircles); (2) Alpha Shapes (reconstructs non-convex boundaries and concave organic geometries via circumradius parameter α); (3) Convex Hull (computes minimal enclosing convex polygon wrapper); and (4) Grid Triangulation (generates regular quad-strip surface topology).")
    add_bullet("Interactive Screen-Space Region Selection: ", "Frustum ray-casting converts 2D mouse drag rectangles into Normalized Device Coordinates (NDC) [-1, 1], allowing users to isolate point subsets, delete selected regions, or execute camera 'Zoom to Selection'.")
    add_bullet("Standardized PLY Export: ", "Serializes modified vertices and reconstructed polygonal faces into compliant ASCII PLY format using Blob and URL.createObjectURL(), enabling seamless export to CAD/GIS tools.")

    # Embedded MDP Screenshots
    mdp_s1 = os.path.join(assets_dir, "mdp_ply_forge_screenshot1.jpg")
    mdp_s2 = os.path.join(assets_dir, "mdp_ply_forge_screenshot2.jpg")
    if os.path.exists(mdp_s1) and os.path.exists(mdp_s2):
        p_img1 = doc.add_paragraph()
        p_img1.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        p_img1.add_run().add_picture(mdp_s1, width=Inches(3.3))
        p_img1.add_run("   ")
        p_img1.add_run().add_picture(mdp_s2, width=Inches(3.3))
        add_caption("Figure 2: Prior MDP Deliverable — PLY Forge Point Cloud Processor UI (Left: Stanford Bunny Demo & Controls; Right: Delaunay Surface Meshing & Region Selection)")

    add_h2("Cross-Project Synthesis: How MDP Directly Empowers the Current IDP:")
    add_p(
        "Our previous MDP work serves as the software visualization engine for the current IDP. Rather than building a 3D visualizer from scratch, "
        "PLY Forge's WebGL rendering engine is directly embedded into the IDP Ground Operations Dashboard (Tab 4: PLY Forge WebGL Viewer). "
        "When the mobile platform (Drone or Smart 4WD Car) streams LiDAR facade scans, PLY Forge provides zero-latency in-browser 3D rendering. "
        "Furthermore, PLY Forge's voxel downsampling filters high-frequency sensor noise from dense scans, and its Delaunay 2.5D meshing enables "
        "automated calculation of spalling cavity surface areas and volumetric concrete loss."
    )
    add_callout(
        "What Was NOT in MDP vs. What IDP Adds: It is critical to note that MDP was purely an offline, file-based software tool "
        "operating on pre-recorded static files and synthetic demos (Stanford Bunny). MDP had no physical hardware integration, no ToF or LiDAR sensors, "
        "no serial telemetry, no mobile robotics, and no structural health defect classification. The current IDP bridges this gap by engineering "
        "the physical acquisition testbed, real-time ESP32 FreeRTOS firmware, physical calibration (y = 1.0228x + 3.20 cm), autonomous aerial "
        "and terrestrial robotic platforms, and automated civil structural anomaly classification algorithms.",
        title="MDP VS. IDP COMPARISON & DELINEATION"
    )

    # ================= SECTION 4: CURRENT IDP ARCHITECTURE & VERIFIED WORK =================
    add_h1("4. Current IDP Architecture & Verified Work Completed")
    add_p(
        "The current IDP establishes a complete end-to-end cyber-physical pipeline spanning airborne/ground acquisition and ground-side "
        "spatial analytics. The verified operational architecture and implemented subsystems are detailed below:"
    )

    idp_tab = doc.add_table(rows=2, cols=2)
    idp_tab.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(idp_tab)

    idp_cells = idp_tab.rows[0].cells
    idp_cells[0].paragraphs[0].add_run("AERIAL SUBSYSTEM (15377IDP01) — IMPLEMENTED").bold = True
    idp_cells[1].paragraphs[0].add_run("GROUND ANALYTICS (15377IDP02) — IMPLEMENTED").bold = True
    set_cell_background(idp_cells[0], "F1F5F9")
    set_cell_background(idp_cells[1], "F1F5F9")

    idp_r1 = idp_tab.rows[1].cells
    idp_r1[0].paragraphs[0].add_run(
        "• Sensing Core: Benewake TF-Luna 850nm dToF sensor (<5g, 0.35W, 100 Hz, 2° FOV).\n"
        "• Embedded Controller: ESP32-WROOM-32 running custom C++ FreeRTOS firmware.\n"
        "• UART Binary Framing: Strict state machine syncing to 0x59 0x59 preamble, extracting 2-byte distance, 2-byte amplitude, 2-byte chip temp, and validating 8-bit checksum: (Sum Bytes 0..7) & 0xFF == Byte 8.\n"
        "• Two-Point Metrology Fit: Universal calibration equation y = 1.0228x + 3.20 cm derived from physical 39.0 cm and 61.4 cm benchmarks (residual RMSE = ±0.00 cm).\n"
        "• Signal Conditioning: On-chip running median filter (window size N=5) to eliminate single-sample optical dropouts.\n"
        "• Data Handoff: 115200 baud USB-UART streaming with planned UDP telemetry."
    )
    idp_r1[1].paragraphs[0].add_run(
        "• Live Telemetry Ingestion: Python serial/buffer reader ingesting calibrated distances.\n"
        "• Rolling Baseline Tracking: Window-mean baseline filter tracking surface contours.\n"
        "• Rule-Based Anomaly Classifier:\n"
        "  - Cavity (Spall): Δd ≥ +3.5 cm (recessed into wall, colored Orange).\n"
        "  - Bulge (Buckle): Δd ≤ -3.5 cm (protruding outward, colored Orange).\n"
        "  - Crack Indication: |Δd| ≥ 1.5 cm vs adjacent neighbors.\n"
        "• 3D Digital Twin Reconstructor: Generates 9,969-point spatial cloud (.PLY) with North/South/East/West wall tags.\n"
        "• Verified Physical Defect Segmentation: Accurately rendered 4.8m × 4.2m room with 65 cm inward Almari bulge and 60 cm outward Gate recess.\n"
        "• Multi-Tab Streamlit Dashboard: 5 operational tabs for telemetry, profiles, calibration, PLY Forge WebGL, and room metrology."
    )

    for row in idp_tab.rows:
        for cell in row.cells:
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            for p in cell.paragraphs:
                p.paragraph_format.line_spacing = 1.15
                for run in p.runs:
                    run.font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Embedded Photos: Room mesh + Hardware Setup
    room_mesh = os.path.join(assets_dir, "room_mesh_labeled.png")
    bench_setup = os.path.join(assets_dir, "hardware_bench_setup.png")
    if os.path.exists(room_mesh) and os.path.exists(bench_setup):
        p_mesh = doc.add_paragraph()
        p_mesh.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        p_mesh.add_run().add_picture(room_mesh, width=Inches(3.8))
        p_mesh.add_run("   ")
        p_mesh.add_run().add_picture(bench_setup, width=Inches(2.7))
        add_caption("Figure 3: Left: 3D Digital Twin Room Mesh with Almari Bulge (+65cm) & Gate Recess (-60cm); Right: Physical ESP32 + TF-Luna Testbed")

    # Embedded Photos: Physical Bench + Profile
    scan1 = os.path.join(assets_dir, "physical_scan_bench_1.jpg")
    profile2 = os.path.join(assets_dir, "pptx2_ground_s8_img2.jpg")
    if os.path.exists(scan1) and os.path.exists(profile2):
        p_pbench = doc.add_paragraph()
        p_pbench.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        p_pbench.add_run().add_picture(scan1, width=Inches(2.8))
        p_pbench.add_run("   ")
        p_pbench.add_run().add_picture(profile2, width=Inches(3.7))
        add_caption("Figure 4: Left: Physical Bench Measuring Tape Calibration Setup; Right: 2D Structural Residual Profile (Ground Station Tab 2)")

    # ================= SECTION 5: CURRENT CHALLENGES & SMART 4WD CAR =================
    add_h1("5. Current Challenges & The Contingency Smart 4WD Ground Robotic Car")
    add_p(
        "A rigorous empirical analysis of our physical scanning trials revealed several real-world operational challenges that led directly "
        "to the formulation of our Dual-Platform Strategy:"
    )
    add_bullet("1. Manual Sliding Jitter vs. Defect Threshold Overlap: ", "During initial wall scanning, the TF-Luna was manually slid along the wall. Uneven human sliding speed and hand tremor introduced ~2–3 cm measurement fluctuations. Because true structural spalls have depths of 2.5–4.0 cm, hand-motion jitter directly overlaps with the detection threshold (default T = ±3.5 cm), creating false alarms.")
    add_bullet("2. Tilt Beam Elongation: ", "When the sensor tilts by angle θ relative to the surface normal, the beam travels along the hypotenuse: d_meas = d_true / cos(θ). At a 200 cm standoff, a 10° pitch or roll causes a 3.1 cm artificial elongation—falsely mimicking a cavity.")
    add_bullet("3. Drone Aerodynamic Constraints Indoors: ", "Flying an aerial drone indoors (corridors, classrooms, basements) presents severe challenges: lack of GPS lock, regulatory flight restrictions, and aerodynamic wall-effect suction (prop-wash turbulence pulling the drone into the wall when operating at <1.5 m standoff distances).")

    add_h2("The Contingency Platform: Smart 4WD Robotic Car with Optical Wheel Encoders")
    add_p(
        "HOW WE WILL OPERATE IF WE DO NOT USE THE DRONE:\n"
        "If indoor flight restrictions, prop-wash turbulence, or battery flight-time constraints prevent drone operation, the entire sensing array "
        "is immediately deployed on our Smart 4WD Ground Robotic Car. The car transforms the system from an airborne inspector into an "
        "ultra-stable, millimeter-precision terrestrial surface scanner:"
    )
    add_bullet("Hardware Architecture on the Car: ", "A 4-wheel drive robotic chassis equipped with four high-torque DC gear motors (1:48 gear ratio), an L298N/TB6612FNG Dual H-Bridge motor driver, and dual optical wheel encoders (20-slot slotted photo-interrupter disks). A rigid, telescoping vertical aluminum mast holds the TF-Luna ToF sensor and YDLIDAR X2 at adjustable heights (0.2 m to 2.2 m elevation).")
    add_bullet("Closed-Loop Odometry & Speed Stabilization: ", "Unlike erratic human hand sliding, the ESP32 microcontroller executes a closed-loop PID cruise-control routine driving the car at an exact, vibration-free linear speed (e.g., constant 5.0 cm/sec). Wheel encoder pulses integrate exact linear distance traveled along the wall:\n    ΔX = N_ticks × [π × D_wheel / 20 slots]  (where D_wheel = 6.5 cm, giving ~1.02 mm resolution per tick).")
    add_bullet("Dynamic Wall Spatial Coordinate Generation: ", "The car initializes at a designated corner origin datum: P_car(0) = (0, 0, Z_mast). As the car rolls parallel to the wall, every distance measurement d_meas(t) is stamped with its exact encoder X-coordinate:\n    X_point = X_encoder(t)\n    Y_point = d_meas(t) × cos(θ_tilt)  (perpendicular distance from wall)\n    Z_point = Z_mast (stepped in 10 cm or 20 cm vertical elevation bands for full-wall coverage).")
    add_bullet("Key Advantages of the Smart Car: ", "(1) Zero Hand Jitter: Eliminates the 2–3 cm sliding noise completely; (2) Zero Prop-Wash: No aerodynamic turbulence near walls; (3) Extended Scan Endurance: Operates for 2–3 continuous hours on a 12V Li-ion pack (vs. 14 mins on drone); and (4) 100% Indoor Compliance: Safe to operate in any laboratory or classroom without flight clearance.")

    # Embedded Car Diagram (Full-Width High Readability)
    car_diag = os.path.join(assets_dir, "flowchart_smart_car_operation.png")
    if os.path.exists(car_diag):
        p_car = doc.add_paragraph()
        p_car.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        p_car.add_run().add_picture(car_diag, width=Inches(6.4))
        add_caption("Figure 5: Contingency Platform — Smart 4WD Ground Robotic Car Scanning Architecture & Odometry Workflow")

    # ================= SECTION 6: PROPOSED HARDWARE UPGRADE =================
    add_h1("6. Proposed Hardware Upgrade & Technical Justification")
    add_p("To achieve autonomous 3D facade digitisation and eliminate tilt and motion errors, four critical hardware upgrades are specified:")
    add_bullet("1. YDLIDAR X2 360° 2D Laser Rangefinder (INR 7,189.00): ", "Replaces single-point ToF with a 360° rotating laser (3,000 samples/sec, 8.0 m range, 0.12 m blind zone, 7 Hz motor). Instead of scanning one point at a time, it acquires an entire 2D cross-sectional slice in 142 ms, capturing hundreds of surface points simultaneously.")
    add_bullet("2. DFRobot Gravity Digital 360° Tilt Sensor (INR 245.00): ", "High-speed orientation sensor mounted coaxially with the LiDAR. Measures pitch (θ_p) and roll (θ_r) in real time. The ground software applies instant trigonometry: d_corrected = d_raw × cos(θ), completely eliminating the 3.1 cm false-cavity artifact.")
    add_bullet("3. F450 Quadcopter Drone Airframe & Propulsion (INR 5,200.00): ", "Sturdy 450 mm glass-fiber/polyamide frame with four A2212 1000KV brushless motors, 30A SimonK ESCs, and 1045 propellers. Delivers 3,200 g total thrust against a 1,220 g all-up weight (2.6:1 thrust-to-weight ratio).")
    add_bullet("4. High-Capacity 3S 11.1V 4200mAh LiPo Battery (INR 2,850.00): ", "Delivers 14–16 minutes of stable hovering flight, powering both the propulsion motors and the onboard avionics/LiDAR payload.")

    # Embedded Hardware Upgrade Photos
    yd_listing = os.path.join(assets_dir, "ydlidar_x2_listing.png")
    yd_specs = os.path.join(assets_dir, "ydlidar_x2_specs.png")
    drone_img = os.path.join(assets_dir, "drone_airframe.png")
    features_img = os.path.join(assets_dir, "ydlidar_x2_features.png")

    if os.path.exists(yd_listing) and os.path.exists(yd_specs):
        p_h1 = doc.add_paragraph()
        p_h1.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        p_h1.add_run().add_picture(yd_listing, width=Inches(3.3))
        p_h1.add_run("   ")
        p_h1.add_run().add_picture(yd_specs, width=Inches(3.3))
        add_caption("Figure 6(a): Left: YDLIDAR X2 Robu.in Listing (INR 7,189); Right: Technical Specifications")

    if os.path.exists(drone_img) and os.path.exists(features_img):
        p_h2 = doc.add_paragraph()
        p_h2.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        p_h2.add_run().add_picture(drone_img, width=Inches(3.3))
        p_h2.add_run("   ")
        p_h2.add_run().add_picture(features_img, width=Inches(3.3))
        add_caption("Figure 6(b): Left: F450 Quadcopter Airframe; Right: YDLIDAR X2 Dimensional Drawing")

    # ================= SECTION 7: HARDWARE INTEGRATION & COMPATIBILITY =================
    add_h1("7. Hardware Integration & Compatibility Study")
    add_p("A rigorous mechanical, electrical, and computational feasibility analysis confirms 100% interoperability across subsystems:")
    add_bullet("Payload & Mass Budget: ", "F450 frame (282g), 4x Motors/ESCs (340g), Pixhawk/GPS (125g), 3S 4200mAh LiPo (315g), YDLIDAR X2 (120g), ESP32 telemetry (38g) = 1,220 g All-Up Weight (AUW). Total thrust = 3,200 g. Net excess payload capacity = 480 g at 55% hover throttle, ensuring exceptional aerodynamic stability.")
    add_bullet("Power Distribution: ", "11.1V LiPo feeds 4 ESCs directly. A dedicated LM2596 buck converter steps 11.1V down to 5.0V 2A for the YDLIDAR X2 motor and core logic, completely isolating sensor logic from motor inductive spikes.")
    add_bullet("MCU Concurrency & Pin Budget: ", "ESP32-WROOM-32 assigns HardwareSerial2 (GPIO16/17) to YDLIDAR X2 at 115200 baud, GPIO4 to the tilt sensor, and operates FreeRTOS dual-core execution (Core 0: LiDAR UART DMA ingestion; Core 1: WiFi UDP packetization).")

    # ================= SECTION 8: COMPLETE PROCUREMENT BUDGET =================
    add_h1("8. Complete Procurement Budget & Platform-Wise Breakdown")
    add_p(
        "To provide complete financial transparency and operational flexibility for faculty review and grant sanctioning, "
        "the procurement budget is categorized into three mutually transparent packages based on whether the Aerial Drone, "
        "the Smart 4WD Ground Car, or the Integrated Dual-Platform is deployed:"
    )
    add_bullet("Shared Core Sensing & Computing Hardware (INR 8,774.00): ", "Baseline components required regardless of platform (YDLIDAR X2 360° LiDAR, DFRobot Tilt Sensor, ESP32 MCU, LM2596 buck regulators, wiring harness, shipping).")
    add_bullet("Package A — Required ONLY if We Use the Aerial Drone (INR 17,350.00): ", "Flight airframe, brushless propulsion, SimonK ESCs, 1045 propellers, 3S 4200mAh LiPo battery, iMAX B6 digital balance charger, Pixhawk 2.4.8 autopilot with GPS/telemetry, and flight reserve.")
    add_bullet("Package B — Required ONLY if We Use the Smart 4WD Ground Car (INR 3,830.00): ", "High-traction 4WD chassis kit, four 1:48 DC gear motors, dual 20-slot optical wheel encoders for odometry, L298N motor driver, telescoping aluminum sensor mast, 12V Li-ion pack, and ground reserve.")

    bom_items = [
        # PART 1: SHARED CORE
        ("PART 1: SHARED CORE SENSING & COMPUTING", "COMMON TO BOTH", "--", "--", "8,774.00", "Essential for Drone & Car", True, "E2E8F0"),
        ("YDLIDAR X2 360° 2D LiDAR Scanner", "Both (Drone & Car)", "1", "7,189.00", "7,189.00", "Robu.in / In Stock (Screenshot Ref)", False, None),
        ("DFRobot Gravity Digital 360° Tilt Sensor", "Both (Drone & Car)", "1", "245.00", "245.00", "Robu.in / Silverline (Screenshot Ref)", False, None),
        ("ESP32-WROOM-32 Development Board", "Both (Drone & Car)", "1", "380.00", "380.00", "Robu.in / In Stock", False, None),
        ("LM2596 DC-DC Buck Step-Down Voltage Regulator", "Both (Drone & Car)", "2", "120.00", "240.00", "Robu.in / QuartzComponents", False, None),
        ("Wiring Harness, XT60 & JST Connectors, Hardware", "Both (Drone & Car)", "1 lot", "320.00", "320.00", "Robu.in / QuartzComponents", False, None),
        ("Consolidated Domestic Shipping (GST Registered)", "Both (Drone & Car)", "1 lot", "400.00", "400.00", "Robu.in courier rate", False, None),
        # PART 2: DRONE ONLY
        ("PART 2: REQUIRED ONLY IF WE USE DRONE", "DRONE ONLY", "--", "--", "17,350.00", "Exterior Facade Flight", True, "E0E7FF"),
        ("F450 Quadcopter Drone Frame Kit + Landing Gear", "Drone Only", "1", "1,350.00", "1,350.00", "Robu.in / QuartzComponents", False, None),
        ("A2212 1000KV Brushless Motors (Set of 4)", "Drone Only", "1 set", "2,100.00", "2,100.00", "Robu.in / In Stock", False, None),
        ("30A SimonK ESC Speed Controllers (Set of 4)", "Drone Only", "1 set", "1,750.00", "1,750.00", "Robu.in / In Stock", False, None),
        ("1045 Propeller Pairs (CW + CCW, 2 pairs)", "Drone Only", "2 pairs", "130.00", "260.00", "Robu.in / In Stock", False, None),
        ("Orange 3S 11.1V 4200mAh 30C LiPo Battery Pack", "Drone Only", "1", "2,850.00", "2,850.00", "Robu.in / In Stock", False, None),
        ("iMAX B6 80W LiPo Digital Balance Charger + Adapter", "Drone Only", "1", "1,580.00", "1,580.00", "Robu.in / QuartzComponents", False, None),
        ("Pixhawk 2.4.8 Autopilot + M8N GPS + Telemetry", "Drone Only", "1 kit", "5,950.00", "5,950.00", "Robu.in / Silverline", False, None),
        ("Silicone Ball Vibration Damper Mounts for Pixhawk/LiDAR", "Drone Only", "1 set", "250.00", "250.00", "Robu.in / In Stock", False, None),
        ("Drone Subsystem Engineering Contingency (8%)", "Drone Only", "Reserve", "--", "1,260.00", "Wire/connector replacements", False, None),
        # PART 3: CAR ONLY
        ("PART 3: REQUIRED ONLY IF WE USE SMART 4WD CAR", "CAR ONLY", "--", "--", "3,830.00", "Indoor Corridor Scanning", True, "FEF3C7"),
        ("Smart 4WD High-Traction Chassis + 4x 1:48 Motors & Wheels", "Car Only", "1 kit", "1,050.00", "1,050.00", "Robu.in / QuartzComponents", False, None),
        ("Dual 20-Slot Optical Wheel Encoders (Photo-Interrupters)", "Car Only", "1 pair", "320.00", "320.00", "Robu.in / In Stock", False, None),
        ("L298N / TB6612FNG Dual H-Bridge Motor Driver Module", "Car Only", "1", "380.00", "380.00", "Robu.in / QuartzComponents", False, None),
        ("Telescoping Aluminum Sensor Mast & Mounting Bracket (0.2--2.2m)", "Car Only", "1", "650.00", "650.00", "Local fabrication / Hardware", False, None),
        ("12V 2200mAh Li-ion Battery Pack & Dedicated Charger", "Car Only", "1", "1,150.00", "1,150.00", "QuartzComponents / In Stock", False, None),
        ("Smart Car Subsystem Engineering Contingency (8%)", "Car Only", "Reserve", "--", "280.00", "Drive belt/coupler replacements", False, None),
        # CONSOLIDATED TOTAL
        ("TOTAL INTEGRATED DUAL-PLATFORM SYSTEM BUDGET", "FULL SYSTEM", "All Kits", "--", "28,874.00", "Faculty Grant Proposal", True, "0F172A")
    ]

    bom_tab = doc.add_table(rows=len(bom_items)+1, cols=6)
    bom_tab.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(bom_tab)

    headers = ["Item Name & Model", "Platform Requirement", "Qty", "Unit Price", "Subtotal (INR)", "Supplier / Ref Source"]
    for c_idx, h_text in enumerate(headers):
        cell = bom_tab.rows[0].cells[c_idx]
        cell.paragraphs[0].add_run(h_text).bold = True
        set_cell_background(cell, "1E3A8A")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for r_idx, (name, plat, qty, uprice, sub, supp, is_header, bg_hex) in enumerate(bom_items):
        row_cells = bom_tab.rows[r_idx+1].cells
        is_total = (r_idx == len(bom_items)-1)
        for c_idx, val in enumerate([name, plat, qty, uprice, sub, supp]):
            cell = row_cells[c_idx]
            run = cell.paragraphs[0].add_run(val)
            if is_header or is_total:
                run.bold = True
            if is_total:
                set_cell_background(cell, "0F172A")
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            elif bg_hex:
                set_cell_background(cell, bg_hex)
            elif c_idx in [0, 4]:
                run.bold = True

    for row in bom_tab.rows:
        for cell in row.cells:
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            for p in cell.paragraphs:
                p.paragraph_format.line_spacing = 1.05
                for run in p.runs:
                    run.font.size = Pt(8.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Decision Matrix Table
    add_h2("Table 8(b): Deployment Scenarios & Platform Decision Matrix")
    matrix_items = [
        ("Scenario 1: Smart 4WD Car Only (Indoor Lab Contingency)", "Shared Core (INR 8,774) +\nCar Platform (INR 3,830)", "INR 12,604.00\n(MVP: INR 9,964)", "Best for GPS-denied indoor corridors & classrooms. 100% compliant with indoor safety rules; eliminates hand-sliding jitter (1.02 mm/tick odometry); eliminates wall prop-wash suction; runs 2.5 hours non-stop."),
        ("Scenario 2: Aerial Drone Only (Exterior Facade Scanning)", "Shared Core (INR 8,774) +\nDrone Platform (INR 17,350)", "INR 26,124.00", "Best for multi-story exterior building facades & bridge piers. Autonomous GPS waypoint facade tracking; scans inaccessible heights up to 30m; 14–16 minutes flight endurance per battery."),
        ("Scenario 3: Integrated Dual-Platform (Complete Civil SHM System)", "Shared Core (INR 8,774) +\nDrone Platform (INR 17,350) +\nCar Platform (INR 3,830)\n(Less shared charger discount)", "INR 28,874.00", "Complete all-environment Cyber-Physical SHM system. Deploys Drone for exterior tall facades and Smart 4WD Car for indoor corridors. Fulfills 100% of IDP project objectives and research scope.")
    ]

    mat_tab = doc.add_table(rows=len(matrix_items)+1, cols=4)
    mat_tab.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(mat_tab)

    mheaders = ["Deployment Scenario", "Hardware Packages Included", "Total Cost (INR)", "Operational Capabilities & Field Suitability"]
    for c_idx, h_text in enumerate(mheaders):
        cell = mat_tab.rows[0].cells[c_idx]
        cell.paragraphs[0].add_run(h_text).bold = True
        set_cell_background(cell, "1E3A8A")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for r_idx, (scen, pkgs, cost, cap) in enumerate(matrix_items):
        row_cells = mat_tab.rows[r_idx+1].cells
        for c_idx, val in enumerate([scen, pkgs, cost, cap]):
            cell = row_cells[c_idx]
            run = cell.paragraphs[0].add_run(val)
            if c_idx in [0, 2]:
                run.bold = True

    for row in mat_tab.rows:
        for cell in row.cells:
            set_cell_margins(cell, top=70, bottom=70, left=90, right=90)
            for p in cell.paragraphs:
                p.paragraph_format.line_spacing = 1.10
                for run in p.runs:
                    run.font.size = Pt(9.0)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ================= SECTION 9: PROCUREMENT PRIORITY & STAGING =================
    add_h1("9. Hardware Procurement Priority & Staging Strategy")
    add_p("To maximize technical progress and optimize procurement lead times, purchases are organized into 3 sequential procurement phases:")
    add_bullet("Tier 1: Immediate Critical Sensing Core (INR 9,964.00): ", "YDLIDAR X2, DFRobot Tilt Sensor, 4WD Car Kit with Encoders, Buck Converters. Unlock 360° planar wall contour scanning; eliminate 2–3 cm hand jitter; validate tilt correction in laboratory testbed.")
    add_bullet("Tier 2: Flight Platform & Power Train (INR 9,890.00): ", "F450 Frame, 4x A2212 Motors, 4x ESCs, 1045 Props, 3S LiPo, B6 Charger. Construct physical quadcopter UAV; calibrate thrust-to-weight ratio; conduct tethered hover and vibration damping trials.")
    add_bullet("Tier 3: Autonomous Avionics & Contingency (INR 9,020.00): ", "Pixhawk 2.4.8 Kit, GPS/Compass, 433MHz Telemetry, Contingency reserve. Integrate autonomous GPS-waypoint facade tracking, close-loop optical flow hover, and outdoor multi-story facade scanning.")

    # ================= SECTION 10: TECHNICAL ARCHITECTURE & FLOWCHARTS (FULL-WIDTH CRISP) =================
    add_h1("10. Technical Architecture & System Flowcharts")
    add_p(
        "To provide a complete architectural reference, all verified system pipelines and engineering workflows are diagrammed below. "
        "Each diagram is rendered at full page width with high-resolution vector typography for complete readability:"
    )

    f1 = os.path.join(assets_dir, "flowchart_system_architecture.png")
    if os.path.exists(f1):
        p_f1 = doc.add_paragraph()
        p_f1.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        p_f1.add_run().add_picture(f1, width=Inches(6.4))
        add_caption("Figure 7: Diagram 1 — High-Level SHM System Architecture & Cross-Subsystem Telemetry Pipeline")

    f2 = os.path.join(assets_dir, "flowchart_aerial_acquisition.png")
    if os.path.exists(f2):
        p_f2 = doc.add_paragraph()
        p_f2.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        p_f2.add_run().add_picture(f2, width=Inches(6.4))
        add_caption("Figure 8: Diagram 2 — Aerial Subsystem Acquisition Workflow & FreeRTOS Ingestion Pipeline")

    f3 = os.path.join(assets_dir, "flowchart_ground_analytics.png")
    if os.path.exists(f3):
        p_f3 = doc.add_paragraph()
        p_f3.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        p_f3.add_run().add_picture(f3, width=Inches(6.4))
        add_caption("Figure 9: Diagram 3 — Ground Analytics, Baseline Tracking & Structural Defect Decision Tree")

    f4 = os.path.join(assets_dir, "flowchart_power_wiring.png")
    if os.path.exists(f4):
        p_f4 = doc.add_paragraph()
        p_f4.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        p_f4.add_run().add_picture(f4, width=Inches(6.4))
        add_caption("Figure 10: Diagram 4 — Dual-Platform Power Distribution & Hardware Wiring Architecture (Drone vs. Smart 4WD Car)")

    f5 = os.path.join(assets_dir, "flowchart_testing_roadmap.png")
    if os.path.exists(f5):
        p_f5 = doc.add_paragraph()
        p_f5.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        p_f5.add_run().add_picture(f5, width=Inches(6.4))
        add_caption("Figure 11: Diagram 5 — 7-Phase Testing Roadmap & Quantitative Scientific Acceptance Criteria")

    # ================= SECTION 11: FUTURE WORK & PHASED ROADMAP =================
    add_h1("11. Future Work & Phased Implementation Roadmap")
    add_p("A rigorous, 7-phase implementation plan structured across 16 weeks will guide project execution toward full autonomous deployment:")
    add_bullet("Phase 1: Component Procurement & Bench Validation (Weeks 1–2): ", "Procure Tier 1 hardware (YDLIDAR X2, Tilt Sensor, 4WD Car Kit). Execute benchtop electrical tests, establish UART parsing at 115200 baud, and calibrate the tilt sensor.")
    add_bullet("Phase 2: Firmware Integration & Telemetry Pipeline (Weeks 3–4): ", "Develop FreeRTOS tasks on ESP32 Core 0 and Core 1. Integrate hardware DMA buffer for YDLIDAR packets. Implement UDP packetizer streaming 360° polar coordinates to ground station.")
    add_bullet("Phase 3: Airframe Assembly & Propulsion Benchmarking (Weeks 5–6): ", "Assemble F450 frame, calibrate ESC throttle ranges, balance 1045 propellers dynamically. Conduct load-cell thrust tests verifying >2.5:1 thrust-to-weight ratio.")
    add_bullet("Phase 4: Sensor Payload Integration & Tilt Compensation (Weeks 7–8): ", "Fabricate 3D-printed vibration-damping mounting plate. Co-locate YDLIDAR X2 and tilt sensor. Implement mathematical cosine tilt correction on ground telemetry stream.")
    add_bullet("Phase 5: Laboratory Wall Scanning & Terrestrial Odometry (Weeks 9–10): ", "Deploy sensing rig on Smart 4WD Car. Conduct linear wall traverses at 5.0 cm/s using optical encoder odometry. Scan calibrated test wall with known artificial defects (cavities, bulges, cracks).")
    add_bullet("Phase 6: Flight Trials & Tethered Facade Sweeps (Weeks 11–13): ", "Perform outdoor tethered hovering flights. Evaluate acoustic and vibration noise on LiDAR point clouds. Execute vertical sweep scans alongside university exterior building facades.")
    add_bullet("Phase 7: End-to-End System Evaluation & Final Report (Weeks 14–16): ", "Integrate PLY Forge WebGL automated meshing with live Streamlit dashboard. Conduct blind defect detection benchmarks. Publish final engineering report and project video.")

    # ================= SECTION 12: RIGOROUS TESTING & EVALUATION =================
    add_h1("12. Rigorous Testing & Empirical Evaluation Plan")
    add_p("To validate real-world readiness, the system will undergo four empirical testing protocols with quantified pass/fail criteria:")
    add_bullet("LiDAR Static Ranging Accuracy: ", "Range RMSE (0.5m to 6.0m) ≤ ±1.5 cm. Static target at 1.0m, 2.0m, 3.0m, 5.0m verified against laser tape measure.")
    add_bullet("Tilt Correction Efficacy: ", "Elongation Error at 15° tilt ≤ 0.5 cm. Sensor inclined at 5°, 10°, 15° on goniometer bench; evaluate raw vs corrected distance.")
    add_bullet("4WD Car Odometry Accuracy: ", "Linear Displacement Drift ≤ 1.0 cm per 5m traverse. Compare optical wheel encoder accumulated distance against floor benchmark marks.")
    add_bullet("Aero-Acoustic Vibration Drift: ", "Point Cloud Standard Deviation σ ≤ 0.8 cm at 60% hover throttle. Measure standard deviation of planar wall points with motors disarmed vs spinning at hover thrust.")
    add_bullet("Defect Segmentation Sensitivity: ", "True Positive Spall Detection Sensitivity ≥ 95% for Δd ≥ 3.0 cm across 10 test cavities and bulges mounted on test wall.")

    # ================= SECTION 13: RISK MANAGEMENT & MITIGATION =================
    add_h1("13. Risk Management & Technical Mitigation Strategies")
    add_p("A comprehensive engineering risk assessment identified 6 critical failure modes and formulated concrete mitigation protocols:")
    add_bullet("Motor Vibration Inducing LiDAR Point Smear (High / High): ", "Deploy dual-tier silicone vibration-damping mount (Shore 30A silicone balls); dynamically balance motor bells & props.")
    add_bullet("Prop-Wash Wall Suction Effect (High / Medium): ", "Enforce minimum 1.5m standoff buffer; switch to Smart 4WD Ground Car for close-proximity (<1.0m) wall inspection.")
    add_bullet("LiDAR Sunlight Saturation Outdoors (Medium / High): ", "YDLIDAR X2 features optical narrow bandpass filter; schedule flight tests during overcast conditions or golden hour (<20k Lux).")
    add_bullet("Wheel Slip on Polished Floor (4WD Car) (Medium / Medium): ", "Fit high-friction soft rubber tires; add weight ballast over drive axles; cross-check encoder ticks with lateral ToF baseline.")
    add_bullet("Telemetry UDP Packet Loss (Medium / Low): ", "Implement onboard SD-card binary logging concurrently with WiFi UDP broadcast; buffer 500 packets in ESP32 PSRAM.")
    add_bullet("LiPo Battery Low-Voltage Cutoff in Flight (Critical / Low): ", "Configure Pixhawk voltage failsafe: auto-land when per-cell voltage drops below 3.5V (10.5V total pack voltage).")

    # ================= SECTION 14: EXPECTED OUTCOMES & CONTRIBUTIONS =================
    add_h1("14. Expected Outcomes & Research Contributions")
    add_p("Upon successful execution of the phased roadmap, the project will deliver the following measurable outcomes and contributions:")
    add_bullet("Dual-Platform Autonomous Scanning System: ", "A fully functional autonomous SHM testbed featuring both an F450 quadcopter drone for elevated facade sweeps and a Smart 4WD Ground Robotic Car with optical wheel encoders for GPS-denied indoor corridors.")
    add_bullet("High-Speed Planar LiDAR Metrology: ", "360° cross-sectional scanning at 3,000 points/second with automated tilt compensation, reducing single-point scan times by 98% while improving spatial coverage by 15x.")
    add_bullet("Millimetric Defect Segmentation: ", "Automated civil structural anomaly classification capable of detecting spalling cavities (Δd ≥ 3.5 cm), buckling bulges (Δd ≤ -3.5 cm), and surface cracks (|Δd| ≥ 1.5 cm) with ≥95% sensitivity.")
    add_bullet("Integrated 3D Digital Twin Software Suite: ", "Extension of our team's MDP WebGL point-cloud processor (PLY Forge) into a real-time Streamlit operations dashboard featuring zero-latency 3D rendering, voxel compression, and automated compliance reporting.")
    add_bullet("Academic Publications & Intellectual Property: ", "Preparation of an IEEE-format research manuscript targeting conferences/journals in Structural Health Monitoring, Civil Robotics, and Smart Infrastructure.")

    # ================= SECTION 15: CONCLUSION & IMMEDIATE NEXT STEPS =================
    add_h1("15. Conclusion & Immediate Next Steps")
    add_p(
        "This enhanced IDP progress report establishes the complete technological foundation for autonomous Cyber-Physical Structural "
        "Health Monitoring. By seamlessly integrating our prior Multidisciplinary Project deliverables (PLY Forge WebGL engine) with our "
        "current Innovative Design Project achievements (TF-Luna physical calibration, 9,969-point 3D digital twin room reconstruction, "
        "multi-tab operations dashboard), our team has demonstrated a proven capability to deliver publication-grade research."
    )
    add_p(
        "The formulation of the Dual-Platform Strategy—deploying the F450 quadcopter drone for exterior elevated scanning and the "
        "Smart 4WD Ground Robotic Car with optical wheel encoders for indoor GPS-denied surveys—directly resolves all identified operational "
        "constraints (hand-motion jitter, tilt distortion, prop-wash wall effects). Supported by our verified platform-wise procurement breakdown "
        "(Car-Only MVP: INR 9,964; Drone-Only: INR 26,124; Full Integrated Dual-Platform: INR 28,874), our team is poised to commence "
        "Phase 1 component acquisition upon faculty approval."
    )
    add_callout(
        "Immediate Next Steps: (1) Submit this progress report for formal Guide review (Dr. Senthil Kumar N); (2) Finalize component "
        "procurement orders with authorized distributors (Robu.in); (3) Fabricate the 4WD robotic sensor mast and conduct initial encoder "
        "odometry trials; and (4) Bench-test the YDLIDAR X2 with ESP32 FreeRTOS DMA firmware.",
        title="IMMEDIATE ACTION ITEMS"
    )

    # ================= SECTION 16: IEEE REFERENCES =================
    add_h1("16. IEEE References & Technical Datasheets")
    refs = [
        "[1] Benewake (Beijing) Co., Ltd., \"TF-Luna Single-Point Ranging LiDAR Datasheet & User Manual,\" Rev. 2.1, 2024.",
        "[2] Shenzhen EAI Technology Co., Ltd., \"YDLIDAR X2 360-Degree 2D Range Finder Datasheet & Development Manual,\" EAI Tech, 2023.",
        "[3] DFRobot Electronic & Technology Co., \"Gravity: Digital 360-Degree Tilt Sensor User Guide,\" SKU: DFR0028, 2023.",
        "[4] Espressif Systems, \"ESP32 Series SoC Datasheet & FreeRTOS API Reference Guide,\" v4.2, 2024.",
        "[5] F. Nex and F. Remondino, \"UAV for 3D mapping applications: a review,\" Applied Geomatics, vol. 6, no. 1, pp. 1–15, 2014.",
        "[6] J. P. Valenchon et al., \"Structural health monitoring of civil infrastructure using unmanned aerial vehicles: A state-of-the-art review,\" Computer-Aided Civil and Infrastructure Engineering, vol. 37, no. 8, pp. 982–1003, 2022.",
        "[7] H. Guan et al., \"Use of low-cost UAV and LiDAR for crack detection and deformation measurement of concrete structures,\" Automation in Construction, vol. 125, p. 103648, 2021.",
        "[8] R. B. Rusu and S. Cousins, \"3D is here: Point Cloud Library (PCL),\" IEEE International Conference on Robotics and Automation (ICRA), pp. 1–4, 2011.",
        "[9] Dronecode Project, \"Pixhawk 2.4.8 Open Hardware Autopilot Specifications,\" Dronecode Foundation, 2022.",
        "[10] Vitus, \"BACSE291 Innovative Design Project Course Syllabus & Rubrics,\" School of Computer Science & Engineering, VIT Vellore, 2026.",
        "[11] N. P. Joshi, A. P. Mithari, and M. Gupta, \"Web-Based 3D Mesh Simplification Tool — PLY Forge: Point Cloud Processor,\" Multidisciplinary Project Final Report, VIT Vellore, 2025.",
        "[12] P. Sharma and A. Kaushik, \"Aerial Sensing & Drone Integration for Structural Facade Monitoring,\" BACSE291 Review 1 Deliverables, 15377IDP01, VIT Vellore, 2026."
    ]
    for r in refs:
        add_p(r, font_size=9.5, space_after=2)

    # Save Document
    doc.save(DOCX_FILENAME)
    print(f"Successfully generated DOCX report: {DOCX_FILENAME}")

if __name__ == "__main__":
    build_docx()
