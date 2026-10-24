import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

sys.stdout.reconfigure(encoding='utf-8')

PDF_NAME = "ONE_PAGE_EXECUTIVE_PROGRESS_SUMMARY.pdf"
DOCX_NAME = "ONE_PAGE_EXECUTIVE_PROGRESS_SUMMARY.docx"

# Color Palette
C_NAVY = colors.HexColor('#0F172A')
C_PRIMARY = colors.HexColor('#1E3A8A')
C_SECONDARY = colors.HexColor('#0284C7')
C_TEXT = colors.HexColor('#1E293B')
C_MUTED = colors.HexColor('#64748B')
C_BG_LIGHT = colors.HexColor('#F8FAFC')
C_BORDER = colors.HexColor('#CBD5E1')
C_WHITE = colors.HexColor('#FFFFFF')
C_EMERALD = colors.HexColor('#059669')
C_AMBER = colors.HexColor('#D97706')

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

def build_pdf_summary():
    doc = SimpleDocTemplate(
        PDF_NAME,
        pagesize=A4,
        leftMargin=28,
        rightMargin=28,
        topMargin=26,
        bottomMargin=26
    )

    styles = getSampleStyleSheet()

    t_head = ParagraphStyle('HHead', fontName='Helvetica-Bold', fontSize=12, leading=15, textColor=C_NAVY, alignment=1)
    t_sub = ParagraphStyle('HSub', fontName='Helvetica-Bold', fontSize=8, leading=10.5, textColor=C_PRIMARY, alignment=1)
    t_meta = ParagraphStyle('HMeta', fontName='Helvetica', fontSize=6.8, leading=8.8, textColor=C_MUTED, alignment=1)

    sec_title = ParagraphStyle('SecTitle', fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, textColor=C_WHITE, alignment=1)
    b_text = ParagraphStyle('BText', fontName='Helvetica', fontSize=6.2, leading=8.0, textColor=C_TEXT)
    b_bold = ParagraphStyle('BBold', fontName='Helvetica-Bold', fontSize=6.2, leading=8.0, textColor=C_NAVY)

    story = []

    # Header
    story.append(Paragraph("AI IN STRUCTURAL HEALTH MONITORING FOR PREDICTIVE MAINTENANCE &amp; SAFETY ASSURANCE", t_head))
    story.append(Paragraph("EXECUTIVE PROGRESS SUMMARY: PREVIOUS MDP, CURRENT IDP, HARDWARE UPGRADE &amp; PROCUREMENT PLAN", t_sub))
    story.append(Paragraph("BACSE291 — Innovative Design Project | Fall 2026 | Vellore Institute of Technology (VIT), Vellore", t_meta))
    story.append(Paragraph("<b>Guide:</b> Dr. Senthil Kumar N (Emp ID: 15377, SCOPE) | <b>Aerial (15377IDP01):</b> Priyam S., Ayushman K. | <b>Ground (15377IDP02):</b> Nisargkumar J. (Lead), Aryan M., Mudit G.", t_meta))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_PRIMARY, spaceBefore=0, spaceAfter=4))

    # Quadrant 1 & 2 Table
    q1_content = [
        Paragraph("<b>1. PREVIOUS MDP PROJECT: PLY FORGE</b>", sec_title)
    ]
    q1_body = Paragraph(
        "• <b>Objective &amp; Architecture:</b> Client-side WebGL 3D Point Cloud Processor in HTML5/ES6 without external libraries.<br/>"
        "• <b>Implemented Capabilities:</b> Binary/ASCII PLY parsing (DataView/TextDecoder), 3D point cloud rendering, circle ROI filtering, 2.5D Delaunay/grid surface triangulation, and standardized PLY export.<br/>"
        "• <b>Voxel Compression:</b> Spatial hashing downsampling point clouds by 60%–85% while preserving structural boundaries.<br/>"
        "• <b>Cross-Project Reuse:</b> Provides the verified GPU rendering and digital twin engine for current IDP ground analytics. Eliminates software licensing costs.",
        b_text
    )

    q2_content = [
        Paragraph("<b>2. CURRENT IDP WORK DEVELOPED &amp; VERIFIED</b>", sec_title)
    ]
    q2_body = Paragraph(
        "• <b>Aerial Subsystem (15377IDP01):</b> Benewake TF-Luna 850nm ToF (<5g, 0.35W, 100 Hz) interfaced with ESP32. Firmware parses 9-byte packets, validates 0x59 0x59 sync and 8-bit checksum. Integrated median filter (N=5).<br/>"
        "• <b>Two-Point Metrology Fit:</b> Universal straight-line model: <i>y = 1.0228x + 3.20 cm</i> (R²=1.0000, RMSE=±0.02 cm across 39.0cm and 61.4cm physical benchmarks).<br/>"
        "• <b>Ground Subsystem (15377IDP02):</b> Rolling baseline residuals (Δd = d_meas - d_ref); flags spalling cavities (Δd ≥ +3.5cm) and bulges (Δd ≤ -3.5cm).<br/>"
        "• <b>3D Digital Twin:</b> Reconstructed 9,969-point room (.PLY) isolating Almari bulge (+65cm, Orange) and Gate recess (-60cm, Green). 5-tab Streamlit dashboard active.",
        b_text
    )

    row1_table = Table([
        [q1_content, q2_content],
        [[q1_body], [q2_body]]
    ], colWidths=[267, 272])
    row1_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), C_PRIMARY),
        ('BACKGROUND', (1,0), (1,0), C_SECONDARY),
        ('BACKGROUND', (0,1), (-1,1), C_BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(row1_table)
    story.append(Spacer(1, 4))

    # Quadrant 3 & 4 Table
    q3_content = [
        Paragraph("<b>3. HARDWARE UPGRADES &amp; PROCUREMENT BUDGET</b>", sec_title)
    ]
    q3_body = Paragraph(
        "• <b>Engineering Need:</b> Manual sliding jitter (~2–3 cm) and sensor tilt elongation (d_true = d_meas · cos θ) require dedicated hardware sensing and active airframe mobility.<br/>"
        "• <b>YDLIDAR X2 360° LiDAR:</b> 3,000 pts/s, 7 Hz continuous planar slicing, 0.12–8.0m range, 3.3V UART (115200 bps), 5V 500mA. Ref price: <b>₹7,189.00</b>.<br/>"
        "• <b>DFRobot Gravity Tilt Sensor:</b> 360° ball switch detecting pitch/roll to apply trigonometric compensation in ESP32 firmware. Ref price: <b>₹245.00</b>.<br/>"
        "• <b>F450 Drone Kit + Pixhawk:</b> F450 frame, 4x 2212 motors, 4x 30A ESCs, Pixhawk 2.4.8 autopilot, 1045 props. Subtotal: <b>₹12,020.00</b>.<br/>"
        "• <b>Power &amp; Mounting:</b> 3S 4200mAh 35C LiPo (₹2,450), iMAX B6 charger (₹1,350), 5V 5A UBEC (₹380), silicone damper &amp; wiring (₹740).<br/>"
        "• <b>TOTAL BUDGET:</b> Essential: ₹24,724 | Shipping: ₹400 | Contingency (8%): ₹2,000 | <b>TOTAL: ₹27,124.00 INR</b> (MVP Option: ₹8,214.00).",
        b_text
    )

    q4_content = [
        Paragraph("<b>4. FUTURE ROADMAP &amp; SYSTEM INTEGRATION</b>", sec_title)
    ]
    q4_body = Paragraph(
        "• <b>Phase 1–2 (Weeks 1–3):</b> Procure Priority 1 hardware (LiDAR, tilt sensor, UBEC); verify UART framing and 5V rail brownout protection on bench.<br/>"
        "• <b>Phase 3–4 (Weeks 4–6):</b> Implement firmware tilt compensation (d_true = d_cal · cos θ); assemble F450 quadcopter airframe; balance center of gravity; install silicone vibration isolation deck (>18 dB attenuation).<br/>"
        "• <b>Phase 5–6 (Weeks 7–9):</b> Adapt PLY Forge WebGL engine for streaming UDP point cloud buffers; conduct tethered hover flight trials; scan facade with calibrated 2cm &amp; 3.5cm simulated spalls.<br/>"
        "• <b>Phase 7 (Week 10):</b> End-to-end faculty demonstration, automated PDF inspection report generation, and longitudinal deterioration baseline establishment.<br/>"
        "• <b>Target Metrics:</b> Static distance MAE ≤ ±0.5cm; Tilt error residual ≤ ±1.0cm; Defect detection precision ≥ 90%, recall ≥ 85%; Continuous hover flight time ≥ 14 mins.",
        b_text
    )

    row2_table = Table([
        [q3_content, q4_content],
        [[q3_body], [q4_body]]
    ], colWidths=[267, 272])
    row2_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), C_AMBER),
        ('BACKGROUND', (1,0), (1,0), C_EMERALD),
        ('BACKGROUND', (0,1), (-1,1), C_BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(row2_table)
    story.append(Spacer(1, 4))

    # Budget Summary Mini Table
    b_sum_data = [
        [
            Paragraph("<b>Component Group</b>", ParagraphStyle('ThS', fontName='Helvetica-Bold', fontSize=6.2, textColor=C_WHITE, alignment=1)),
            Paragraph("<b>Key Inclusions</b>", ParagraphStyle('ThS', fontName='Helvetica-Bold', fontSize=6.2, textColor=C_WHITE, alignment=1)),
            Paragraph("<b>Cost (INR)</b>", ParagraphStyle('ThS', fontName='Helvetica-Bold', fontSize=6.2, textColor=C_WHITE, alignment=1)),
            Paragraph("<b>Procurement Phasing</b>", ParagraphStyle('ThS', fontName='Helvetica-Bold', fontSize=6.2, textColor=C_WHITE, alignment=1))
        ],
        [
            Paragraph("Sensors &amp; Power Regulation", b_bold),
            Paragraph("YDLIDAR X2 360° LiDAR (₹7,189), DFRobot Tilt Sensor (₹245), 5V 5A UBEC (₹380)", b_text),
            Paragraph("₹7,814.00", b_bold),
            Paragraph("<font color='#059669'><b>Priority 1 (Immediate / Week 1–2)</b></font>", b_text)
        ],
        [
            Paragraph("Airframe &amp; Power Reservoir", b_bold),
            Paragraph("F450 Frame Kit + Motors + ESCs (₹5,200), 3S 4200mAh LiPo &amp; B6 Charger (₹3,800), Dampers (₹740)", b_text),
            Paragraph("₹9,740.00", b_bold),
            Paragraph("<font color='#D97706'><b>Priority 2 (Integration / Week 3–4)</b></font>", b_text)
        ],
        [
            Paragraph("Avionics &amp; Contingency", b_bold),
            Paragraph("Pixhawk 2.4.8 Autopilot + GPS Kit (₹6,850), Courier Shipping (₹400), Risk Reserve (₹2,000)", b_text),
            Paragraph("₹9,250.00", b_bold),
            Paragraph("<font color='#1E3A8A'><b>Priority 3 (Flight Trials / Week 5–6)</b></font>", b_text)
        ],
        [
            Paragraph("<b>TOTAL RECOMMENDED GRANT</b>", ParagraphStyle('TbTot', fontName='Helvetica-Bold', fontSize=6.5, textColor=C_WHITE)),
            Paragraph("<b>Complete Airborne Cyber-Physical SHM System (MVP Bench Option: ₹8,214.00)</b>", ParagraphStyle('TbTot', fontName='Helvetica-Bold', fontSize=6.2, textColor=C_WHITE)),
            Paragraph("<b>₹27,124.00</b>", ParagraphStyle('TbTot', fontName='Helvetica-Bold', fontSize=6.5, textColor=C_WHITE)),
            Paragraph("<b>Faculty Sign-Off Ready</b>", ParagraphStyle('TbTot', fontName='Helvetica-Bold', fontSize=6.2, textColor=C_WHITE))
        ]
    ]
    t_bsum = Table(b_sum_data, colWidths=[110, 249, 70, 110])
    t_bsum.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('BACKGROUND', (0,-1), (-1,-1), C_PRIMARY),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_bsum)
    story.append(Spacer(1, 4))

    # Sign-off line
    sign_text = Paragraph(
        "<b>Project Leads:</b> Nisargkumar Joshi (25BCE0594, Ground Lead) &amp; Priyam Sharma (25BAI0159, Aerial Lead) | "
        "<b>Guide Sign-off:</b> Dr. Senthil Kumar N (Associate Professor Grade 2, SCOPE) | <b>Date:</b> October 24, 2026",
        ParagraphStyle('SignLine', fontName='Helvetica-Oblique', fontSize=6.2, leading=8.0, textColor=C_MUTED, alignment=1)
    )
    story.append(sign_text)

    doc.build(story)
    print(f"Successfully generated 1-page summary PDF: {PDF_NAME}")

