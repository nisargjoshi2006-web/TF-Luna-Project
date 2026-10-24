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

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
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
        leftMargin=26,
        rightMargin=26,
        topMargin=22,
        bottomMargin=22
    )

    styles = getSampleStyleSheet()

    t_head = ParagraphStyle('HHead', fontName='Helvetica-Bold', fontSize=11.5, leading=14.5, textColor=C_NAVY, alignment=1)
    t_sub = ParagraphStyle('HSub', fontName='Helvetica-Bold', fontSize=8, leading=10.2, textColor=C_PRIMARY, alignment=1)
    t_meta = ParagraphStyle('HMeta', fontName='Helvetica', fontSize=6.8, leading=8.6, textColor=C_MUTED, alignment=1)

    sec_title = ParagraphStyle('SecTitle', fontName='Helvetica-Bold', fontSize=7.2, leading=9.2, textColor=C_WHITE, alignment=1)
    b_text = ParagraphStyle('BText', fontName='Helvetica', fontSize=6.2, leading=7.9, textColor=C_TEXT)
    b_bold = ParagraphStyle('BBold', fontName='Helvetica-Bold', fontSize=6.2, leading=7.9, textColor=C_NAVY)

    story = []

    # Header
    story.append(Paragraph("AI IN STRUCTURAL HEALTH MONITORING FOR PREDICTIVE MAINTENANCE &amp; SAFETY ASSURANCE", t_head))
    story.append(Paragraph("EXECUTIVE PROGRESS SUMMARY: PRIOR MDP, CURRENT IDP, DUAL-PLATFORM DEPLOYMENT &amp; PROCUREMENT PLAN", t_sub))
    story.append(Paragraph("BACSE291 -- Innovative Design Project | Fall 2026 | Vellore Institute of Technology (VIT), Vellore", t_meta))
    story.append(Paragraph("<b>Guide:</b> Dr. Senthil Kumar N (Emp ID: 15377, SCOPE) | <b>Aerial (15377IDP01):</b> Priyam S., Ayushman K. | <b>Ground (15377IDP02):</b> Nisargkumar J. (Lead), Aryan M., Mudit G.", t_meta))
    story.append(Spacer(1, 3))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_PRIMARY, spaceBefore=0, spaceAfter=3))

    # Row 1: Prior MDP & Current IDP
    q1_content = [Paragraph("<b>1. PREVIOUS MDP PROJECT: PLY FORGE POINT CLOUD PROCESSOR</b>", sec_title)]
    q1_body = Paragraph(
        "&bull; <b>Architecture &amp; Independence:</b> Client-side WebGL 1.0 3D point cloud processor in HTML5/ES6 requiring zero external libraries (no Three.js, no Node.js backend).<br/>"
        "&bull; <b>Core Capabilities:</b> Binary/ASCII PLY parser (`DataView`/`ArrayBuffer`), built-in 18,000-pt Stanford Bunny demo, circle ROI filtering, 2.5D Delaunay/grid meshing, and PLY export.<br/>"
        "&bull; <b>Voxel Downsampling:</b> 3D spatial hash map downsampling point clouds by 60%--90% while preserving structural boundaries.<br/>"
        "&bull; <b>Direct IDP Role:</b> Directly embedded into Ground Station Tab 4 (Streamlit WebGL Viewer) providing zero-latency 3D facade rendering without external desktop software.",
        b_text
    )

    q2_content = [Paragraph("<b>2. CURRENT IDP WORK DEVELOPED &amp; VERIFIED</b>", sec_title)]
    q2_body = Paragraph(
        "&bull; <b>Aerial Sensing (15377IDP01):</b> Calibrated Benewake TF-Luna 850nm dToF (&lt;5g, 0.35W, 100 Hz) on ESP32 FreeRTOS. UART sync to 0x59 0x59 with checksum verification and median filter (N=5).<br/>"
        "&bull; <b>Empirical Metrology Fit:</b> Universal regression model: <i>y = 1.0228x + 3.20 cm</i> (R<sup>2</sup>=1.0000, RMSE=&plusmn;0.02 cm across 39.0cm and 61.4cm physical benchmarks).<br/>"
        "&bull; <b>Ground Analytics (15377IDP02):</b> Rolling baseline tracking calculating geometric residuals (&Delta;d); flags spalls (&Delta;d &ge; +3.5cm) and bulges (&Delta;d &le; -3.5cm).<br/>"
        "&bull; <b>3D Digital Twin:</b> Reconstructed 9,969-point room (.PLY) isolating Almari bulge (+65cm, Orange) and Gate recess (-60cm, Green). 5-tab Streamlit dashboard active.",
        b_text
    )

    row1_table = Table([
        [q1_content, q2_content],
        [[q1_body], [q2_body]]
    ], colWidths=[270, 273])
    row1_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), C_PRIMARY),
        ('BACKGROUND', (1,0), (1,0), C_SECONDARY),
        ('BACKGROUND', (0,1), (-1,1), C_BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(row1_table)
    story.append(Spacer(1, 3))

    # Row 2: Dual-Platform Strategy & Upgrades
    q3_content = [Paragraph("<b>3. DUAL-PLATFORM STRATEGY &amp; HARDWARE UPGRADES</b>", sec_title)]
    q3_body = Paragraph(
        "&bull; <b>Platform Duality:</b> (1) <i>Autonomous F450 Drone:</i> Elevated facade &amp; bridge inspection; (2) <i>Smart 4WD Ground Car:</i> Indoor corridors, eliminating prop-wash suction &amp; hand jitter.<br/>"
        "&bull; <b>Smart 4WD Car Odometry:</b> Dual 20-slot optical wheel encoders integrate distance at ~1.02 mm/tick; closed-loop PID maintains constant 5.0 cm/s traverse; coordinates: (X_enc, d_meas*cos&theta;, Z_mast).<br/>"
        "&bull; <b>YDLIDAR X2 360&deg; LiDAR (INR 7,189.00):</b> 3,000 pts/s, 7 Hz planar rotation, 0.12--8.0m range, capturing full 2D cross-sectional wall slices in 142 ms.<br/>"
        "&bull; <b>DFRobot Gravity Tilt Sensor (INR 245.00):</b> Instant pitch/roll correction: d_true = d_meas*cos(&theta;), eliminating 3.1 cm artificial elongation false cavities.",
        b_text
    )

    q4_content = [Paragraph("<b>4. FUTURE ROADMAP &amp; SYSTEM INTEGRATION</b>", sec_title)]
    q4_body = Paragraph(
        "&bull; <b>Phase 1--2 (Weeks 1--3):</b> Procure Tier 1 hardware (LiDAR, tilt sensor, 4WD car kit); verify UART framing and 5V rail regulation.<br/>"
        "&bull; <b>Phase 3--4 (Weeks 4--6):</b> Assemble F450 airframe &amp; propulsion; implement silicone vibration-damping deck (&gt;18 dB attenuation); benchmark hover thrust.<br/>"
        "&bull; <b>Phase 5--6 (Weeks 7--10):</b> Laboratory wall scanning with Smart 4WD car (encoder odometry); tethered facade flights; blind defect detection benchmarks.<br/>"
        "&bull; <b>Phase 7 (Weeks 11--14):</b> End-to-end integration, Streamlit PLY Forge 3D meshing, automated compliance PDF reports, and IEEE conference paper submission.<br/>"
        "&bull; <b>Target Benchmarks:</b> Static distance RMSE &le; &plusmn;1.5cm; Tilt residual &le; 0.5cm; Defect sensitivity &ge; 95%; Car odometry drift &le; 1.0cm / 5m.",
        b_text
    )

    row2_table = Table([
        [q3_content, q4_content],
        [[q3_body], [q4_body]]
    ], colWidths=[270, 273])
    row2_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), C_AMBER),
        ('BACKGROUND', (1,0), (1,0), C_EMERALD),
        ('BACKGROUND', (0,1), (-1,1), C_BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(row2_table)
    story.append(Spacer(1, 3))

    # Budget Summary Mini Table
    b_sum_data = [
        [
            Paragraph("<b>Component Group</b>", ParagraphStyle('ThS', fontName='Helvetica-Bold', fontSize=6.2, textColor=C_WHITE, alignment=1)),
            Paragraph("<b>Key Inclusions &amp; Specifications</b>", ParagraphStyle('ThS', fontName='Helvetica-Bold', fontSize=6.2, textColor=C_WHITE, alignment=1)),
            Paragraph("<b>Cost (INR)</b>", ParagraphStyle('ThS', fontName='Helvetica-Bold', fontSize=6.2, textColor=C_WHITE, alignment=1)),
            Paragraph("<b>Procurement Phasing</b>", ParagraphStyle('ThS', fontName='Helvetica-Bold', fontSize=6.2, textColor=C_WHITE, alignment=1))
        ],
        [
            Paragraph("Sensors &amp; Contingency Car", b_bold),
            Paragraph("YDLIDAR X2 360&deg; LiDAR (INR 7,189), DFRobot Tilt (INR 245), Smart 4WD Car + Encoders (INR 1,750), Buck (INR 240)", b_text),
            Paragraph("INR 9,424.00", b_bold),
            Paragraph("<font color='#059669'><b>Tier 1 (Immediate Critical / Weeks 1--2)</b></font>", b_text)
        ],
        [
            Paragraph("Airframe &amp; Power Reservoir", b_bold),
            Paragraph("F450 Frame + 4x Motors + 4x ESCs (INR 5,200), 1045 Props (INR 260), 3S 4200mAh LiPo &amp; B6 Charger (INR 4,430)", b_text),
            Paragraph("INR 9,890.00", b_bold),
            Paragraph("<font color='#D97706'><b>Tier 2 (UAV Assembly / Weeks 3--4)</b></font>", b_text)
        ],
        [
            Paragraph("Avionics, Shipping &amp; Reserve", b_bold),
            Paragraph("Pixhawk 2.4.8 Kit (INR 5,950), ESP32 (INR 380), Dampers/Wire (INR 570), Shipping (INR 400), Contingency (INR 2,000)", b_text),
            Paragraph("INR 9,300.00", b_bold),
            Paragraph("<font color='#1E3A8A'><b>Tier 3 (Flight Trials / Weeks 5--6)</b></font>", b_text)
        ],
        [
            Paragraph("<b>TOTAL DUAL-PLATFORM BUDGET</b>", ParagraphStyle('ThS2', fontName='Helvetica-Bold', fontSize=6.5, textColor=C_WHITE)),
            Paragraph("<b>Complete Airborne UAV &amp; Smart 4WD Ground Robotic Car Systems</b>", ParagraphStyle('ThS2', fontName='Helvetica-Bold', fontSize=6.2, textColor=C_WHITE)),
            Paragraph("<b>INR 28,874.00</b>", ParagraphStyle('ThS2', fontName='Helvetica-Bold', fontSize=6.5, textColor=C_WHITE, alignment=1)),
            Paragraph("<b>Ground MVP Option: INR 9,964.00</b>", ParagraphStyle('ThS2', fontName='Helvetica-Bold', fontSize=6.2, textColor=C_WHITE, alignment=1))
        ]
    ]

    t_bsum = Table(b_sum_data, colWidths=[120, 243, 75, 105])
    t_bsum.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('BACKGROUND', (0,-1), (-1,-1), C_NAVY),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_bsum)

    doc.build(story)
    print(f"Successfully generated 1-page summary PDF: {PDF_NAME}")

