# AI-Driven Robotic Structural Health Monitoring (SHM) System

## Project Overview
An autonomous, low-cost robotic infrastructure inspection and predictive maintenance framework using **TF-Luna Time-of-Flight (ToF) LiDAR**, **Mathematical Calibration ($y = mx + c$)**, and **3D Point Cloud (.PLY) Spatial Reconstruction**.

---

## System Architecture & Features

### 1. Embedded LiDAR Telemetry
- **Sensor:** TF-Luna Time-of-Flight LiDAR ($850\text{ nm}$ infrared, $100\text{ Hz}$ update rate).
- **Microcontroller:** Arduino Uno R3.
- **Protocol:** High-speed `SoftwareSerial` on Pins 2 (RX) and 3 (TX) at 115200 baud with 9-byte packet checksum validation.

### 2. Scientific Calibration & DSP Pipeline
- **Zero-Offset & Regression Calibration:** Corrects physical optical casing delays ($\Delta d = +3.00\text{ cm}$) using linear regression models ($y = mx + c$) with $R^2 \ge 0.999$.
- **Digital Signal Processing (DSP):** Rolling Window Median Filter eliminates ambient optical noise and sub-centimeter laser jitter without phase lag.

### 3. 3D Point Cloud (.PLY) Generation
- Converts 1D distance $r$ and angular trajectories $(\theta, \phi)$ into 3D Cartesian coordinates:
  $$X = r \cos\phi \cos\theta, \quad Y = r \sin\phi, \quad Z = r \cos\phi \sin\theta$$
- Exports industry-standard `.ply` point cloud files compatible with Blender, MeshLab, Open3D, and ROS.

### 4. Interactive Web Dashboard (Streamlit & Three.js)
- **Tab 1: Live Monitor:** Real-time distance readout, error delta badge, and scrolling time-series graph.
- **Tab 2: Calibration Report:** Plotted regression curve, empirical benchmark points, and precision statistics.
- **Tab 3: PLY·FORGE 3D Suite:** Three.js WebGL interactive 3D point cloud & mesh viewer with 360° rotation, zoom, point sizing, and `.ply` importing.

---

## Structural Health Monitoring (SHM) Applications
1. **Depth Anomaly Detection:** Detects spalling, missing bricks, and cavities $>2\text{ cm}$ deep via step-change point cloud analysis.
2. **Structural Deformation Tracking:** Identifies wall tilting, bulging, and sagging over time for predictive maintenance.
3. **Autonomous Drone Stand-Off Safety:** Acts as a real-time Rangefinder in the flight control loop to maintain a safe $1.50\text{ m}$ standoff boundary.
4. **Sensor Fusion for Crack Inspection:** Provides $(X, Y, Z)$ spatial references for RGB camera crack segmentation algorithms.

---

## Directory Structure
```
TF_LUNA_PROJECT/
├── arduino/
│   ├── tf_luna_code.ino          # Arduino Uno sensor-only firmware
│   └── scanner.ino               # Dual-servo scanning firmware
├── data/
│   ├── calibration.json          # Verified calibration model & parameters
│   └── distance_data.csv         # Real-time calibrated measurement logs
├── data_collection/
│   ├── calibrate.py              # Automated zero-offset & linear regression tool
│   ├── serial_reader.py          # Calibrated reader with median filtering
│   └── export_ply.py             # 3D spatial coordinate & .PLY exporter
├── dashboard/
│   ├── app.py                    # Multi-tab Streamlit dashboard
│   └── templates/
│       └── ply_forge.html        # Three.js WebGL 3D Point Cloud viewer
└── README.md                     # Project documentation
```

---

## Getting Started

### 1. Calibrate Sensor
```bash
python data_collection/calibrate.py
```

### 2. Run Live Calibrated Logger
```bash
python data_collection/serial_reader.py
```

### 3. Launch Dashboard
```bash
streamlit run dashboard/app.py
```

### 4. Export 3D Point Cloud Scan
```bash
python data_collection/export_ply.py
```
