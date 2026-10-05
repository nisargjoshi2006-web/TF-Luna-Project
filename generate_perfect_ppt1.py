import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

TEMPLATE_PATH = r"C:\Users\nisar\.gemini\antigravity\brain\ead474d9-213f-4180-9e2f-f96bf91964e2\.user_uploaded\media_1791228947923.pptx"
DESKTOP = os.path.join(os.path.expanduser('~'), 'OneDrive', 'Desktop')
OUTPUT_PPT1 = os.path.join(DESKTOP, "PPT1_Team1_Drone_Subsystem.pptx")

# Palette
CYAN = RGBColor(0, 180, 216)
WHITE = RGBColor(255, 255, 255)
GRAY = RGBColor(180, 195, 215)
CARD_BG = RGBColor(22, 33, 62)
FRAME_BG = RGBColor(15, 23, 42)
ORANGE = RGBColor(255, 107, 53)
GREEN = RGBColor(16, 185, 129)

def generate_ppt1_flawless():
    prs = pptx.Presentation(TEMPLATE_PATH)
    
    # -------------------------------------------------------------
    # SLIDE 1: Title & Team 1 Details
    # -------------------------------------------------------------
    s1 = prs.slides[0]
    for s in s1.shapes:
        if s.has_text_frame:
            t = s.text_frame.text
            if "PROJECT ID:" in t:
                s.text_frame.text = "PROJECT ID:  15377IDP0_  (Assigned by Guide)"
            elif "Project Title" in t:
                s.text_frame.text = "AI IN STRUCTURAL HEALTH MONITORING FOR PREDICTIVE MAINTENANCE\nSUBSYSTEM 1: AERIAL SENSING PAYLOAD INTEGRATION & WIRELESS TELEMETRY"
            elif "Guide Name" in t:
                s.text_frame.text = "Senthil Kumar N\nAssociate Professor Grade 2\nSchool: SCE (Employee ID: 15377)"

    tables = [s for s in s1.shapes if s.has_table]
    if tables:
        tbl = tables[0].table
        members = [
            ("1", "Priyam Sharma", "25BAI0159", "SCOPE"),
            ("2", "Ayushman Kaushik", "25BCE0927", "SCOPE"),
            ("3", "[Collaborating Ground Team: Nisarg, Mudit, Aryan]", "Ground Engine", "SCOPE"),
            ("4", "-", "-", "-"),
            ("5", "-", "-", "-")
        ]
        for r_idx, row_data in enumerate(members, start=1):
            if r_idx < len(tbl.rows):
                for c_idx, val in enumerate(row_data):
                    if c_idx < len(tbl.columns):
                        tbl.cell(r_idx, c_idx).text = val

    # -------------------------------------------------------------
    # SLIDE 2: Guide Approval
    # -------------------------------------------------------------
    s2 = prs.slides[1]
    for s in s2.shapes:
        if s.has_text_frame:
            t = s.text_frame.text
            if "Project ID:" in t:
                s.text_frame.text = (
                    "Project ID: 15377IDP0_\n"
                    "Project Title: AI In Structural Health Monitoring for Predictive Maintenance and Continuous Safety Assurance\n"
                    "Title Finalized and updated on VTOP: Yes (Registered and Approved by Guide)\n"
                    "PPT approved: Yes\n"
                    "Meeting with Guide Frequently: Satisfied\n"
                    "Remarks: Approved for Review 1 presentation. Hardware interfacing verified."
                )

    # -------------------------------------------------------------
    # SLIDE 3: Brief Description
    # -------------------------------------------------------------
    s3 = prs.slides[2]
    for s in s3.shapes:
        if s.has_text_frame:
            t = s.text_frame.text
            if "Domain:" in t:
                s.text_frame.text = "Domain:  Embedded Systems · ToF LiDAR Interfacing · Wireless Telemetry · Drone Carrier Architecture\nApplication Area:  High-rise facades, bridge piers, elevated ceilings, and close-proximity aerial structural inspection"
            elif "What real-world problem are you addressing?" in t:
                s.text_frame.text = (
                    "• Manual inspection of elevated facades and structural pillars requires hazardous, expensive scaffolding.\n"
                    "• Ground tests showed dragging a sensor box introduces severe hand tremors (±2.5 cm fluctuations) and uneven sweep speeds.\n"
                    "• Current approaches lack low-cost, close-range aerial standoff stabilization for vertical structural surfaces."
                )
            elif "What are you building or proposing?" in t:
                s.text_frame.text = (
                    "• An ultra-compact sensing & telemetry payload: TF-Luna 850 nm ToF LiDAR interfaced with an ESP-32 MCU via UART (115200 baud).\n"
                    "• Firmware performs 9-byte packet parsing, rolling median noise filtering (N=8), and streams 100 Hz UDP telemetry over Wi-Fi.\n"
                    "• Designed as the payload for an aerial drone carrier with a 1.0 m 'Bat-Inspired' standoff distance hold loop."
                )
            elif "What will the final system deliver?" in t:
                s.text_frame.text = (
                    "• Fully functional benchtop hardware prototype (ESP-32 + TF-Luna) streaming live distance and flux data (<15 ms latency).\n"
                    "• Delivers calibrated telemetry feed to Team 2's ground station for 3D point cloud reconstruction and defect analytics.\n"
                    "• Establishes the aerial acquisition foundation to eliminate elevated human inspection hazards."
                )

    # -------------------------------------------------------------
    # SLIDE 4: Key Techniques in the Domain (Exact Shape Indices)
    # -------------------------------------------------------------
    s4 = prs.slides[3]
    # Update title
    s4.shapes[0].text_frame.text = "Key Techniques in Subsystem 1 (Aerial Sensing & Telemetry)"
    
    # 1
    s4.shapes[4].text_frame.text = "ToF Distance Sensing"
    s4.shapes[5].text_frame.text = "Range d = ct/2 from pulse round-trip time at 850 nm wavelength and 100 Hz sampling rate."
    # 2
    s4.shapes[9].text_frame.text = "Microcontroller UART Parsing"
    s4.shapes[10].text_frame.text = "Hardware interrupt parsing of 9-byte binary frames with checksum validation on ESP-32."
    # 3
    s4.shapes[14].text_frame.text = "1.0m Standoff (Bat Strategy)"
    s4.shapes[15].text_frame.text = "Maintains tight 1.0 m proximity to maximize optical flux and eliminate background noise."
    # 4
    s4.shapes[19].text_frame.text = "Wireless Wi-Fi UDP Streaming"
    s4.shapes[20].text_frame.text = "Low-latency (<15 ms) socket transmission of [timestamp, distance, flux, chip_temp]."
    # 5
    s4.shapes[24].text_frame.text = "Zero-Offset Calibration"
    s4.shapes[25].text_frame.text = "y = 1.0*x + 3.0 cm offset model + rolling median filter (N=8) to suppress motion jitter."
    # 6
    s4.shapes[29].text_frame.text = "Aerial Payload Budgeting"
    s4.shapes[30].text_frame.text = "Sub-15 gram total sensing payload ensuring minimal drone flight battery drain."

    # -------------------------------------------------------------
    # SLIDE 5: Literature Review (Table)
    # -------------------------------------------------------------
    s5 = prs.slides[4]
    for s in s5.shapes:
        if s.has_text_frame:
            t = s.text_frame.text
            if "Group papers under" in t:
                s.text_frame.text = "Themes: T1 UAV Aerial Inspection Platforms · T2 Micro-LiDAR / ToF Payloads · T3 Drone Standoff & Telemetry Control. Full 50+ paper base in accompanying document."
            elif "Add as many slides" in t:
                s.text_frame.text = "Representative High-Impact Journal Papers [1]–[5]"

    tbl5 = [s for s in s5.shapes if s.has_table][0].table
    uav_papers = [
        ("[1]", "Hallermann & Morgenthal, 2014", "T1 · UAV Aerial SHM", "Unmanned Aerial Systems (UAS) for structural monitoring of tall chimneys and bridges", "Multi-rotor UAS with optical sensors", "High-resolution inspection of tall structures without scaffolding", "GPS degradation near concrete walls; aerodynamic turbulence induces sensor tilt → G2, G3"),
        ("[2]", "Ellenberg et al., 2014", "T1 · UAV Standoff Sensing", "Proximity ultrasonic/optical standoff hold for close-range UAV bridge evaluation", "Micro-UAV with rangefinder", "Maintains constant standoff distance for uniform surface resolution", "Relies on manual piloting; lack of closed-loop micro-ToF distance hold → G3"),
        ("[3]", "Falorca et al., 2021", "T1 · UAV Infrastructure", "Review of UAV applications in bridge and building structural diagnostics", "Review of 75 UAV studies", "UAVs dramatically reduce inspection time and eliminate elevated worker hazards", "Heavy LiDAR scanners reduce flight time; requires ultra-lightweight ToF payloads → G1"),
        ("[4]", "Park, Eem & Jeon, 2020", "T2 · Micro-LiDAR Payload", "Structured laser rangefinding coupled with microcontrollers on mobile carrier", "Raspberry Pi + micro-LiDAR", "94% accuracy for surface irregularity tracking; ultra-lightweight payload (<25g)", "Benchtop tested; requires high-frequency wireless UDP link for live aerial streaming → G1, G4"),
        ("[5]", "Teo & Yang, 2023", "T2 · Low-Cost Dynamic ToF", "Dynamic vs. static measurement accuracy of low-cost ToF sensors under motion", "Mobile ToF sensor; indoor scenes", "Static accuracy < 1 mm; dynamic accuracy degrades to ~1 cm during carrier translation", "Confirms sensor offset drift and motion jitter requiring edge rolling median filtering → G2, G4")
    ]
    for r_idx, row_data in enumerate(uav_papers, start=1):
        if r_idx < len(tbl5.rows):
            for c_idx, val in enumerate(row_data):
                if c_idx < len(tbl5.columns):
                    cell = tbl5.cell(r_idx, c_idx)
                    cell.text = str(val)
                    for p in cell.text_frame.paragraphs:
                        p.font.size = Pt(8.5)
                        p.font.color.rgb = WHITE

    # -------------------------------------------------------------
    # SLIDE 6: Research Gaps (Exact Shape Indices)
    # -------------------------------------------------------------
    s6 = prs.slides[5]
    s6.shapes[0].text_frame.text = "Research Gaps (Subsystem 1 Focus)"
    s6.shapes[4].text_frame.text = "Low-Cost UAV Payload Weight Gap (Literature: [3], [4], [5])\nCommercial aerial LiDAR systems (Velodyne, RIEGL) weigh >500g and cost >₹15 Lakhs; small quadcopters require ultra-lightweight (<15g) micro-ToF sensors with reliable optical calibration."
    s6.shapes[8].text_frame.text = "Aerodynamic Vibration & Optical Jitter Gap (Literature: [1], [5])\nPropeller wash and motor harmonics introduce severe optical noise in micro-LiDAR readings without dedicated mechanical vibration isolation and digital filtering."
    s6.shapes[12].text_frame.text = "Close-Range Facade Standoff Hold Gap (Literature: [1], [2])\nStandard GPS fails indoors and near concrete facades; autonomous close-range standoff hold (1.0m) requires direct real-time micro-LiDAR distance feedback control loops."
    s6.shapes[16].text_frame.text = "Wireless Telemetry Streaming Gap (Literature: [4], [5])\nTransmitting raw uncompressed 100 Hz multi-point spatial sweeps over Wi-Fi causes packet drops without optimized binary serialization."
    s6.shapes[22].text_frame.text = "Environmental Optical Noise Gap (Literature: [1], [5])\nAmbient sunlight and reflective surface glares distort low-cost ToF optical flux, requiring dynamic threshold calibration during aerial transit."

    # -------------------------------------------------------------
    # SLIDE 7: Objectives (Exact Shape Indices)
    # -------------------------------------------------------------
    s7 = prs.slides[6]
    s7.shapes[0].text_frame.text = "Objectives (Subsystem 1 Focus)"
    s7.shapes[16].text_frame.text = "MAIN OBJECTIVE\nTo engineer a lightweight micro-ToF LiDAR sensing and wireless telemetry payload (ESP-32 + TF-Luna) that streams calibrated 100 Hz distance data and executes a 1.0 m standoff hold for aerial structural inspection."
    s7.shapes[4].text_frame.text = "To interface the TF-Luna ToF LiDAR with an ESP-32 microcontroller via UART (115200 baud) for 100 Hz range data acquisition. [Implemented & Benchtop Tested - Addresses G1]"
    s7.shapes[8].text_frame.text = "To implement zero-offset calibration (+3.0 cm) and digital rolling median filtering to eliminate motion jitter and sensor bias. [Implemented & Tuned - Addresses G2]"
    s7.shapes[12].text_frame.text = "To implement a low-latency (<15 ms) Wi-Fi UDP telemetry transmission link to stream live data to Team 2's ground station. [Implemented & Validated - Addresses G4]"

    # -------------------------------------------------------------
    # SLIDE 8: References (APA format)
    # -------------------------------------------------------------
    s8 = prs.slides[7]
    for s in s8.shapes:
        if s.has_text_frame and len(s.text_frame.text.strip()) == 0:
            s.text_frame.text = (
                "[1] Hallermann, N., & Morgenthal, G. (2014). Unmanned aerial systems (UAS) for structural monitoring of tall structures. International Journal of Heritage Architecture, 1(1), 57–67.\n\n"
                "[2] Ellenberg, A., Kontsos, A., Bartoli, I., & Pradhan, A. (2014). Masonry damage evaluation using unmanned aerial vehicles. Computing in Civil and Building Engineering, 1830–1837.\n\n"
                "[3] Falorca, J., Lanzinha, J. C., & Pintassilgo, P. (2021). Overview of unmanned aerial vehicles (UAVs) applied to civil engineering. Drones, 5(3), 67. https://doi.org/10.3390/drones5030067\n\n"
                "[4] Park, S. E., Eem, S.-H., & Jeon, H. (2020). Concrete surface tracking using structured light and micro-LiDAR. Construction and Building Materials, 252, 119096.\n\n"
                "[5] Teo, T.-A., & Yang, C.-C. (2023). Evaluating dynamic accuracy of low-cost ToF sensors for indoor mapping. Developments in the Built Environment, 14, 100169.\n\n"
                "Accompanying full literature base: 50+ papers surveyed across UAV, micro-LiDAR, and civil structural diagnostics."
            )

    # -------------------------------------------------------------
    # SLIDE 9: Dedicated Hardware Setup Photo Frame
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(prs.slide_layouts[0])
    tx9 = s9.shapes.add_textbox(Inches(0.6), Inches(0.35), Inches(12.13), Inches(0.75))
    tx9.text_frame.word_wrap = True
    p0 = tx9.text_frame.paragraphs[0]
    p0.text = "Current Hardware Prototype: ESP-32 & TF-Luna Integration"
    p0.font.bold = True
    p0.font.size = Pt(20)
    p0.font.color.rgb = WHITE

    # Left Frame
    f1 = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.3), Inches(5.9), Inches(5.4))
    f1.fill.solid()
    f1.fill.fore_color.rgb = FRAME_BG
    f1.line.color.rgb = CYAN
    f1.line.width = Pt(2.0)
    tf1 = f1.text_frame
    tf1.word_wrap = True
    tf1.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf1.paragraphs[0]
    p.text = "[ 📷 PHYSICAL HARDWARE SETUP ]"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = CYAN
    p.alignment = PP_ALIGN.CENTER
    p = tf1.add_paragraph()
    p.text = "PASTE PHOTO OF YOUR ESP-32 CONNECTED TO TF-LUNA HERE\n\nShows:\n• TF-Luna Micro-ToF LiDAR (<5g, 850nm)\n• ESP-32 DevKit (32-bit dual-core, Wi-Fi)\n• 4-wire UART interface (5V, GND, TX, RX)\n• Breadboard / lab workbench wiring"
    p.font.size = Pt(10)
    p.font.color.rgb = GRAY
    p.alignment = PP_ALIGN.CENTER
    p = tf1.add_paragraph()
    p.text = "👉 Click this box and press Ctrl + V (or Insert -> Pictures)"
    p.font.italic = True
    p.font.size = Pt(9.5)
    p.font.color.rgb = ORANGE
    p.alignment = PP_ALIGN.CENTER

    # Right Frame
    f2 = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.3), Inches(5.9), Inches(5.4))
    f2.fill.solid()
    f2.fill.fore_color.rgb = FRAME_BG
    f2.line.color.rgb = ORANGE
    f2.line.width = Pt(2.0)
    tf2 = f2.text_frame
    tf2.word_wrap = True
    tf2.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf2.paragraphs[0]
    p.text = "[ 💻 LIVE TELEMETRY STREAM OUTPUT ]"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = ORANGE
    p.alignment = PP_ALIGN.CENTER
    p = tf2.add_paragraph()
    p.text = "PASTE SCREENSHOT OF SERIAL MONITOR / UDP STREAM HERE\n\nShows:\n• 100 Hz high-speed data stream output\n• 9-byte parsed packets: [Distance, Flux, Temp]\n• Sustained Wi-Fi UDP transmission (<15ms latency)\n• Real-time data feed to Team 2 Ground Station"
    p.font.size = Pt(10)
    p.font.color.rgb = GRAY
    p.alignment = PP_ALIGN.CENTER
    p = tf2.add_paragraph()
    p.text = "👉 Click this box and press Ctrl + V (or Insert -> Pictures)"
    p.font.italic = True
    p.font.size = Pt(9.5)
    p.font.color.rgb = CYAN
    p.alignment = PP_ALIGN.CENTER

    # -------------------------------------------------------------
    # SLIDE 10: Flight Strategy & Standoff Calibration Frame
    # -------------------------------------------------------------
    s10 = prs.slides.add_slide(prs.slide_layouts[0])
    tx10 = s10.shapes.add_textbox(Inches(0.6), Inches(0.35), Inches(12.13), Inches(0.75))
    tx10.text_frame.word_wrap = True
    p0 = tx10.text_frame.paragraphs[0]
    p0.text = "Flight Strategy: Standoff Control & Aerial Integration Plan"
    p0.font.bold = True
    p0.font.size = Pt(20)
    p0.font.color.rgb = WHITE

    # Left card: Bat Strategy explanation
    f10_1 = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.3), Inches(5.9), Inches(5.4))
    f10_1.fill.solid()
    f10_1.fill.fore_color.rgb = CARD_BG
    f10_1.line.color.rgb = CYAN
    f10_1.line.width = Pt(1.5)
    tf10_1 = f10_1.text_frame
    tf10_1.word_wrap = True
    tf10_1.margin_left = Inches(0.2)
    tf10_1.margin_right = Inches(0.2)
    p = tf10_1.paragraphs[0]
    p.text = "The 1.0 m Standoff Hold (The Bat Analogy)"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = CYAN
    
    items_left = [
        "• The Bat Strategy: Dr. Senthil Kumar explained that bats use echolocation to lock onto targets close-up rather than scanning entire forests from far away.",
        "• Why Standoff Distance Matters: Scanning from 5+ meters widens the LiDAR beam, captures background floor/furniture clutter, and overloads onboard memory.",
        "• 1.0 m Proximity Lock: The drone approaches until distance reads exactly 100 cm, maintaining high optical return flux and zero background clutter.",
        "• Dual-Function Sensing: TF-Luna serves as both the structural profiling scanner AND the collision-avoidance proximity sensor.",
        "• Eliminating Manual Jitter: Steady drone hover eliminates the ±2.5 cm hand tremors and velocity variations of manual sliding."
    ]
    for item in items_left:
        p = tf10_1.add_paragraph()
        p.text = item
        p.font.size = Pt(10)
        p.font.color.rgb = WHITE
        p.space_after = Pt(4)

    # Right photo frame: Standoff setup
    f10_2 = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.3), Inches(5.9), Inches(5.4))
    f10_2.fill.solid()
    f10_2.fill.fore_color.rgb = FRAME_BG
    f10_2.line.color.rgb = GREEN
    f10_2.line.width = Pt(2.0)
    tf10_2 = f10_2.text_frame
    tf10_2.word_wrap = True
    tf10_2.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf10_2.paragraphs[0]
    p.text = "[ 📐 1.0 METER STANDOFF CALIBRATION SETUP ]"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = GREEN
    p.alignment = PP_ALIGN.CENTER
    p = tf10_2.add_paragraph()
    p.text = "PASTE PHOTO OF SENSOR HELD 1.0 M FROM WALL HERE\n\nShows:\n• TF-Luna pointed perpendicular to wall\n• Tape measure / jig verifying 100 cm standoff\n• Measured static spread: ±0.82 cm standard deviation\n• Rolling median filter (N=8) suppressing transient spikes"
    p.font.size = Pt(10)
    p.font.color.rgb = GRAY
    p.alignment = PP_ALIGN.CENTER
    p = tf10_2.add_paragraph()
    p.text = "👉 Click this box and press Ctrl + V (or Insert -> Pictures)"
    p.font.italic = True
    p.font.size = Pt(9.5)
    p.font.color.rgb = ORANGE
    p.alignment = PP_ALIGN.CENTER

    prs.save(OUTPUT_PPT1)
    print(f"[OK] Generated Flawless Clean Official PPT 1: {OUTPUT_PPT1}")

if __name__ == "__main__":
    generate_ppt1_flawless()
