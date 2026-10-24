import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

import reportlab
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

PAGE_W, PAGE_H = A4
PRINT_W = PAGE_W - 72  # 0.5 in margins = 36pt * 2 -> 523.27 pt width

C_NAVY = colors.HexColor('#1B365D')
C_TEAL = colors.HexColor('#008296')
C_AMBER = colors.HexColor('#D97706')
C_DARK = colors.HexColor('#2D3748')
C_MUTED = colors.HexColor('#64748B')
C_LIGHT_BG = colors.HexColor('#F8FAFC')
C_ALT_BG = colors.HexColor('#EDF2F7')
C_BORDER = colors.HexColor('#CBD5E1')
C_WHITE = colors.HexColor('#FFFFFF')
C_CALLOUT_BG = colors.HexColor('#F0F9FF')
C_CALLOUT_BORDER = colors.HexColor('#BAE6FD')

def generate_one_page_pdf(filename="ONE_PAGE_RESEARCH_PROGRESS_SUMMARY.pdf"):
    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle('SumInst', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, leading=11, textColor=C_NAVY, alignment=1))
    styles.add(ParagraphStyle('SumTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=C_NAVY, alignment=1, spaceBefore=2, spaceAfter=2))
    styles.add(ParagraphStyle('SumSub', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.5, leading=10, textColor=C_TEAL, alignment=1, spaceAfter=3))
    styles.add(ParagraphStyle('SecHead', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7, leading=9, textColor=C_WHITE))
    styles.add(ParagraphStyle('ItemHead', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=6.5, leading=8.5, textColor=C_NAVY))
    styles.add(ParagraphStyle('ItemBody', parent=styles['Normal'], fontName='Helvetica', fontSize=5.8, leading=7.5, textColor=C_DARK))
    styles.add(ParagraphStyle('MetaCell', parent=styles['Normal'], fontName='Helvetica', fontSize=5.6, leading=7.2, textColor=C_DARK))
    styles.add(ParagraphStyle('MetaCellB', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=5.6, leading=7.2, textColor=C_NAVY))

    story = []

    # Logo + Title Header
    vit_logo = "reports/assets/vit_logo.png"
    if os.path.exists(vit_logo):
        logo_img = Image(vit_logo, width=75, height=26.5)
        head_text = [
            Paragraph("<b>VELLORE INSTITUTE OF TECHNOLOGY (VIT), VELLORE</b>", styles['SumInst']),
            Paragraph("BACSE291 – Innovative Design Project · Project ID: 15377IDP01 &amp; 15377IDP02", styles['MetaCellB'])
        ]
        t_head = Table([[logo_img, head_text]], colWidths=[85, PRINT_W - 85])
        t_head.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (0,0), (0,0), 'LEFT'),
            ('ALIGN', (1,0), (1,0), 'CENTER'),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(t_head)
    
    story.append(Spacer(1, 1.5))
    story.append(Paragraph("AI IN STRUCTURAL HEALTH MONITORING FOR PREDICTIVE MAINTENANCE AND CONTINUOUS SAFETY ASSURANCE", styles['SumTitle']))
    story.append(Paragraph("ONE-PAGE EXECUTIVE RESEARCH PROGRESS &amp; MILESTONE SUMMARY", styles['SumSub']))
    story.append(HRFlowable(width="100%", thickness=1, color=C_NAVY, spaceBefore=1, spaceAfter=2.5))

    # Compact Meta Block
    meta_p = [
        [
            Paragraph("<b>Guide:</b> Dr. N. Senthil Kumar, Ph.D (SCE, Emp: 15377)", styles['MetaCell']),
            Paragraph("<b>Team 1 (Aerial):</b> Priyam Sharma (25BAI0159), Ayushman Kaushik (25BCE0927)", styles['MetaCell']),
            Paragraph("<b>Team 2 (Ground):</b> Nisargkumar Joshi (25BCE0594), Aryan Mithari (25BAI0115), Mudit Gupta (25BA0110)", styles['MetaCell'])
        ]
    ]
    t_m = Table(meta_p, colWidths=[150, 180, 193])
    t_m.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_m)
    story.append(Spacer(1, 2.5))

    def make_section_box(title, items, bg_color):
        head_tbl = Table([[Paragraph(f"<b>{title}</b>", styles['SecHead'])]], colWidths=[PRINT_W])
        head_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), bg_color),
            ('TOPPADDING', (0,0), (-1,-1), 1.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
            ('LEFTPADDING', (0,0), (-1,-1), 3.5),
        ]))
        
        body_content = []
        for h, b in items:
            p_text = f"<b>{h}:</b> {b}"
            body_content.append(Paragraph(p_text, styles['ItemBody']))
            body_content.append(Spacer(1, 1))
        
        body_tbl = Table([[body_content]], colWidths=[PRINT_W])
        body_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), C_WHITE),
            ('BOX', (0,0), (-1,-1), 0.5, C_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('LEFTPADDING', (0,0), (-1,-1), 4),
            ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ]))
        return [head_tbl, body_tbl, Spacer(1, 2.5)]

    # 1. WHAT WE COMPLETED PREVIOUSLY
    p1_items = [
        ("Sensor Interfacing & Framing", "Wired Benewake TF-Luna 850nm ToF Micro-LiDAR to ESP-32 MCU over hardware UART (115200 baud). Engineered 9-byte packet parser with modular checksum validation (tf_luna_code.ino)."),
        ("Mathematical Calibration", "Derived physical linear regression model: Calibrated Distance = 1.0228 × Raw + 3.20 cm (R² = 1.0000, RMSE = ±0.02 cm at 39.0cm & 61.4cm marks), resolving optical casing delay. Implemented 8-sample oversampling."),
        ("3D Digital Twin & Viewer", "Created continuous_multi_point_scanner.py executing 4-wall sweep. Extruded 9,969-point watertight 4.8m × 4.8m room twin (room_mesh.ply/.obj). Built Three.js WebGL viewer with dimension callouts."),
        ("Literature & Scoping", "Reviewed 25 SCI/Scopus papers (2020–2026). Established Review 1 baseline and decomposed architecture into Subsystem 1 (Aerial Sensing) and Subsystem 2 (Ground Analytics).")
    ]
    story.extend(make_section_box("1. WHAT WE COMPLETED PREVIOUSLY (REVIEW 1 THROUGH REVIEW 3)", p1_items, C_NAVY))

    # 2. WHAT WE ARE WORKING ON NOW
    p2_items = [
        ("Sliding Jitter vs. Defect Tuning", "Resolving mechanical hand-sliding noise (~2–3 cm) from structural defect thresholds (±3.5 cm). Tuning 8-sample median filter + 12-sample spatial persistence gating to prevent false anomaly triggers."),
        ("Feature Discrimination Refinement", "Verified macro features: Normal Wall (Cyan, |Δd| < 15cm), Almari Bulge (Orange, Δd ≤ -15cm), Gate Recess (Green, Δd ≥ +15cm). Refining fine-grained cavity/crack isolation via optical flux amplitude."),
        ("ADXL345 Tilt & Vibration Sensor", "Breadboarding ADXL345 3-axis accelerometer over I2C. Programming real-time trigonometric Euler tilt correction: d_true = d_meas · cos(θ_tilt) to prevent tilt-induced distance stretching."),
        ("Wireless UDP Telemetry", "Transitioning from wired USB-serial logging to ESP-32 Wi-Fi UDP streaming with 16-bit packet sequence numbering to detect packet drop.")
    ]
    story.extend(make_section_box("2. WHAT WE ARE WORKING ON NOW (CURRENT WORK IN PROGRESS)", p2_items, C_TEAL))

    # 3. WHAT WE WILL DO NEXT
    p3_items = [
        ("Dynamic Coordinate Tracking (0,0,0) → (X,Y,Z)", "Implement guide's core odometry requirement: Initial datum set to (0,0,0); as the scanner moves/drags across space, coordinates update dynamically: P_sensor(t) = P_sensor(0) + ΔT(t), preventing point cloud collapse."),
        ("2D 360° LiDAR Sensor Upgrade", "Procure and mount YDLIDAR X4 / LD06 2D 360° laser scanner (3–5k pts/s). Replaces manual sequential wall sweeps with instantaneous omnidirectional planar room closure and 2D SLAM."),
        ("Dual-Platform Testing (Drone & Smart Car Rover)", "Test on: (1) Primary Carbon Fiber Quadcopter UAV with silicone dampers; and (2) Smart 4WD Car Rover with optical wheel encoders as an indoor GPS-denied contingency platform."),
        ("Longitudinal Predictive Maintenance", "Compare dated scan point clouds of the same asset over time to compute deterioration trends (Δd progression) for predictive structural maintenance.")
    ]
    story.extend(make_section_box("3. WHAT WE WILL DO NEXT (FUTURE WORK PLAN & MILESTONE R1 ROADMAP)", p3_items, C_DARK))

    # 4. EXPECTED OUTCOME & BUDGET SUMMARY
    p4_items = [
        ("Expected Deliverables", "Fully flight/rover-validated LiDAR SHM platform, sub-centimeter calibrated 3D room twins, automated defect classification logs, and WebGL Three.js interactive inspection suite."),
        ("Itemized Hardware Budget", "Complete Dual-Subsystem Hardware: ₹26,900 Total (Procured: TF-Luna ₹2,200, ESP32s ₹900, Drone Frame ₹2,200, Motors/ESC ₹4,500, Dampers ₹550 | To Procure: 2D LiDAR ₹7,800, Flight Controller ₹3,200, LiPo Battery ₹1,800, Charger ₹1,400, Car Rover Chassis ₹1,600, Encoders ₹300).")
    ]
    story.extend(make_section_box("4. EXPECTED FINAL OUTCOME & PROJECT BUDGET SUMMARY", p4_items, C_AMBER))

    # Build PDF
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=20,
        bottomMargin=20
    )
    doc.build(story)
    print(f"Successfully generated 1-page summary PDF: {filename}")