def build_docx_summary():
    doc = docx.Document()
    for s in doc.sections:
        s.top_margin = Inches(0.4)
        s.bottom_margin = Inches(0.4)
        s.left_margin = Inches(0.4)
        s.right_margin = Inches(0.4)

    p_h = doc.add_paragraph()
    r_h = p_h.add_run("AI IN STRUCTURAL HEALTH MONITORING FOR PREDICTIVE MAINTENANCE & SAFETY ASSURANCE\n")
    r_h.bold = True
    r_h.font.size = Pt(12)
    r_h.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
    p_h.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    r_sub = p_h.add_run("EXECUTIVE PROGRESS SUMMARY: PREVIOUS MDP, CURRENT IDP, HARDWARE UPGRADE & PROCUREMENT PLAN\n")
    r_sub.bold = True
    r_sub.font.size = Pt(9)
    r_sub.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)

    r_meta = p_h.add_run(
        "BACSE291 — Innovative Design Project | Fall 2026 | Vellore Institute of Technology (VIT), Vellore\n"
        "Guide: Dr. Senthil Kumar N (Emp ID: 15377, SCOPE) | Aerial: Priyam S., Ayushman K. | Ground: Nisargkumar J. (Lead), Aryan M., Mudit G."
    )
    r_meta.font.size = Pt(7.5)
    p_h.paragraph_format.space_after = Pt(6)

    # 4-quadrant table
    q_table = doc.add_table(rows=2, cols=2)
    q_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(q_table)

    cells = q_table.rows[0].cells
    cells[0].paragraphs[0].add_run("1. PREVIOUS MDP: PLY FORGE (POINT CLOUD PROCESSOR)\n").bold = True
    cells[0].paragraphs[0].add_run(
        "• Client-side WebGL 3D Point Cloud Processor built in HTML5/ES6 without external libraries.\n"
        "• Verified features: Binary/ASCII PLY parsing, circle ROI filtering, 2.5D Delaunay/grid surface triangulation, and PLY export.\n"
        "• Voxel-grid downsampling achieving 60%–85% file compression while preserving structural boundaries.\n"
        "• Cross-Project Reuse: Directly powers the ground analytics 3D WebGL digital twin rendering engine, eliminating software licensing costs."
    )
    set_cell_background(cells[0], "F1F5F9")

    cells[1].paragraphs[0].add_run("2. CURRENT IDP WORK DEVELOPED & VERIFIED\n").bold = True
    cells[1].paragraphs[0].add_run(
        "• Aerial Subsystem (15377IDP01): Benewake TF-Luna 850nm ToF (<5g, 0.35W, 100 Hz) interfaced with ESP32. Firmware parses 9-byte packets, validates 0x59 0x59 sync and 8-bit checksum. Running median filter (N=5).\n"
        "• Two-Point Calibration: Universal straight-line model: y = 1.0228x + 3.20 cm (R²=1.0000, RMSE=±0.02 cm on physical benchmarks).\n"
        "• Ground Subsystem (15377IDP02): Rolling baseline residuals (Δd = d_meas - d_ref); flags spalling cavities (Δd ≥ +3.5cm) and bulges (Δd ≤ -3.5cm).\n"
        "• 3D Digital Twin: Reconstructed 9,969-point room (.PLY) isolating Almari bulge (+65cm, Orange) and Gate recess (-60cm, Green). 5-tab Streamlit dashboard active."
    )
    set_cell_background(cells[1], "F8FAFC")

    cells2 = q_table.rows[1].cells
    cells2[0].paragraphs[0].add_run("3. HARDWARE UPGRADES & PROCUREMENT BUDGET\n").bold = True
    cells2[0].paragraphs[0].add_run(
        "• Engineering Need: Manual sliding jitter (~2–3 cm) and sensor tilt elongation (d_true = d_meas · cos θ) require dedicated sensing and airframe mobility.\n"
        "• YDLIDAR X2 360° LiDAR: 3,000 pts/s, 7 Hz continuous planar slicing, 0.12–8.0m range, 3.3V UART (115200 bps). Ref price: ₹7,189.00.\n"
        "• DFRobot Gravity Tilt Sensor: 360° ball switch detecting pitch/roll to apply trigonometric compensation in ESP32 firmware. Ref price: ₹245.00.\n"
        "• F450 Drone Kit + Pixhawk: F450 frame, 4x 2212 motors, 4x 30A ESCs, Pixhawk 2.4.8 autopilot, 1045 props. Subtotal: ₹12,020.00.\n"
        "• Power & Mounting: 3S 4200mAh 35C LiPo (₹2,450), iMAX B6 charger (₹1,350), 5V 5A UBEC (₹380), silicone damper & wiring (₹740).\n"
        "• TOTAL BUDGET: Essential: ₹24,724 | Shipping: ₹400 | Contingency (8%): ₹2,000 | TOTAL: ₹27,124.00 INR (MVP Option: ₹8,214.00)."
    )
    set_cell_background(cells2[0], "FEF3C7")

    cells2[1].paragraphs[0].add_run("4. FUTURE ROADMAP & SYSTEM INTEGRATION\n").bold = True
    cells2[1].paragraphs[0].add_run(
        "• Phase 1–2 (Weeks 1–3): Procure Priority 1 hardware (LiDAR, tilt sensor, UBEC); verify UART framing and 5V rail brownout protection on bench.\n"
        "• Phase 3–4 (Weeks 4–6): Implement firmware tilt compensation (d_true = d_cal · cos θ); assemble F450 quadcopter airframe; balance center of gravity; install silicone vibration isolation deck (>18 dB attenuation).\n"
        "• Phase 5–6 (Weeks 7–9): Adapt PLY Forge WebGL engine for streaming UDP point cloud buffers; conduct tethered hover flight trials; scan facade with calibrated 2cm & 3.5cm simulated spalls.\n"
        "• Phase 7 (Week 10): End-to-end faculty demonstration, automated PDF inspection report generation, and longitudinal deterioration baseline establishment.\n"
        "• Target Metrics: Static distance MAE ≤ ±0.5cm; Tilt error residual ≤ ±1.0cm; Defect detection precision ≥ 90%, recall ≥ 85%; Continuous hover flight time ≥ 14 mins."
    )
    set_cell_background(cells2[1], "ECFDF5")

    for row in q_table.rows:
        for cell in row.cells:
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            for p in cell.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(8)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Mini budget table in DOCX
    b_table = doc.add_table(rows=5, cols=4)
    b_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(b_table)

    b_h = ["Component Group", "Key Inclusions", "Cost (INR)", "Procurement Phasing"]
    for i, h in enumerate(b_h):
        cell = b_table.rows[0].cells[i]
        cell.paragraphs[0].add_run(h).bold = True
        set_cell_background(cell, "0F172A")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        cell.paragraphs[0].runs[0].font.size = Pt(8)

    b_rows = [
        ("Sensors & Power Regulation", "YDLIDAR X2 360° LiDAR (₹7,189), DFRobot Tilt Sensor (₹245), 5V 5A UBEC (₹380)", "₹7,814.00", "Priority 1 (Immediate / Week 1–2)"),
        ("Airframe & Power Reservoir", "F450 Frame Kit + Motors + ESCs (₹5,200), 3S 4200mAh LiPo & B6 Charger (₹3,800), Dampers (₹740)", "₹9,740.00", "Priority 2 (Integration / Week 3–4)"),
        ("Avionics & Contingency", "Pixhawk 2.4.8 Autopilot + GPS Kit (₹6,850), Courier Shipping (₹400), Risk Reserve (₹2,000)", "₹9,250.00", "Priority 3 (Flight Trials / Week 5–6)"),
        ("TOTAL RECOMMENDED GRANT", "Complete Airborne Cyber-Physical SHM System (MVP Bench Option: ₹8,214.00)", "₹27,124.00", "Faculty Sign-Off Ready")
    ]

    for row_idx, data in enumerate(b_rows):
        row = b_table.rows[row_idx + 1]
        for col_idx, text in enumerate(data):
            cell = row.cells[col_idx]
            r = cell.paragraphs[0].add_run(text)
            r.font.size = Pt(7.5)
            if row_idx == 3:
                r.bold = True
                set_cell_background(cell, "1E3A8A")
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            elif row_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")

    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    p_sign = doc.add_paragraph()
    r_s = p_sign.add_run(
        "Project Leads: Nisargkumar Joshi (25BCE0594, Ground Lead) & Priyam Sharma (25BAI0159, Aerial Lead) | "
        "Guide Sign-off: Dr. Senthil Kumar N (Associate Professor Grade 2, SCOPE) | Date: October 24, 2026"
    )
    r_s.font.size = Pt(7.5)
    r_s.font.italic = True
    p_sign.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    doc.save(DOCX_NAME)
    print(f"Successfully generated 1-page summary DOCX: {DOCX_NAME}")

if __name__ == "__main__":
    build_pdf_summary()
    build_docx_summary()
