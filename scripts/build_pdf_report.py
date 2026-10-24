import os
import sys
import shutil

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import reportlab
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

PAGE_W, PAGE_H = A4
PRINT_W = PAGE_W - 108  # 487.27 pt printable width

# Color Palette
C_NAVY = colors.HexColor('#1B365D')
C_TEAL = colors.HexColor('#008296')
C_CYAN = colors.HexColor('#00A3C4')
C_AMBER = colors.HexColor('#D97706')
C_GREEN = colors.HexColor('#059669')
C_DARK = colors.HexColor('#2D3748')
C_MUTED = colors.HexColor('#64748B')
C_LIGHT_BG = colors.HexColor('#F8FAFC')
C_ALT_BG = colors.HexColor('#EDF2F7')
C_BORDER = colors.HexColor('#CBD5E1')
C_WHITE = colors.HexColor('#FFFFFF')
C_CALLOUT_BG = colors.HexColor('#F0F9FF')
C_CALLOUT_BORDER = colors.HexColor('#BAE6FD')
C_ALERT_BG = colors.HexColor('#FEF3C7')
C_ALERT_BORDER = colors.HexColor('#FDE68A')

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            if self._pageNumber > 1:
                self.saveState()
                # Running Header
                self.setFont('Helvetica-Bold', 7.5)
                self.setFillColor(C_NAVY)
                self.drawString(54, PAGE_H - 36, "VELLORE INSTITUTE OF TECHNOLOGY · BACSE291 INNOVATIVE DESIGN PROJECT")
                self.setFont('Helvetica', 7.5)
                self.setFillColor(C_MUTED)
                self.drawRightString(PAGE_W - 54, PAGE_H - 36, "PROJECT ID: 15377IDP01 / 15377IDP02")
                self.setStrokeColor(C_BORDER)
                self.setLineWidth(0.65)
                self.line(54, PAGE_H - 42, PAGE_W - 54, PAGE_H - 42)

                # Running Footer
                self.line(54, 46, PAGE_W - 54, 46)
                self.setFont('Helvetica', 7.5)
                self.setFillColor(C_MUTED)
                self.drawString(54, 34, "AI in Structural Health Monitoring for Predictive Maintenance and Continuous Safety Assurance")
                page_text = f"Page {self._pageNumber} of {num_pages}"
                self.drawRightString(PAGE_W - 54, 34, page_text)
                self.restoreState()
            super().showPage()
        super().save()

