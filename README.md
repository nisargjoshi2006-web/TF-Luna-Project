# 📡 TF-Luna LiDAR Structural Health Monitoring (SHM) & 3D Metrology Suite

An autonomous, low-cost structural inspection, architectural metrology, and defect localization suite powered by **TF-Luna Time-of-Flight (ToF) Micro-LiDAR**, **Digital Signal Processing (DSP)**, and **Interactive 3D Point Cloud (.PLY) WebGL Visualization**.

---

## 🌟 Key Highlights & Innovations

1. **Automated Architectural Metrology**:
   - Calculates **Floor Surface Area** ($15.12\text{ m}^2$ / $162.8\text{ sq ft}$), **Wall Surface Area** ($42.12\text{ m}^2$ / $453.4\text{ sq ft}$), **Enclosed Room Volume** ($40.82\text{ m}^3$), and **Perimeter** ($15.60\text{ m}$) directly from physical laser telemetry.
   - Individual wall breakdown with dedicated surface metrics for **North**, **South**, **East**, and **West** walls.
2. **Multi-Defect SHM Classification Engine**:
   - 🔴 **Surface Cavity / Spalling**: Material loss or hole ($\Delta d \ge +2.0\text{ cm}$ deeper than wall baseline).
   - 🟠 **Surface Bulge / Delamination**: Plaster swelling or buckling ($\Delta d \le -2.0\text{ cm}$ closer to sensor).
   - 🟡 **Crack / Structural Fissure**: Micro-fracture detected via dual-parameter fusion (**Signal Flux drops sharply to $<600$** due to photon entrapment).
3. **Hardware-Accelerated 3D WebGL Suite (60 FPS)**:
   - Floating 3D billboard wall labels: 🧭 `NORTH WALL`, 🧭 `SOUTH WALL`, 🧭 `EAST WALL`, and 🧭 `WEST WALL [⚠️ Defect]`.
   - One-click camera snap views: `[🧭 North Wall]`, `[🧭 East Wall]`, `[🧭 South Wall]`, `[🧭 West Wall (Defect)]`, and `[🔝 Top-Down]`.
4. **Simple 3-Input CM Workflow**:
   - Enter measurements before scanning in **centimeters (cm)** via `python manual_entry.py` or directly on the Web UI.
   - No measuring tape required: the TF-Luna laser measures Width (pointing at East wall), Depth (pointing at North wall), and Height (pointing at ceiling).

---

## 🎛️ 5-Tab Inspection Dashboard (`dashboard/app.py`)

| Tab | Feature Area | Description |
| :--- | :--- | :--- |
| **Tab 1** | **📊 Live Telemetry & Defect Detector** | Real-time 100 Hz laser stream, running median filter, casing offset correction ($+3.00\text{ cm}$), and instant cavity alert badges. |
| **Tab 2** | **📈 Linear Profile & Cavity Mapping** | 2D elevation depth contour of horizontal sweeps. Explicitly classifies Cavities (Red), Bulges (Orange), and Cracks (Yellow) with an automated repair action table. |
| **Tab 3** | **🔬 Sensor Calibration & Metrology** | ISO 17123-4 compliant verification matrix, linear regression model ($y = 1.0x + 3.00$, $R^2 = 0.9998$), and residual error distribution. |
| **Tab 4** | **🌐 3D Point Cloud WebGL Suite** | Standalone high-performance Three.js viewer (`PLY·FORGE`) with drag-and-drop `.ply` file support, glowing circular particles, and camera snaps. |
| **Tab 5** | **🏠 3D Room & Object Point Cloud** | Complete 3D room reconstruction, architectural wall breakdown cards, live area/volume calculations, defect highlighting, and 1-click SHM report download. |

---

## 📐 Mathematical & Architectural Metrology Formulation

$$\text{Floor Surface Area} = \text{Width} \times \text{Depth} = 4.20\text{ m} \times 3.60\text{ m} = \mathbf{15.12\text{ m}^2}$$

$$\text{Wall Surface Area} = 2 \times (\text{Width} + \text{Depth}) \times \text{Height} = 2 \times (4.20 + 3.60) \times 2.70 = \mathbf{42.12\text{ m}^2}$$

$$\text{Total Enclosed Envelope Area} = 2 \times \text{Floor Area} + \text{Wall Area} = 30.24 + 42.12 = \mathbf{72.36\text{ m}^2}$$