def generate_one_page_docx(filename="ONE_PAGE_RESEARCH_PROGRESS_SUMMARY.docx"):
    doc = docx.Document()
    for s in doc.sections:
        s.top_margin = Inches(0.5)
        s.bottom_margin = Inches(0.5)
        s.left_margin = Inches(0.5)
        s.right_margin = Inches(0.5)

    NAVY = RGBColor(27, 54, 93)
    TEAL = RGBColor(0, 130, 150)
    DARK = RGBColor(40, 44, 52)
    MUTED = RGBColor(100, 110, 120)

    p_t = doc.add_paragraph()
    p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t.paragraph_format.space_after = Pt(2)
    r = p_t.add_run("VELLORE INSTITUTE OF TECHNOLOGY (VIT), VELLORE\nBACSE291 – INNOVATIVE DESIGN PROJECT · FALL 2026")
    r.font.name = "Arial"
    r.font.size = Pt(10)
    r.font.bold = True
    r.font.color.rgb = NAVY

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(2)
    r = p_title.add_run("AI IN STRUCTURAL HEALTH MONITORING FOR PREDICTIVE MAINTENANCE AND CONTINUOUS SAFETY ASSURANCE")
    r.font.name = "Arial"
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = NAVY

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(4)
    r = p_sub.add_run("ONE-PAGE EXECUTIVE RESEARCH PROGRESS & MILESTONE SUMMARY")
    r.font.name = "Arial"
    r.font.size = Pt(9)
    r.font.bold = True
    r.font.color.rgb = TEAL

    # Meta
    p_m = doc.add_paragraph()
    p_m.paragraph_format.space_after = Pt(4)
    r = p_m.add_run("Guide: Dr. N. Senthil Kumar, Ph.D (SCE, Emp: 15377) | Project IDs: 15377IDP01 & 15377IDP02\nTeam 1 (Aerial): Priyam Sharma (25BAI0159), Ayushman Kaushik (25BCE0927)\nTeam 2 (Ground): Nisargkumar Joshi (25BCE0594), Aryan Mithari (25BAI0115), Mudit Gupta (25BA0110)")
    r.font.name = "Calibri"
    r.font.size = Pt(8)
    r.font.color.rgb = MUTED

    def add_sec(title, items, col_rgb):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(f"■ {title}")
        r.font.name = "Arial"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = col_rgb
        for h, b in items:
            bp = doc.add_paragraph(style='List Bullet')
            bp.paragraph_format.space_before = Pt(0)
            bp.paragraph_format.space_after = Pt(1.5)
            rh = bp.add_run(f"{h}: ")
            rh.font.name = "Calibri"
            rh.font.size = Pt(8.5)
            rh.font.bold = True
            rh.font.color.rgb = DARK
            rb = bp.add_run(b)
            rb.font.name = "Calibri"
            rb.font.size = Pt(8.5)
            rb.font.color.rgb = DARK

    p1_items = [
        ("Sensor Interfacing & Framing", "Wired Benewake TF-Luna 850nm ToF Micro-LiDAR to ESP-32 MCU over hardware UART (115200 baud). Engineered 9-byte packet parser with modular checksum validation (tf_luna_code.ino)."),
        ("Mathematical Calibration", "Derived physical linear regression model: Calibrated Distance = 1.0228 × Raw + 3.20 cm (R² = 1.0000, RMSE = ±0.02 cm at 39.0cm & 61.4cm marks), resolving optical casing delay. Implemented 8-sample oversampling."),
        ("3D Digital Twin & Viewer", "Created continuous_multi_point_scanner.py executing 4-wall sweep. Extruded 9,969-point watertight 4.8m × 4.8m room twin (room_mesh.ply/.obj). Built Three.js WebGL viewer with dimension callouts."),
        ("Literature & Scoping", "Reviewed 25 SCI/Scopus papers (2020–2026). Established Review 1 baseline and decomposed architecture into Subsystem 1 (Aerial Sensing) and Subsystem 2 (Ground Analytics).")
    ]
    add_sec("1. WHAT WE COMPLETED PREVIOUSLY (REVIEW 1 THROUGH REVIEW 3)", p1_items, NAVY)

    p2_items = [
        ("Sliding Jitter vs. Defect Tuning", "Resolving mechanical hand-sliding noise (~2–3 cm) from structural defect thresholds (±3.5 cm). Tuning 8-sample median filter + 12-sample spatial persistence gating to prevent false anomaly triggers."),
        ("Feature Discrimination Refinement", "Verified macro features: Normal Wall (Cyan, |Δd| < 15cm), Almari Bulge (Orange, Δd ≤ -15cm), Gate Recess (Green, Δd ≥ +15cm). Refining fine-grained cavity/crack isolation via optical flux amplitude."),
        ("ADXL345 Tilt & Vibration Sensor", "Breadboarding ADXL345 3-axis accelerometer over I2C. Programming real-time trigonometric Euler tilt correction: d_true = d_meas · cos(θ_tilt) to prevent tilt-induced distance stretching."),
        ("Wireless UDP Telemetry", "Transitioning from wired USB-serial logging to ESP-32 Wi-Fi UDP streaming with 16-bit packet sequence numbering to detect packet drop.")
    ]
    add_sec("2. WHAT WE ARE WORKING ON NOW (CURRENT WORK IN PROGRESS)", p2_items, TEAL)

    p3_items = [
        ("Dynamic Coordinate Tracking (0,0,0) → (X,Y,Z)", "Implement guide's core odometry requirement: Initial datum set to (0,0,0); as the scanner moves/drags across space, coordinates update dynamically: P_sensor(t) = P_sensor(0) + ΔT(t), preventing point cloud collapse."),
        ("2D 360° LiDAR Sensor Upgrade", "Procure and mount YDLIDAR X4 / LD06 2D 360° laser scanner (3–5k pts/s). Replaces manual sequential wall sweeps with instantaneous omnidirectional planar room closure and 2D SLAM."),
        ("Dual-Platform Testing (Drone & Smart Car Rover)", "Test on: (1) Primary Carbon Fiber Quadcopter UAV with silicone dampers; and (2) Smart 4WD Car Rover with optical wheel encoders as an indoor GPS-denied contingency platform."),
        ("Longitudinal Predictive Maintenance", "Compare dated scan point clouds of the same asset over time to compute deterioration trends (Δd progression) for predictive structural maintenance.")
    ]
    add_sec("3. WHAT WE WILL DO NEXT (FUTURE WORK PLAN & MILESTONE R1 ROADMAP)", p3_items, DARK)

    p4_items = [
        ("Expected Deliverables", "Fully flight/rover-validated LiDAR SHM platform, sub-centimeter calibrated 3D room twins, automated defect classification logs, and WebGL Three.js interactive inspection suite."),
        ("Itemized Hardware Budget", "Complete Dual-Subsystem Hardware: ₹26,900 Total (Procured: TF-Luna ₹2,200, ESP32s ₹900, Drone Frame ₹2,200, Motors/ESC ₹4,500, Dampers ₹550 | To Procure: 2D LiDAR ₹7,800, Flight Controller ₹3,200, LiPo Battery ₹1,800, Charger ₹1,400, Car Rover Chassis ₹1,600, Encoders ₹300).")
    ]
    add_sec("4. EXPECTED FINAL OUTCOME & PROJECT BUDGET SUMMARY", p4_items, RGBColor(217, 119, 6))

    doc.save(filename)
    print(f"Successfully generated 1-page summary DOCX: {filename}")

if __name__ == '__main__':
    generate_one_page_pdf()
    generate_one_page_docx()