def setup_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle('DocTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=15, leading=19, textColor=C_NAVY, alignment=1, spaceAfter=3))
    styles.add(ParagraphStyle('DocSub', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9.5, leading=13, textColor=C_TEAL, alignment=1, spaceAfter=8))
    styles.add(ParagraphStyle('CoverInstitution', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=C_NAVY, alignment=1, spaceAfter=2))
    styles.add(ParagraphStyle('CoverSchool', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=12, textColor=C_DARK, alignment=1, spaceAfter=6))
    
    styles.add(ParagraphStyle('SecH1', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10.5, leading=14, textColor=C_NAVY, spaceBefore=10, spaceAfter=3.5, keepWithNext=True))
    styles.add(ParagraphStyle('SecH2', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=C_TEAL, spaceBefore=7, spaceAfter=2.5, keepWithNext=True))
    styles.add(ParagraphStyle('SecH3', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=11, textColor=C_DARK, spaceBefore=5, spaceAfter=2, keepWithNext=True))
    styles.add(ParagraphStyle('BodyDark', parent=styles['Normal'], fontName='Helvetica', fontSize=7.5, leading=10.5, textColor=C_DARK, spaceBefore=0, spaceAfter=3))
    styles.add(ParagraphStyle('BulletDark', parent=styles['Normal'], fontName='Helvetica', fontSize=7.5, leading=10, textColor=C_DARK, leftIndent=11, firstLineIndent=-7, spaceBefore=1, spaceAfter=1.5))
    
    styles.add(ParagraphStyle('CalloutTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.5, leading=10, textColor=C_NAVY, spaceBefore=0, spaceAfter=1.5))
    styles.add(ParagraphStyle('CalloutText', parent=styles['Normal'], fontName='Helvetica', fontSize=7, leading=9.5, textColor=C_DARK, spaceBefore=0, spaceAfter=0))
    
    styles.add(ParagraphStyle('TableHead', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=6.5, leading=8.5, textColor=C_WHITE, alignment=1))
    styles.add(ParagraphStyle('TableCell', parent=styles['Normal'], fontName='Helvetica', fontSize=6.5, leading=8.5, textColor=C_DARK))
    styles.add(ParagraphStyle('TableCellBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=6.5, leading=8.5, textColor=C_DARK))
    styles.add(ParagraphStyle('TableCellCenter', parent=styles['Normal'], fontName='Helvetica', fontSize=6.5, leading=8.5, textColor=C_DARK, alignment=1))
    styles.add(ParagraphStyle('ImgCaption', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=6.5, leading=8.5, textColor=C_MUTED, alignment=1, spaceBefore=2, spaceAfter=4))
    
    return styles

def make_callout(styles, title_text, body_text, bg_hex=C_CALLOUT_BG, border_hex=C_CALLOUT_BORDER):
    content = [
        Paragraph(title_text, styles['CalloutTitle']),
        Spacer(1, 1.5),
        Paragraph(body_text.replace('\n', '<br/>'), styles['CalloutText'])
    ]
    t = Table([[content]], colWidths=[PRINT_W])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_hex),
        ('BOX', (0,0), (-1,-1), 0.65, border_hex),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    return t

def generate_pdf(filename="BACSE291_RESEARCH_PROGRESS_REPORT_AND_FUTURE_WORK_PLAN.pdf"):
    styles = setup_styles()
    story = []

    # ==================================================================================
    # SECTION 1: COVER PAGE
    # ==================================================================================
    vit_logo_path = "reports/assets/vit_logo.png"
    if os.path.exists(vit_logo_path):
        logo_img = Image(vit_logo_path, width=115, height=40.6)
        header_text = [
            Paragraph("<b>VELLORE INSTITUTE OF TECHNOLOGY (VIT), VELLORE</b>", styles['CoverInstitution']),
            Paragraph("School of Computer Science and Engineering (SCOPE) &amp; School of Civil Engineering (SCE)<br/><b>BACSE291 – Innovative Design Project</b> · Fall Semester 2026", styles['CoverSchool'])
        ]
        head_table = Table([[logo_img, header_text]], colWidths=[125, PRINT_W - 125])
        head_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (0,0), (0,0), 'LEFT'),
            ('ALIGN', (1,0), (1,0), 'CENTER'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(head_table)
    else:
        story.append(Paragraph("<b>VELLORE INSTITUTE OF TECHNOLOGY (VIT), VELLORE</b>", styles['CoverInstitution']))
        story.append(Paragraph("School of Computer Science and Engineering (SCOPE) &amp; School of Civil Engineering (SCE)", styles['CoverSchool']))

    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_NAVY, spaceBefore=2, spaceAfter=6))

    story.append(Paragraph("AI IN STRUCTURAL HEALTH MONITORING FOR PREDICTIVE MAINTENANCE AND CONTINUOUS SAFETY ASSURANCE", styles['DocTitle']))
    story.append(Paragraph("Comprehensive Research Progress Report &amp; Future Work Plan<br/>(Review 1 to Review 3 Synthesis, Subsystem Architecture &amp; Milestone R1 Roadmap)", styles['DocSub']))
    story.append(Spacer(1, 4))

    # Metadata Table
    p_meta = [
        [
            Paragraph("<b>PROJECT IDENTIFIER:</b>", styles['TableCellBold']),
            Paragraph("15377IDP01 (Aerial Subsystem) &amp; 15377IDP02 (Ground Analytics Subsystem)", styles['TableCell']),
            Paragraph("<b>COURSE / SEMESTER:</b>", styles['TableCellBold']),
            Paragraph("BACSE291 – Innovative Design Project (Fall 2026)", styles['TableCell'])
        ],
        [
            Paragraph("<b>PROJECT GUIDE:</b>", styles['TableCellBold']),
            Paragraph("Dr. N. Senthil Kumar, Ph.D (IITM), Assoc. Professor Grade 2 (SCE)", styles['TableCell']),
            Paragraph("<b>REPORTING MILESTONE:</b>", styles['TableCellBold']),
            Paragraph("Progress Review &amp; Future Engineering Plan (Rev. R0)", styles['TableCell'])
        ]
    ]
    meta_table = Table(p_meta, colWidths=[105, 145, 110, 127])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 0.75, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 6))

    # All 5 Team Members Table
    story.append(Paragraph("<b>PROJECT RESEARCH TEAM (ALL 5 MEMBERS ACROSS SUBSYSTEMS 1 &amp; 2):</b>", styles['SecH3']))
    team_rows = [
        [
            Paragraph("S.No", styles['TableHead']),
            Paragraph("Student Name", styles['TableHead']),
            Paragraph("Register No.", styles['TableHead']),
            Paragraph("School", styles['TableHead']),
            Paragraph("Subsystem &amp; Primary Role", styles['TableHead']),
            Paragraph("Assigned Work Package", styles['TableHead'])
        ],
        [
            Paragraph("1", styles['TableCellCenter']),
            Paragraph("<b>Nisargkumar Piyushkumar Joshi</b>", styles['TableCellBold']),
            Paragraph("25BCE0594", styles['TableCellCenter']),
            Paragraph("SCOPE", styles['TableCellCenter']),
            Paragraph("Subsystem 2 Lead (Ground Analytics)", styles['TableCell']),
            Paragraph("Linear regression calibration (y=1.0228x+3.20), 3D WebGL engine &amp; spatial metrology", styles['TableCell'])
        ],
        [
            Paragraph("2", styles['TableCellCenter']),
            Paragraph("<b>Aryan Pranit Mithari</b>", styles['TableCellBold']),
            Paragraph("25BAI0115", styles['TableCellCenter']),
            Paragraph("SCOPE", styles['TableCellCenter']),
            Paragraph("Subsystem 2 (Ground Analytics)", styles['TableCell']),
            Paragraph("Baseline deviation (&Delta;d) calculation, serial pipeline &amp; anomaly detection rules", styles['TableCell'])
        ],
        [
            Paragraph("3", styles['TableCellCenter']),
            Paragraph("<b>Mudit Gupta</b>", styles['TableCellBold']),
            Paragraph("25BA0110", styles['TableCellCenter']),
            Paragraph("SCOPE", styles['TableCellCenter']),
            Paragraph("Subsystem 2 (Ground Analytics)", styles['TableCell']),
            Paragraph("Geometric defect classification (cavity, bulge, crack-like) &amp; .PLY point cloud export", styles['TableCell'])
        ],
        [
            Paragraph("4", styles['TableCellCenter']),
            Paragraph("<b>Priyam Sharma</b>", styles['TableCellBold']),
            Paragraph("25BAI0159", styles['TableCellCenter']),
            Paragraph("SCOPE", styles['TableCellCenter']),
            Paragraph("Subsystem 1 (Aerial Sensing)", styles['TableCell']),
            Paragraph("TF-Luna ToF rangefinding payload, MCU hardware wiring &amp; power regulation", styles['TableCell'])
        ],
        [
            Paragraph("5", styles['TableCellCenter']),
            Paragraph("<b>Ayushman Kaushik</b>", styles['TableCellBold']),
            Paragraph("25BCE0927", styles['TableCellCenter']),
            Paragraph("SCOPE", styles['TableCellCenter']),
            Paragraph("Subsystem 1 (Aerial Sensing)", styles['TableCell']),
            Paragraph("9-byte UART binary frame parser, checksum verification &amp; wireless telemetry link", styles['TableCell'])
        ]
    ]
    team_table = Table(team_rows, colWidths=[22, 115, 60, 42, 110, 138])
    team_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('BOX', (0,0), (-1,-1), 0.75, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_WHITE, C_LIGHT_BG]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(team_table)
    story.append(Spacer(1, 6))

    # Executive Overview Callout Box
    story.append(make_callout(
        styles,
        "EXECUTIVE SUMMARY &amp; FACULTY EVALUATION SCOPE:",
        "This progress report presents the completed milestones, ongoing engineering investigations, and future research work for our Innovative Design Project. The system integrates a lightweight 850nm ToF Micro-LiDAR on an ESP-32 microcontroller with a ground analytics DSP engine and 3D WebGL digital twin platform. Key achievements to date include hardware bench acquisition at 60-100 Hz, sub-centimeter linear calibration (y = 1.0228x + 3.20 cm, R² = 1.0000), 4-wall sequential room twin reconstruction (9,969 vertices), and real-time classification of planar walls, Almari inward bulges, and Gate recesses. The next phase focuses on ADXL345 dynamic tilt compensation, 2D 360° LiDAR integration, wireless UDP telemetry, dynamic coordinate tracking from initial datum (0,0,0), and a dual-platform deployment strategy (drone payload with smart ground car contingency)."
    ))

    story.append(PageBreak())

    # ==================================================================================
    # SECTION 2: PROJECT OVERVIEW
    # ==================================================================================
    story.append(Paragraph("2. Project Overview &amp; Research Motivation", styles['SecH1']))
    story.append(Paragraph(
        "Civil infrastructure worldwide—including highway bridges, concrete columns, retaining walls, tunnels, and residential complexes—is subjected to continuous structural fatigue caused by environmental weathering, seismic vibrations, ground settlement, and heavy cyclic loads. Structural Health Monitoring (SHM) is the discipline of tracking physical integrity over time to detect early-stage damage before catastrophic collapse occurs.",
        styles['BodyDark']
    ))
    story.append(Paragraph(
        "<b>The Traditional Inspection Bottleneck:</b> Current industrial civil inspection relies predominantly on manual visual observation and physical measuring tapes, often requiring personnel to deploy hazardous scaffolding, cherry-pickers, or rope-access rigs. This practice has three fatal weaknesses: (1) <b>High Danger &amp; Cost:</b> Inspecting high-altitude facades or bridge piers is labor-intensive and life-threatening; (2) <b>Human Parallax &amp; Sag Error:</b> Measuring tapes sag and bend over spans exceeding 3 meters, introducing random errors of &plusmn;2 to 5 cm; and (3) <b>Depth Blindness:</b> Optical cameras and human visual inspections capture 2D surface discoloration and hairline cracks but cannot quantify 3D metric volume loss, subsurface cavities, plaster delamination bulges, or structural wall tilt.",
        styles['BodyDark']
    ))
    story.append(Paragraph(
        "<b>Our Engineering Objective:</b> We develop an autonomous, cost-effective robotic metrology and digital twin pipeline that captures millimeter-accurate physical distance at up to 100 Hz, executes real-time sensor calibration, computes planar wall deviations (&Delta;d), isolates structural anomalies, and renders interactive 3D WebGL point clouds (.PLY/.OBJ) with zero server dependencies.",
        styles['BodyDark']
    ))

    # ==================================================================================
    # SECTION 3: WORK COMPLETED PREVIOUSLY (REVIEW 1 TO REVIEW 3)
    # ==================================================================================
    story.append(Paragraph("3. Work Completed Previously (Review 1 Through Review 3)", styles['SecH1']))
    story.append(Paragraph(
        "Across earlier evaluation reviews (Review 1 through Review 3), the team successfully established the theoretical foundation, physical sensing hardware, mathematical calibration, and 3D digital twin visualization pipeline:",
        styles['BodyDark']
    ))
    
    story.append(Paragraph("• <b>Review 1 — Literature Survey &amp; Scoping:</b> Conducted a comprehensive survey of 25 peer-reviewed papers (SCI/Scopus indexed) across UAV inspection, Time-of-Flight ranging, and vibration isolation. Formulated five core research gaps and decomposed the project into Subsystem 1 (Aerial Payload) and Subsystem 2 (Ground Analytics).", styles['BulletDark']))
    story.append(Paragraph("• <b>Review 2 — Hardware Bench Prototyping &amp; Calibration:</b> Built the benchtop sensing rig combining an ESP-32 DevKit MCU with the Benewake TF-Luna 850nm ToF LiDAR over hardware UART (Serial2). Programmed binary frame decoding with 9-byte modular checksum verification. Derived the exact linear regression calibration model: Calibrated Distance = 1.0228 &times; Raw + 3.20 cm (R² = 1.0000, RMSE = &plusmn;0.02 cm), resolving the intrinsic optical casing delay.", styles['BulletDark']))
    story.append(Paragraph("• <b>Review 3 — Sequential 4-Wall Scanning &amp; 3D Twin Extrusion:</b> Engineered <code>continuous_multi_point_scanner.py</code>, executing sequential wall scanning across North, East, South, and West baselines. Reconstructed a watertight 4.80m &times; 4.80m room digital twin comprising 9,969 points (<code>room_mesh.ply</code> and <code>room_mesh.obj</code>). Created the standalone Three.js WebGL viewer (<code>real_scan_3d_viewer.html</code>) with toggleable 3D dimension banners and feature callouts.", styles['BulletDark']))

    # Side-by-side Hardware Photographs Table
    hw_img_path = "reports/assets/hardware_bench_setup.png"
    drone_img_path = "reports/assets/drone_airframe.png"
    if os.path.exists(hw_img_path) and os.path.exists(drone_img_path):
        img_hw = Image(hw_img_path, width=170, height=137.7)
        img_dr = Image(drone_img_path, width=135, height=139.9)
        hw_table = Table([
            [img_hw, img_dr],
            [
                Paragraph("<b>Figure 1:</b> Actual Bench Hardware Assembly<br/>(ESP-32 MCU + TF-Luna ToF LiDAR via UART)", styles['ImgCaption']),
                Paragraph("<b>Figure 2:</b> Custom Carbon Fiber Quadcopter Airframe<br/>(Brushless motors, PDB, flight controller bay)", styles['ImgCaption'])
            ]
        ], colWidths=[245, 242])
        hw_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
            ('TOPPADDING', (0,0), (-1,-1), 1),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ]))
        story.append(KeepTogether([hw_table]))

    # ==================================================================================
    # SECTION 4: CURRENT WORK IN PROGRESS
    # ==================================================================================
    story.append(Paragraph("4. Current Work in Progress", styles['SecH1']))
    story.append(Paragraph(
        "At present, both subsystems are actively tackling specific signal-processing and embedded hardware refinements to elevate the system from laboratory bench validation to robust physical operation:",
        styles['BodyDark']
    ))
    
    story.append(Paragraph("<b>1. Resolving Sliding Noise vs. Defect Sensitivity Overlap:</b> During physical testing, manually sliding the sensor along a wall surface introduces mechanical hand jitter of approximately &plusmn;2 to 3 cm. Because true civil defects (such as shallow concrete spalling or plaster delamination) often manifest at depths of 2.5 to 3.5 cm, raw thresholding causes false anomaly triggers. We are actively refining an 8-sample rolling median filter (N = 8) combined with multi-pass spatial persistence gating (requiring &ge; 12 consecutive anomalous pulses) to eliminate sliding noise.", styles['BulletDark']))
    story.append(Paragraph("<b>2. Enhancing Feature Discrimination (Macro vs. Micro):</b> Currently, the system reliably identifies macro-architectural elements: Normal Wall baseline (Cyan, |&Delta;d| &lt; 15 cm), Almari/Wardrobe inward protrusions (Orange, &Delta;d &le; -15 cm), and Gate/Doorway outward recesses (Green, &Delta;d &ge; +15 cm). Work is in progress to distinguish fine structural cracks and spalling from standard architectural mouldings using reflected optical signal strength (flux amplitude).", styles['BulletDark']))
    story.append(Paragraph("<b>3. ADXL345 3-Axis Accelerometer / Tilt Sensor Integration:</b> To eliminate distance stretching caused by sensor pitch and roll tilt (d_true = d_meas &middot; cos(&theta;_tilt)), we are breadboarding the ADXL345 digital accelerometer over I2C to stream real-time tilt angles and dynamic motor vibration data into the ESP-32 telemetry frame.", styles['BulletDark']))
    story.append(Paragraph("<b>4. Wireless Telemetry Link Implementation:</b> Transitioning from wired USB-serial CSV logging to real-time wireless Wi-Fi UDP streaming from the ESP-32 aerial payload to the ground station receiver.", styles['BulletDark']))

    # Status Assessment Table
    status_data = [
        [Paragraph("Subsystem Activity", styles['TableHead']), Paragraph("Target Scope", styles['TableHead']), Paragraph("Engineering Status", styles['TableHead']), Paragraph("Supporting Evidence", styles['TableHead'])],
        [Paragraph("UART Checksum Parsing", styles['TableCellBold']), Paragraph("Subsystem 1 (Aerial)", styles['TableCell']), Paragraph("<font color='#059669'><b>COMPLETED</b></font>", styles['TableCellCenter']), Paragraph("<code>tf_luna_code.ino</code> running at 115200 baud", styles['TableCell'])],
        [Paragraph("Linear Regression Calibration", styles['TableCellBold']), Paragraph("Subsystem 2 (Ground)", styles['TableCell']), Paragraph("<font color='#059669'><b>COMPLETED</b></font>", styles['TableCellCenter']), Paragraph("y = 1.0228x + 3.20 cm (R² = 1.0000, &plusmn;0.02 cm)", styles['TableCell'])],
        [Paragraph("4-Wall Room Twin Extrusion", styles['TableCellBold']), Paragraph("Subsystem 2 (Ground)", styles['TableCell']), Paragraph("<font color='#059669'><b>COMPLETED</b></font>", styles['TableCellCenter']), Paragraph("9,969-point <code>room_mesh.ply</code> with Three.js viewer", styles['TableCell'])],
        [Paragraph("Sliding Jitter vs Defect Tuning", styles['TableCellBold']), Paragraph("Subsystem 2 (Ground)", styles['TableCell']), Paragraph("<font color='#D97706'><b>IN PROGRESS</b></font>", styles['TableCellCenter']), Paragraph("Median filter N=8 + 12-sample cluster threshold", styles['TableCell'])],
        [Paragraph("ADXL345 Tilt &amp; Vibration Sensor", styles['TableCellBold']), Paragraph("Subsystem 1 (Aerial)", styles['TableCell']), Paragraph("<font color='#D97706'><b>IN PROGRESS</b></font>", styles['TableCellCenter']), Paragraph("I2C driver integration for pitch/roll Euler correction", styles['TableCell'])],
        [Paragraph("Wireless Wi-Fi / UDP Telemetry", styles['TableCellBold']), Paragraph("Subsystems 1 &amp; 2", styles['TableCell']), Paragraph("<font color='#D97706'><b>IN PROGRESS</b></font>", styles['TableCellCenter']), Paragraph("UDP packet framing with sequence numbers", styles['TableCell'])],
        [Paragraph("Flight &amp; Rover Field Testing", styles['TableCellBold']), Paragraph("Subsystems 1 &amp; 2", styles['TableCell']), Paragraph("<font color='#1B365D'><b>PLANNED</b></font>", styles['TableCellCenter']), Paragraph("Tethered flight &amp; embedded smart car rover tests", styles['TableCell'])]
    ]
    st_table = Table(status_data, colWidths=[120, 95, 82, 190])
    st_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('BOX', (0,0), (-1,-1), 0.75, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_WHITE, C_LIGHT_BG]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(KeepTogether([st_table]))

    # ==================================================================================
    # SECTION 5: IDENTIFIED RESEARCH GAPS
    # ==================================================================================
    story.append(Paragraph("5. Identified Research Gaps (Literature Synthesis)", styles['SecH1']))
    story.append(Paragraph(
        "Synthesizing the 25 peer-reviewed papers examined during Review 1 reveals five distinct research gaps that directly justify our project's hardware, calibration, and algorithmic architecture:",
        styles['BodyDark']
    ))

    gaps = [
        ("Gap 1: Cost &amp; Weight Bottleneck in 3D Structural LiDAR [Ref: Papers 2, 5, 11, 19]",
         "Commercial Terrestrial Laser Scanners (TLS) and multi-beam LiDARs offer sub-millimeter precision but weigh &gt; 1.2 kg and cost $15,000 to $30,000, making them completely impractical for low-cost micro-drones. Our response is a sub-5g, &lt; $25 single-point ToF LiDAR (TF-Luna) coupled with algorithmic 3D spatial extrusion."),
        ("Gap 2: Optical Zero-Point Bias &amp; Parallax Drift in Low-Cost ToF [Ref: Papers 10, 14, 17, 22]",
         "Low-cost ToF sensors exhibit internal optical casing offsets (~3 to 4 cm) and blind zones (&lt; 20 cm) due to physical emitter-receiver lens parallax. Existing studies often ignore this housing bias. Our response is a dual-point linear regression model (y = 1.0228x + 3.20 cm, R² = 1.0000) running directly in firmware with automated blind-zone warning triggers."),
        ("Gap 3: Sensor Blindness in Vision-Only Defect Detection [Ref: Papers 1, 3, 7, 8, 18]",
         "Computer vision algorithms (CNNs, YOLOv8) segment surface cracks effectively from RGB images but cannot quantify physical depth or volumetric cavity loss. Furthermore, cameras fail under poor illumination, shadows, and featureless concrete surfaces. Our response uses metric LiDAR distance as the primary ground-truth signal."),
        ("Gap 4: Dynamic Vibration &amp; Angular Tilt Distortion [Ref: Papers 4, 5, 6, 24]",
         "When a sensor is mounted on an aerial platform, propeller vibrations introduce high-frequency noise spikes, while quadcopter pitch and roll tilt angles (&theta;_tilt) artificially stretch the measured distance (d_meas = d_true / cos(&theta;_tilt)). Our response incorporates passive silicone damping pads and ADXL345 digital tilt telemetry to apply trigonometric Euler correction."),
        ("Gap 5: Static Origin Assumption vs. Dynamic Spatial Translation [Ref: Papers 13, 20, 25]",
         "Most low-cost scanners assume the sensor remains at a static origin. When the operator or robot moves through space, points collapse into overlapping clusters. Our response implements dynamic origin tracking from an initial datum (0,0,0) to spatial displacement coordinates (X, Y, Z).")
    ]
    for g_title, g_desc in gaps:
        story.append(Paragraph(f"• <b>{g_title}</b>: {g_desc}", styles['BulletDark']))

    # ==================================================================================
    # SECTION 6: PROPOSED SOLUTION & TECHNICAL DESIGN
    # ==================================================================================
    story.append(Paragraph("6. Proposed Solution &amp; Technical System Design", styles['SecH1']))
    story.append(Paragraph(
        "Our system employs a modular, dual-subsystem architecture designed to acquire, calibrate, transmit, and visualize 3D structural condition data in real time:",
        styles['BodyDark']
    ))

    # Architecture Overview Callout
    story.append(make_callout(
        styles,
        "SUBSYSTEM ARCHITECTURE &amp; DATA FLOW PIPELINE:",
        "1. SENSING PAYLOAD (Team 1): Benewake TF-Luna (850nm ToF) + ADXL345 (3-Axis Tilt/Vibration) wired to ESP-32 DevKit MCU via UART & I2C.\n"
        "2. ON-CHIP PROCESSING: 9-byte binary parsing, checksum validation, linear regression calibration (y = 1.0228x + 3.20 cm), and 8-sample moving average filter.\n"
        "3. TELEMETRY LINK: USB-Serial stream (current bench) transitioning to ESP-32 Wi-Fi UDP wireless transmission.\n"
        "4. GROUND ANALYTICS (Team 2): Baseline planar fitting, deviation computation (&Delta;d), rule-based structural anomaly tagging (cavity, bulge, crack-like).\n"
        "5. 3D METROLOGY & DIGITAL TWIN: Sequential 4-wall spatial extrusion into 9,969-point .PLY/.OBJ models rendered in Three.js WebGL with dimension callouts."
    ))
    story.append(Spacer(1, 4))

    # THE GUIDE'S CORE CONCEPT: COORDINATE TRANSFORMATION & DRAGGING
    story.append(Paragraph("6.1 Dynamic Coordinate Tracking Model (Guide's Core Principle)", styles['SecH2']))
    story.append(Paragraph(
        "A critical conceptual requirement emphasized during project evaluation is the mathematical formulation of sensor motion. When moving, sliding, or dragging the scanner across physical space, the system must not assume that every reading originates from a stationary center. Instead, the sensor's own spatial trajectory must be dynamically tracked from an initial datum of (0, 0, 0):",
        styles['BodyDark']
    ))

    story.append(make_callout(
        styles,
        "DYNAMIC COORDINATE DISPLACEMENT &amp; PROJECTION FORMULATION:",
        "1. INITIAL ORIGIN DATUM (t = 0): At the start of scanning, the initial physical position is defined as the absolute World Origin:\n"
        "   P_sensor(0) = [X₀, Y₀, Z₀]ᵀ = [0.000, 0.000, 0.000]ᵀ\n\n"
        "2. TRANSLATION VECTOR (t > 0): As the scanner is dragged, moved, or flown across physical axes:\n"
        "   P_sensor(t) = P_sensor(0) + &Delta;T(t) = [0 + &Delta;X(t),  0 + &Delta;Y(t),  0 + &Delta;Z(t)]ᵀ\n"
        "   where &Delta;X(t) is lateral displacement along wall width, &Delta;Y(t) is vertical elevation/height, and &Delta;Z(t) is longitudinal depth.\n\n"
        "3. GLOBAL TARGET POINT TRANSFORMATION: For calibrated distance d(t) at azimuth angle &theta; and tilt angles (pitch &phi;, roll &psi; from ADXL345):\n"
        "   P_target, global(t) = P_sensor(t) + R_tilt(&phi;, &psi;) &middot; [d(t) &middot; sin(&theta;),  d(t) &middot; sin(&phi;),  d(t) &middot; cos(&theta;)]ᵀ\n\n"
        "Significance: Dynamic origin tracking ensures that points mapped during a continuous sweep are placed at their true global coordinates, preventing point cloud collapse and preserving metric realism.",
        bg_hex=C_ALERT_BG,
        border_hex=C_ALERT_BORDER
    ))
    story.append(Spacer(1, 3))

    # DUAL-PLATFORM CONTINGENCY STRATEGY
    story.append(Paragraph("6.2 Dual-Platform Deployment Strategy: Primary Drone vs. Embedded Smart Ground Rover", styles['SecH2']))
    story.append(Paragraph(
        "To guarantee experimental success and eliminate single-point operational failure, we adopt a dual-platform strategy: (1) <b>Primary Aerial Platform:</b> A custom carbon fiber quadcopter UAV designed for elevated facade and high-altitude bridge pier inspection, featuring a silicone-damped sensor mount; (2) <b>Contingency Embedded Ground Platform:</b> If indoor safety regulations, hover turbulence, or GPS-denied aerodynamic drift impede flight, the identical embedded LiDAR + ADXL345 + ESP32 payload is mounted onto an <b>Autonomous Smart Ground Car (4WD Robotic Rover)</b> equipped with optical wheel encoders. The rover executes dead-reckoning odometry to measure exact displacement (&Delta;X, &Delta;Z) along the floor baseline, validating the dynamic coordinate transformation model with zero risk of drone crash.",
        styles['BodyDark']
    ))

    # Embedded 3D Digital Twin Screenshot
    twin_img_path = "reports/room_mesh_3d_model.png"
    if os.path.exists(twin_img_path):
        img_twin = Image(twin_img_path, width=460, height=196.9)
        twin_tbl = Table([[img_twin], [Paragraph("<b>Figure 3:</b> Actual 3D Digital Twin Point Cloud (9,969 vertices) rendered in Three.js WebGL, showing orthogonal Cyan baseline walls (4.8m &times; 4.8m), inward-bulging Almari (Orange, 65 cm Bahar), and outward-recessed Gate (Green, 60 cm Andar).", styles['ImgCaption'])]], colWidths=[PRINT_W])
        twin_tbl.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('TOPPADDING', (0,0), (-1,-1), 1), ('BOTTOMPADDING', (0,0), (-1,-1), 1)]))
        story.append(KeepTogether([twin_tbl]))

    # ==================================================================================
    # SECTION 7: WORK PLANNED FOR THE FUTURE (MILESTONE R1 ROADMAP)
    # ==================================================================================
    story.append(Paragraph("7. Work Planned for the Future (Milestone R1 Roadmap)", styles['SecH1']))
    story.append(Paragraph(
        "To advance the research from our validated baseline to an end-to-end autonomous inspection platform, the work is structured into five sequential phases:",
        styles['BodyDark']
    ))

    future_phases = [
        ("Phase 1: ADXL345 Dynamic Tilt Compensation &amp; Vibration Filtering",
         "Implement I2C drivers for the ADXL345 sensor on ESP-32. Program real-time trigonometric Euler angle correction: d_true = d_meas &middot; cos(&theta;_tilt). Apply digital bandpass filtering to isolate propeller vibration signatures (100–300 Hz) from physical structural deviations."),
        ("Phase 2: Sensor Upgrade to 2D 360° Scanning LiDAR (TF-Luna + YDLIDAR Hybrid)",
         "Procure and integrate a 2D 360° rotating laser range scanner (YDLIDAR X4 / LD06 / RPLiDAR A1). In contrast to manual sequential wall sweeping, a 2D LiDAR captures full 360° room cross-sections at 5.5–10 Hz (3,000–5,000 pts/sec), enabling instantaneous planar room closure and 2D SLAM occupancy grid generation."),
        ("Phase 3: Wireless UDP Telemetry Link Handoff",
         "Establish low-latency wireless UDP packet streaming over ESP-32 Wi-Fi. Incorporate 16-bit packet sequence numbering to detect and report packet drop percentages directly to the ground station dashboard."),
        ("Phase 4: Experimental Field Testing on Dual Platforms (Rover &amp; Drone)",
         "Conduct comparative scanning trials across laboratory test walls with simulated defects. Evaluate scanning accuracy, point density, and vibration rejection on: (a) the embedded smart ground car rover, and (b) the tethered quadcopter UAV payload."),
        ("Phase 5: Longitudinal Predictive Maintenance Analytics",
         "Develop cloud/local historical database integration to compare dated scan point clouds of the same physical structure over time, computing time-series deterioration trends (&Delta;d progression) for predictive maintenance decision support.")
    ]
    for p_title, p_desc in future_phases:
        story.append(Paragraph(f"• <b>{p_title}</b>: {p_desc}", styles['BulletDark']))

    # ==================================================================================
    # SECTION 8: TIMELINE AND MILESTONES TABLE
    # ==================================================================================
    story.append(Paragraph("8. Timeline and Milestones Table", styles['SecH1']))
    story.append(Paragraph("The research execution plan spans a 12-week schedule aligned with university evaluation stages:", styles['BodyDark']))

    gantt_rows = [
        [
            Paragraph("Phase", styles['TableHead']),
            Paragraph("Core Activity / Milestone", styles['TableHead']),
            Paragraph("Subsystem", styles['TableHead']),
            Paragraph("Status", styles['TableHead']),
            Paragraph("Planned Period", styles['TableHead']),
            Paragraph("Expected Deliverable", styles['TableHead'])
        ],
        [
            Paragraph("P1", styles['TableCellCenter']),
            Paragraph("Literature Survey &amp; 25-Paper Review", styles['TableCell']),
            Paragraph("Joint (Team 1 &amp; 2)", styles['TableCell']),
            Paragraph("<font color='#059669'><b>Completed</b></font>", styles['TableCellCenter']),
            Paragraph("Weeks 1–2", styles['TableCellCenter']),
            Paragraph("Review 1 Presentation &amp; Gap Analysis Table", styles['TableCell'])
        ],
        [
            Paragraph("P2", styles['TableCellCenter']),
            Paragraph("TF-Luna UART &amp; Linear Calibration (y=1.0228x+3.20)", styles['TableCell']),
            Paragraph("Team 1 (Aerial)", styles['TableCell']),
            Paragraph("<font color='#059669'><b>Completed</b></font>", styles['TableCellCenter']),
            Paragraph("Weeks 3–4", styles['TableCellCenter']),
            Paragraph("Bench firmware, ring buffer, calibration.json", styles['TableCell'])
        ],
        [
            Paragraph("P3", styles['TableCellCenter']),
            Paragraph("4-Wall Room Twin Extrusion &amp; WebGL Viewer", styles['TableCell']),
            Paragraph("Team 2 (Ground)", styles['TableCell']),
            Paragraph("<font color='#059669'><b>Completed</b></font>", styles['TableCellCenter']),
            Paragraph("Weeks 5–6", styles['TableCellCenter']),
            Paragraph("9,969-pt room_mesh.ply, Three.js HTML suite", styles['TableCell'])
        ],
        [
            Paragraph("P4", styles['TableCellCenter']),
            Paragraph("Sliding Noise Reduction &amp; ADXL345 Tilt Setup", styles['TableCell']),
            Paragraph("Joint (Team 1 &amp; 2)", styles['TableCell']),
            Paragraph("<font color='#D97706'><b>In Progress</b></font>", styles['TableCellCenter']),
            Paragraph("Weeks 7–8", styles['TableCellCenter']),
            Paragraph("ADXL345 I2C driver, persistence filter, R0 Doc", styles['TableCell'])
        ],
        [
            Paragraph("P5", styles['TableCellCenter']),
            Paragraph("2D 360° LiDAR Integration &amp; Wireless UDP", styles['TableCell']),
            Paragraph("Team 1 (Aerial)", styles['TableCell']),
            Paragraph("<font color='#1B365D'><b>Planned</b></font>", styles['TableCellCenter']),
            Paragraph("Weeks 9–10", styles['TableCellCenter']),
            Paragraph("YDLIDAR turret mount, Wi-Fi UDP packet parser", styles['TableCell'])
        ],
        [
            Paragraph("P6", styles['TableCellCenter']),
            Paragraph("Dual-Platform Testing (Car Rover &amp; Drone Flights)", styles['TableCell']),
            Paragraph("Joint (Team 1 &amp; 2)", styles['TableCell']),
            Paragraph("<font color='#1B365D'><b>Planned</b></font>", styles['TableCellCenter']),
            Paragraph("Weeks 11–12", styles['TableCellCenter']),
            Paragraph("Field metrology validation, final report &amp; demo", styles['TableCell'])
        ]
    ]
    gantt_table = Table(gantt_rows, colWidths=[22, 126, 75, 52, 60, 152])
    gantt_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('BOX', (0,0), (-1,-1), 0.75, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_WHITE, C_LIGHT_BG]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(KeepTogether([gantt_table]))

    # ==================================================================================
    # SECTION 9: CHALLENGES, RISKS & MITIGATION STRATEGIES
    # ==================================================================================
    story.append(Paragraph("9. Challenges, Risks &amp; Mitigation Strategies", styles['SecH1']))
    
    risks_data = [
        [Paragraph("Observed Challenge / Anticipated Risk", styles['TableHead']), Paragraph("Impact on System", styles['TableHead']), Paragraph("Practical Technical Mitigation Strategy", styles['TableHead'])],
        [
            Paragraph("<b>Propeller Vibration Interference:</b> High-frequency motor oscillations (&gt;100 Hz) cause distance jitter.", styles['TableCell']),
            Paragraph("False defect classification spikes in distance telemetry.", styles['TableCell']),
            Paragraph("Dual-stage mechanical silicone damping mount + ADXL345 accelerometer bandpass filtering + digital rolling median (N=8).", styles['TableCell'])
        ],
        [
            Paragraph("<b>Angular Pitch/Roll Tilt Distortion:</b> Drone or rover tilt stretches beam distance (d/cos&theta;).", styles['TableCell']),
            Paragraph("False wall recession error and distorted room twin bounding box.", styles['TableCell']),
            Paragraph("Real-time Euler angle trigonometric correction via ADXL345 tilt angles: d_true = d_meas &middot; cos(&theta;_tilt).", styles['TableCell'])
        ],
        [
            Paragraph("<b>Indoor Aerodynamic Drift &amp; GPS Loss:</b> Inability to fly safely in narrow indoor corridors.", styles['TableCell']),
            Paragraph("Risk of drone collision and discontinuous coordinate tracking.", styles['TableCell']),
            Paragraph("<b>Dual-Platform Contingency:</b> Mount identical embedded sensing rig on 4WD smart car rover with optical wheel encoders for safe ground scanning.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Optical Blind Zone (&lt;20 cm):</b> TF-Luna lens parallax causes inaccurate readings at close range.", styles['TableCell']),
            Paragraph("Erroneous near-zero measurements when approaching structural surface.", styles['TableCell']),
            Paragraph("Firmware automated blind-zone warning + software standoff boundary control holding platform at a safe 1.0 m distance.", styles['TableCell'])
        ]
    ]
    risk_table = Table(risks_data, colWidths=[140, 130, 217])
    risk_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('BOX', (0,0), (-1,-1), 0.75, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_WHITE, C_LIGHT_BG]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(KeepTogether([risk_table]))

    # ==================================================================================
    # SECTION 10: EXPECTED OUTCOMES & ITEMISED PROJECT BUDGET (BILL OF MATERIALS)
    # ==================================================================================
    story.append(Paragraph("10. Expected Outcomes &amp; Comprehensive Project Budget (Bill of Materials)", styles['SecH1']))
    story.append(Paragraph(
        "<b>Intended Final Deliverables:</b> (1) A flight-tested aerial payload and ground rover capable of millimeter-accurate facade ranging; (2) An autonomous coordinate transformation pipeline tracking displacement from initial (0,0,0) datum; (3) A 3D WebGL digital twin platform classifying planar walls, furniture bulges, and door recesses; and (4) An automated CSV/PLY/OBJ export suite for civil structural inspection reporting.",
        styles['BodyDark']
    ))
    story.append(Paragraph("<b>Itemized Project Hardware Budget &amp; Component Sourcing Breakdown:</b>", styles['SecH2']))

    budget_rows = [
        [
            Paragraph("S.No", styles['TableHead']),
            Paragraph("Hardware Component / Module", styles['TableHead']),
            Paragraph("Technical Specifications / Purpose", styles['TableHead']),
            Paragraph("Qty", styles['TableHead']),
            Paragraph("Unit (₹)", styles['TableHead']),
            Paragraph("Total (₹)", styles['TableHead']),
            Paragraph("Procurement Status", styles['TableHead'])
        ],
        [
            Paragraph("1", styles['TableCellCenter']),
            Paragraph("<b>Benewake TF-Luna LiDAR</b>", styles['TableCellBold']),
            Paragraph("850nm NIR ToF Rangefinder, 0.2–8m, 100Hz, UART", styles['TableCell']),
            Paragraph("1", styles['TableCellCenter']),
            Paragraph("2,200", styles['TableCellCenter']),
            Paragraph("2,200", styles['TableCellCenter']),
            Paragraph("<font color='#059669'><b>Procured / Working</b></font>", styles['TableCellCenter'])
        ],
        [
            Paragraph("2", styles['TableCellCenter']),
            Paragraph("<b>ESP32-WROOM-32 MCU</b>", styles['TableCellBold']),
            Paragraph("Dual-core 240MHz, 4MB Flash, Hardware UART, Wi-Fi/BLE", styles['TableCell']),
            Paragraph("2", styles['TableCellCenter']),
            Paragraph("450", styles['TableCellCenter']),
            Paragraph("900", styles['TableCellCenter']),
            Paragraph("<font color='#059669'><b>Procured / Working</b></font>", styles['TableCellCenter'])
        ],
        [
            Paragraph("3", styles['TableCellCenter']),
            Paragraph("<b>2D 360° Scanning LiDAR</b>", styles['TableCellBold']),
            Paragraph("YDLIDAR X4 / LD06 / RPLiDAR A1 (360° sweep, 3–5k pts/s)", styles['TableCell']),
            Paragraph("1", styles['TableCellCenter']),
            Paragraph("7,800", styles['TableCellCenter']),
            Paragraph("7,800", styles['TableCellCenter']),
            Paragraph("<font color='#D97706'><b>To Procure (Phase 2)</b></font>", styles['TableCellCenter'])
        ],
        [
            Paragraph("4", styles['TableCellCenter']),
            Paragraph("<b>ADXL345 Tilt &amp; Vibration Sensor</b>", styles['TableCellBold']),
            Paragraph("3-Axis Digital Accelerometer, &plusmn;16g, I2C/SPI, 13-bit", styles['TableCell']),
            Paragraph("1", styles['TableCellCenter']),
            Paragraph("250", styles['TableCellCenter']),
            Paragraph("250", styles['TableCellCenter']),
            Paragraph("<font color='#059669'><b>Procured / In Testing</b></font>", styles['TableCellCenter'])
        ],
        [
            Paragraph("5", styles['TableCellCenter']),
            Paragraph("<b>Carbon Fiber Drone Frame</b>", styles['TableCellBold']),
            Paragraph("220–250mm FPV quadcopter airframe, 3K carbon fiber", styles['TableCell']),
            Paragraph("1", styles['TableCellCenter']),
            Paragraph("2,200", styles['TableCellCenter']),
            Paragraph("2,200", styles['TableCellCenter']),
            Paragraph("<font color='#059669'><b>Procured / Assembled</b></font>", styles['TableCellCenter'])
        ],
        [
            Paragraph("6", styles['TableCellCenter']),
            Paragraph("<b>Brushless Drone Motors &amp; ESC</b>", styles['TableCellBold']),
            Paragraph("4x 2205 2300KV motors + 4-in-1 30A BLHeli_S ESC", styles['TableCell']),
            Paragraph("1 set", styles['TableCellCenter']),
            Paragraph("4,500", styles['TableCellCenter']),
            Paragraph("4,500", styles['TableCellCenter']),
            Paragraph("<font color='#059669'><b>Procured / Mounted</b></font>", styles['TableCellCenter'])
        ],
        [
            Paragraph("7", styles['TableCellCenter']),
            Paragraph("<b>Flight Controller Module</b>", styles['TableCellBold']),
            Paragraph("F4 V3S Plus with Betaflight / iNav, OSD, Barometer", styles['TableCell']),
            Paragraph("1", styles['TableCellCenter']),
            Paragraph("3,200", styles['TableCellCenter']),
            Paragraph("3,200", styles['TableCellCenter']),
            Paragraph("<font color='#D97706'><b>To Procure (Phase 4)</b></font>", styles['TableCellCenter'])
        ],
        [
            Paragraph("8", styles['TableCellCenter']),
            Paragraph("<b>High-Capacity LiPo Battery</b>", styles['TableCellBold']),
            Paragraph("3S / 4S 1500–2200mAh 75C High-discharge LiPo pack", styles['TableCell']),
            Paragraph("1", styles['TableCellCenter']),
            Paragraph("1,800", styles['TableCellCenter']),
            Paragraph("1,800", styles['TableCellCenter']),
            Paragraph("<font color='#D97706'><b>To Procure (Phase 4)</b></font>", styles['TableCellCenter'])
        ],
        [
            Paragraph("9", styles['TableCellCenter']),
            Paragraph("<b>LiPo Balance Charger</b>", styles['TableCellBold']),
            Paragraph("iMAX B6 80W Digital Multi-chemistry balance charger", styles['TableCell']),
            Paragraph("1", styles['TableCellCenter']),
            Paragraph("1,400", styles['TableCellCenter']),
            Paragraph("1,400", styles['TableCellCenter']),
            Paragraph("<font color='#D97706'><b>To Procure (Phase 4)</b></font>", styles['TableCellCenter'])
        ],
        [
            Paragraph("10", styles['TableCellCenter']),
            Paragraph("<b>Smart Car Rover Chassis Kit</b>", styles['TableCellBold']),
            Paragraph("4WD robotic chassis + 4x geared DC motors + L298N driver", styles['TableCell']),
            Paragraph("1 set", styles['TableCellCenter']),
            Paragraph("1,600", styles['TableCellCenter']),
            Paragraph("1,600", styles['TableCellCenter']),
            Paragraph("<font color='#D97706'><b>To Procure (Fallback)</b></font>", styles['TableCellCenter'])
        ],
        [
            Paragraph("11", styles['TableCellCenter']),
            Paragraph("<b>Optical Wheel Speed Encoders</b>", styles['TableCellBold']),
            Paragraph("Dual optical slotted disc encoders for dead-reckoning odometry", styles['TableCell']),
            Paragraph("2", styles['TableCellCenter']),
            Paragraph("150", styles['TableCellCenter']),
            Paragraph("300", styles['TableCellCenter']),
            Paragraph("<font color='#D97706'><b>To Procure (Fallback)</b></font>", styles['TableCellCenter'])
        ],
        [
            Paragraph("12", styles['TableCellCenter']),
            Paragraph("<b>Silicone Dampers &amp; Hardware</b>", styles['TableCellBold']),
            Paragraph("Vibration-isolation rubber grommets, standoffs, wiring", styles['TableCell']),
            Paragraph("1 set", styles['TableCellCenter']),
            Paragraph("550", styles['TableCellCenter']),
            Paragraph("550", styles['TableCellCenter']),
            Paragraph("<font color='#059669'><b>Procured / Working</b></font>", styles['TableCellCenter'])
        ],
        [
            Paragraph("—", styles['TableCellCenter']),
            Paragraph("<b>TOTAL ESTIMATED PROJECT BUDGET:</b>", styles['TableCellBold']),
            Paragraph("Complete Dual-Subsystem Hardware (Drone + Rover + Sensing)", styles['TableCellBold']),
            Paragraph("—", styles['TableCellCenter']),
            Paragraph("—", styles['TableCellCenter']),
            Paragraph("<b>₹ 26,900</b>", styles['TableCellBold']),
            Paragraph("<b>Academic Allocation</b>", styles['TableCellCenter'])
        ]
    ]
    budget_table = Table(budget_rows, colWidths=[20, 115, 150, 25, 48, 55, 74])
    budget_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('BOX', (0,0), (-1,-1), 0.75, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [C_WHITE, C_LIGHT_BG]),
        ('BACKGROUND', (0,-1), (-1,-1), C_ALT_BG),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(KeepTogether([budget_table]))

    # ==================================================================================
    # SECTION 11: CONCLUSION
    # ==================================================================================
    story.append(Paragraph("11. Conclusion &amp; Immediate Next Steps", styles['SecH1']))
    story.append(Paragraph(
        "This progress report establishes the verified engineering milestones achieved to date across Review 1 through Review 3 for our Innovative Design Project (BACSE291). By integrating the Benewake TF-Luna 850nm ToF Micro-LiDAR with an ESP-32 microcontroller and a ground analytics DSP engine, we have demonstrated sub-centimeter linear calibration (y = 1.0228x + 3.20 cm, R² = 1.0000), 4-wall sequential digital twin reconstruction (9,969 vertices), and real-time classification of planar walls, Almari inward bulges, and Gate recesses.",
        styles['BodyDark']
    ))
    story.append(Paragraph(
        "<b>Immediate Next Steps:</b> (1) Complete ADXL345 tilt and vibration filter testing on the benchtop rig; (2) Implement the dynamic coordinate displacement model updating position vector (&Delta;X, &Delta;Y, &Delta;Z) from initial datum (0,0,0); (3) Procure the 2D 360° scanning LiDAR and battery components; and (4) Validate scanning precision on the embedded smart car rover before progressing to tethered quadcopter flight trials.",
        styles['BodyDark']
    ))

    # ==================================================================================
    # SECTION 12: ACADEMIC REFERENCES
    # ==================================================================================
    story.append(Paragraph("12. Academic References (Literature Base)", styles['SecH1']))
    refs = [
        "[1] S. Feroz and S. Abu Dabous, 'UAV-based remote sensing applications for bridge condition assessment,' Remote Sensing, vol. 13, no. 9, p. 1809, 2021. https://doi.org/10.3390/rs13091809",
        "[2] P. J. Sanchez-Cuevas et al., 'Robotic system for inspection by contact of bridge beams using UAVs,' Sensors, vol. 19, no. 2, p. 305, 2019. https://doi.org/10.3390/s19020305",
        "[3] S.-P. Kao et al., 'Bridge crack inspection efficiency of an unmanned aerial vehicle system with a laser ranging module,' Sensors, vol. 22, no. 12, p. 4469, 2022. https://doi.org/10.3390/s22124469",
        "[4] S. E. Park, S.-H. Eem, and H. Jeon, 'Concrete crack detection and quantification using deep learning and structured light,' Constr. Build. Mater., vol. 252, p. 119096, 2020.",
        "[5] T.-A. Teo and C.-C. Yang, 'Evaluating the accuracy and quality of an iPad Pro's built-in lidar for 3D indoor mapping,' Dev. Built Environ., vol. 14, p. 100169, 2023.",
        "[6] J. Fu et al., 'Design and experimental study on vibration reduction of an UAV Lidar using rubber material,' Actuators, vol. 11, no. 12, p. 345, 2022.",
        "[7] M. Abdulkarem et al., 'Wireless sensor network for structural health monitoring: A contemporary review of technologies, challenges, and future direction,' Struct. Health Monit., vol. 19, no. 3, pp. 693–735, 2020.",
        "[8] Benewake (Beijing) Co., Ltd., 'TF-Luna LiDAR Module Datasheet &amp; Operating Manual,' Benewake Technical Documentation, 2023.",
        "[9] M. Azimi, A. D. Eslamlou, and G. Pekcan, 'Data-driven structural health monitoring and damage detection through deep learning: State-of-the-art review,' Sensors, vol. 20, no. 10, p. 2778, 2020.",
        "[10] B. F. Spencer et al., 'Advances in artificial intelligence for structural health monitoring: A comprehensive review,' KSCE J. Civ. Eng., vol. 29, no. 3, p. 100203, 2025.",
        "[11] C.-Z. Dong and F. N. Catbas, 'A review of computer vision–based structural health monitoring at local and global levels,' Struct. Health Monit., vol. 20, no. 2, pp. 692–743, 2021.",
        "[12] J. Chen and Y. K. Cho, 'CrackEmbed: Point feature embedding for crack segmentation from disaster site point clouds with anomaly detection,' Adv. Eng. Informatics, vol. 52, p. 101550, 2022.",
        "[13] H. Zhang et al., 'Detection of RC spalling damage and quantification of its key properties from 3D point cloud,' KSCE J. Civ. Eng., vol. 26, pp. 2023–2035, 2022.",
        "[14] Z. Sun et al., 'Approach towards the development of digital twin for structural health monitoring of civil infrastructure: A comprehensive review,' Sensors, vol. 25, no. 1, p. 59, 2025.",
        "[15] F. Shahrivar et al., 'AI-based remaining useful life prediction for civil infrastructure: Methods, challenges, and future research directions,' Artif. Intell. Rev., vol. 59, p. 138, 2026."
    ]
    for r in refs:
        story.append(Paragraph(r, styles['BulletDark']))

    # Build PDF with NumberedCanvas
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF report: {filename}")

if __name__ == '__main__':
    generate_pdf()