def build_docx_summary():
    doc = docx.Document()
    for s in doc.sections:
        s.top_margin = Inches(0.4)
        s.bottom_margin = Inches(0.4)
        s.left_margin = Inches(0.45)
        s.right_margin = Inches(0.45)

    c_navy = RGBColor(0x0F, 0x17, 0x2A)
    c_primary = RGBColor(0x1E, 0x3A, 0x8A)
    c_muted = RGBColor(0x64, 0x74, 0x8B)

    p_t = doc.add_paragraph()
    p_t.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p_t.paragraph_format.space_after = Pt(1)
    r1 = p_t.add_run("AI IN STRUCTURAL HEALTH MONITORING FOR PREDICTIVE MAINTENANCE & SAFETY ASSURANCE\n")
    r1.bold = True
    r1.font.size = Pt(12)
    r1.font.color.rgb = c_navy

    r2 = p_t.add_run("EXECUTIVE PROGRESS SUMMARY: PRIOR MDP, CURRENT IDP, DUAL-PLATFORM DEPLOYMENT & PROCUREMENT PLAN\n")
    r2.bold = True
    r2.font.size = Pt(8.5)
    r2.font.color.rgb = c_primary

    r3 = p_t.add_run("BACSE291 — Innovative Design Project | Fall 2026 | Vellore Institute of Technology (VIT), Vellore\n"
                    "Guide: Dr. Senthil Kumar N (Emp ID: 15377, SCOPE) | Aerial (15377IDP01): Priyam S., Ayushman K. | Ground (15377IDP02): Nisargkumar J. (Lead), Aryan M., Mudit G.")
    r3.font.size = Pt(7.5)
    r3.font.color.rgb = c_muted

    tbl = doc.add_table(rows=2, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl)

    cells = tbl.rows[0].cells
    cells[0].paragraphs[0].add_run("1. PREVIOUS MDP: PLY FORGE POINT CLOUD PROCESSOR").bold = True
    cells[1].paragraphs[0].add_run("2. CURRENT IDP WORK DEVELOPED & VERIFIED").bold = True
    set_cell_background(cells[0], "1E3A8A")
    set_cell_background(cells[1], "0284C7")
    cells[0].paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    cells[1].paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    cells[0].paragraphs[0].runs[0].font.size = Pt(8)
    cells[1].paragraphs[0].runs[0].font.size = Pt(8)

    r1_cells = tbl.rows[1].cells
    r1_cells[0].paragraphs[0].add_run(
        "• Architecture: Client-side WebGL 1.0 3D point cloud processor in HTML5/ES6 without external libraries (no Three.js, no Node.js backend).\n"
        "• Core Capabilities: Binary/ASCII PLY parser (DataView/ArrayBuffer), 18,000-pt Stanford Bunny demo, circle ROI filtering, 2.5D Delaunay/grid meshing, and PLY export.\n"
        "• Voxel Downsampling: Spatial hash map downsampling point clouds by 60%–90% while preserving structural boundaries.\n"
        "• Direct IDP Role: Directly embedded into Ground Station Tab 4 (Streamlit WebGL Viewer) for zero-latency 3D facade rendering without external software."
    )
    r1_cells[1].paragraphs[0].add_run(
        "• Aerial Sensing (15377IDP01): Calibrated Benewake TF-Luna 850nm dToF (<5g, 0.35W, 100 Hz) on ESP32 FreeRTOS. UART sync to 0x59 0x59 with checksum and median filter (N=5).\n"
        "• Empirical Metrology Fit: Universal model: y = 1.0228x + 3.20 cm (R²=1.0000, RMSE=±0.02 cm across 39.0cm and 61.4cm physical benchmarks).\n"
        "• Ground Analytics (15377IDP02): Rolling baseline tracking calculating residuals (Δd); flags spalls (Δd ≥ +3.5cm) and bulges (Δd ≤ -3.5cm).\n"
        "• 3D Digital Twin: Reconstructed 9,969-point room (.PLY) isolating Almari bulge (+65cm) and Gate recess (-60cm). 5-tab Streamlit dashboard."
    )

    tbl2 = doc.add_table(rows=2, cols=2)
    tbl2.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl2)

    cells2 = tbl2.rows[0].cells
    cells2[0].paragraphs[0].add_run("3. DUAL-PLATFORM STRATEGY & HARDWARE UPGRADES").bold = True
    cells2[1].paragraphs[0].add_run("4. FUTURE ROADMAP & SYSTEM INTEGRATION").bold = True
    set_cell_background(cells2[0], "D97706")
    set_cell_background(cells2[1], "059669")
    cells2[0].paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    cells2[1].paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    cells2[0].paragraphs[0].runs[0].font.size = Pt(8)
    cells2[1].paragraphs[0].runs[0].font.size = Pt(8)

    r2_cells = tbl2.rows[1].cells
    r2_cells[0].paragraphs[0].add_run(
        "• Platform Duality: (1) Autonomous F450 Drone: Elevated facade inspection; (2) Smart 4WD Ground Car: Indoor corridors, eliminating prop-wash suction & hand jitter.\n"
        "• Smart 4WD Car Odometry: Dual 20-slot optical wheel encoders integrate distance at ~1.02 mm/tick; closed-loop PID maintains constant 5.0 cm/s traverse; coordinates: (X_enc, d_meas*cosθ, Z_mast).\n"
        "• YDLIDAR X2 360° LiDAR (INR 7,189): 3,000 pts/s, 7 Hz planar rotation, capturing full 2D cross-sectional wall slices in 142 ms.\n"
        "• DFRobot Gravity Tilt Sensor (INR 245): Instant pitch/roll correction: d_true = d_meas*cos(θ), eliminating 3.1 cm artificial elongation false cavities."
    )
    r2_cells[1].paragraphs[0].add_run(
        "• Phase 1–2 (Weeks 1–3): Procure Tier 1 hardware (LiDAR, tilt sensor, 4WD car kit); verify UART framing and 5V rail regulation.\n"
        "• Phase 3–4 (Weeks 4–6): Assemble F450 airframe & propulsion; implement silicone vibration-damping deck (>18 dB attenuation); benchmark hover thrust.\n"
        "• Phase 5–6 (Weeks 7–10): Laboratory wall scanning with Smart 4WD car (encoder odometry); tethered facade flights; blind defect detection.\n"
        "• Phase 7 (Weeks 11–14): End-to-end integration, Streamlit PLY Forge 3D meshing, automated compliance PDF reports, and IEEE submission.\n"
        "• Target Metrics: Static distance RMSE ≤ ±1.5cm; Tilt residual ≤ 0.5cm; Defect sensitivity ≥ 95%; Car odometry drift ≤ 1.0cm / 5m."
    )

    for t in [tbl, tbl2]:
        for row in t.rows:
            for cell in row.cells:
                set_cell_margins(cell, top=50, bottom=50, left=70, right=70)
                for p in cell.paragraphs:
                    p.paragraph_format.line_spacing = 1.05
                    for run in p.runs:
                        if run.font.size is None:
                            run.font.size = Pt(7.2)

    doc.add_paragraph().paragraph_format.space_after = Pt(2)

    # Budget Table
    btbl = doc.add_table(rows=5, cols=4)
    btbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(btbl)

    bheaders = ["Component Group", "Key Inclusions & Specifications", "Cost (INR)", "Procurement Phasing"]
    for i, h in enumerate(bheaders):
        c = btbl.rows[0].cells[i]
        c.paragraphs[0].add_run(h).bold = True
        set_cell_background(c, "1E3A8A")
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        c.paragraphs[0].runs[0].font.size = Pt(7.5)

    brows = [
        ("Sensors & Contingency Car", "YDLIDAR X2 360° LiDAR (INR 7,189), DFRobot Tilt (INR 245), Smart 4WD Car + Encoders (INR 1,750), Buck (INR 240)", "INR 9,424.00", "Tier 1 (Immediate Critical / Weeks 1–2)"),
        ("Airframe & Power Reservoir", "F450 Frame + 4x Motors + 4x ESCs (INR 5,200), 1045 Props (INR 260), 3S 4200mAh LiPo & B6 Charger (INR 4,430)", "INR 9,890.00", "Tier 2 (UAV Assembly / Weeks 3–4)"),
        ("Avionics, Shipping & Reserve", "Pixhawk 2.4.8 Kit (INR 5,950), ESP32 (INR 380), Dampers/Wire (INR 570), Shipping (INR 400), Contingency (INR 2,000)", "INR 9,300.00", "Tier 3 (Flight Trials / Weeks 5–6)"),
        ("TOTAL DUAL-PLATFORM BUDGET", "Complete Airborne UAV & Smart 4WD Ground Robotic Car Systems", "INR 28,874.00", "Ground MVP Option: INR 9,964.00")
    ]

    for r_idx, (g, k, cost, ph) in enumerate(brows):
        cells = btbl.rows[r_idx+1].cells
        is_total = (r_idx == len(brows)-1)
        for c_idx, val in enumerate([g, k, cost, ph]):
            c = cells[c_idx]
            run = c.paragraphs[0].add_run(val)
            run.font.size = Pt(7.2)
            if is_total:
                run.bold = True
                set_cell_background(c, "0F172A")
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for row in btbl.rows:
        for cell in row.cells:
            set_cell_margins(cell, top=40, bottom=40, left=60, right=60)
            for p in cell.paragraphs:
                p.paragraph_format.line_spacing = 1.05

    doc.save(DOCX_NAME)
    print(f"Successfully generated 1-page summary DOCX: {DOCX_NAME}")

if __name__ == "__main__":
    build_pdf_summary()
    build_docx_summary()