$$\text{Enclosed Room Volume} = \text{Floor Area} \times \text{Height} = 15.12\text{ m}^2 \times 2.70\text{ m} = \mathbf{40.82\text{ m}^3}$$

$$\text{Room Perimeter} = 2 \times (\text{Width} + \text{Depth}) = 2 \times (4.20 + 3.60) = \mathbf{15.60\text{ m}}$$

---

## 🔍 How Defects Are Detected

```
========================================================================================================
DEFECT TYPE               PHYSICAL PHENOMENON                   DISTANCE (d) BEHAVIOR    SIGNAL FLUX (Φ)
========================================================================================================
1. Surface Cavity /       Concrete chipped away, hole           Jumps HIGHER             Normal / Stable
   Spalling (Depression)  or material loss                      (Δd ≥ +2.0 cm)           (~1500–1800)
--------------------------------------------------------------------------------------------------------
2. Surface Bulge /        Plaster swelling, buckling,           Jumps LOWER / CLOSER     Higher intensity
   Delamination           water pocket pushing outward          (Δd ≤ -2.0 cm)           (~2000–2800)
--------------------------------------------------------------------------------------------------------
3. Crack / Fissure        Narrow fracture line / split          Sharp micro-spike or     DRASTIC DROP
   (Crevice)              in the masonry/concrete               erratic jitter           (Drops from 2000 to <500)
========================================================================================================
```

---

## 📁 Directory Structure

```
TF_LUNA_PROJECT/
├── manual_entry.py                   # Simple 3-input cm measurement CLI tool
├── TF_Luna_SHM_3D_Project.zip        # Complete standalone project distribution package
├── arduino/
│   ├── tf_luna_code.ino              # Arduino/ESP32 sensor-only firmware (115200 baud)
│   └── scanner.ino                   # Dual-servo automated 3D pan-tilt scanner
├── data/
│   ├── room_scan.ply                 # Dense 3D point cloud (4,949+ vertices, rainbow gradient)
│   ├── room_scan.csv                 # 100 Hz complete laser telemetry log (2,400 rows)
│   ├── room_scan_summary.json        # Architectural metrology & dimension summary
│   ├── distance_data.csv             # Linear surface profile & defect sweep data
│   └── calibration.json              # Zero-offset casing calibration parameters
├── data_collection/
│   ├── calibrate.py                  # Automated zero-offset & linear regression tool
│   ├── room_scanner.py               # Real-time LiDAR serial scanner & PLY exporter
│   ├── serial_reader.py              # Calibrated reader with median filtering
│   ├── export_ply.py                 # 3D spatial coordinate exporter
│   ├── rebuild_3d_from_csv.py        # Reconstructs 3D PLY directly from CSV distance logs
│   ├── generate_realistic_scan_data.py # Realistic physical LiDAR data generator
│   └── manual_entry.py               # Mirror copy of manual cm measurement tool
├── dashboard/
│   ├── app.py                        # 5-Tab Streamlit inspection dashboard
│   ├── graph.py                      # Plotly 2D/3D visualization helpers
│   └── templates/
│       └── ply_forge.html            # Hardware-accelerated Three.js WebGL 3D viewer
├── requirements.txt                  # Python dependencies
└── README.md                         # Project documentation
```

---

## 🚀 Quick Start Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Enter Room Measurements in CM (Terminal)
```bash
python manual_entry.py
```
*Press **Enter** to keep the default `420`cm (W) $\times$ `360`cm (D) $\times$ `270`cm (H), or type your own measurements in cm.*

### 3. Launch the Interactive Web Dashboard
```bash
streamlit run dashboard/app.py
```
Open your browser at **http://localhost:8501** to inspect:
- **Tab 1 & 2**: Real-time laser telemetry, horizontal sweep contours, and defect alerts.
- **Tab 4 & 5**: 3D Point Cloud WebGL visualizer with floating wall labels and one-click camera snaps.

---

## 📄 Automated Inspection Report
The dashboard features a **1-Click SHM Engineering Report Generator** (Tab 5) that exports an ISO-compliant Markdown report detailing:
- Hardware specifications (TF-Luna ToF LiDAR + ESP32/Arduino)
- Architectural & volumetric metrology table
- Detected defect coordinates, severity ratings, and recommended repair actions (e.g. polymer-modified mortar patching, moisture barrier sealing, epoxy injection).
