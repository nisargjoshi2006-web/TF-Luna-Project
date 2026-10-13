# Project Technical Report (Revision Zero — R0)

**Project Title:** AI-Driven Robotic Structural Health Monitoring (SHM) & 3D LiDAR Metrology Suite  
**Document Identifier:** `TF_LUNA_PROJECT_DOCUMENT_R0`  
**Revision:** R0 (Baseline Architecture & Sensor Methodology)  
**Date:** October 2026  
**Department / Domain:** Robotics, IoT, Sensor Fusion & Structural Metrology  

---

## Executive Summary

This Revision Zero (R0) technical document outlines the design, mathematical framework, physical implementation, and architectural evolution of the **AI-Driven Robotic Structural Health Monitoring (SHM) and 3D LiDAR Metrology System**. 

The system automates civil infrastructure inspection and indoor architectural metrology by replacing hazardous, qualitative, and labor-intensive manual tape measurements with a lightweight, micro-LiDAR digital twin pipeline. The document details:
1. The **primary 1D ToF sensor currently implemented** (Benewake TF-Luna 850nm) and its empirical linear calibration model ($y = 1.0228x + 3.20\text{ cm}$, $R^2 = 1.0000$).
2. The **upcoming 2D 360° LiDAR sensor** planned for the next engineering phase to enable autonomous omnidirectional SLAM.
3. A rigorous trade-off and comparative metrology analysis between 1D and 2D LiDAR modalities.
4. The core architectural concept, digital twin pipeline, and feature classification (distinguishing normal flat walls from inward-bulging furniture/Almari and outward-recessing doors/Gate).
5. The **Dynamic Coordinate Frame & Translation Model** (origin tracking principle starting at initial datum $(0,0,0)$ and updating dynamically $(\Delta X, \Delta Y, \Delta Z)$ as the sensor is translated/dragged across space).

---

## 1. Problem Statement & Engineering Motivation

### 1.1 The Inspection Bottleneck
Civil infrastructure (buildings, retaining walls, bridges, precast elements) and indoor architectural layouts require continuous geometric verification and structural defect monitoring. Traditional inspection relies on:
* **Manual Tape Measures / Optical Distance Meters:** Slow, labor-intensive, subject to tape sagging/bending over long spans, and introduce human parallax errors ($\ge \pm 2\text{--}5\text{ cm}$).
* **Commercial Terrestrial Laser Scanners (TLS):** Millimeter-accurate but prohibitively expensive ($\$15,000\text{--}\$35,000$), bulky ($> 2\text{--}5\text{ kg}$), and unsuitable for lightweight drones or agile robotic payloads.
* **Pure Computer Vision / Photogrammetry:** Provides high-resolution visual texture for hairline surface cracks but completely lacks direct metric depth, failing in low-light, shadow-rich, or featureless uniform concrete/plaster walls.

### 1.2 The Proposed Solution
Our system bridges this gap through a high-frequency, low-cost micro-LiDAR digital twin pipeline:
* Acquires physical metric distance at up to $100\text{ Hz}$.
* Extrudes orthogonal 3D point cloud models ($4.8\text{ m} \times 4.8\text{ m}$ digital twins) with millimetric planar accuracy.
* Automatically identifies and segments architectural sub-elements (inward bulges such as wardrobes/Almari vs. outward recesses such as doors/Gate).
* Streams real-time telemetric point clouds to interactive WebGL/Three.js dashboards and BIM-compliant `.PLY` / `.OBJ` models.

---

## 2. Sensor Selection & Comparative Metrological Analysis

### 2.1 Current Sensor: Benewake TF-Luna 850nm ToF Micro-LiDAR
The currently deployed hardware utilizes the **Benewake TF-Luna Time-of-Flight (ToF) Micro-LiDAR module**, interfaced via Hardware UART to an ESP-32 microcontroller.

```
       ┌──────────────────────────────────────────────────────────┐
       │             TF-LUNA SENSOR OPTICAL SCHEMATIC             │
       │                                                          │
       │   [ 850nm VCSEL Laser ] ──Pulse──► ──► ──► ──► [ Wall ]  │
       │   [ Receiver Photodiode] ◄─Echo── ◄── ◄── ◄─── (Target)  │
       │                                                          │
       │   Distance (d) = (c * Δt) / 2                            │
       │   Calibration: y = 1.0228 * x + 3.20 cm                  │
       └──────────────────────────────────────────────────────────┘
```

#### Specifications:
* **Operating Principle:** Direct Time-of-Flight (dToF) pulsed infrared laser rangefinding:
  $$d = \frac{c \cdot \Delta t}{2}$$
  where $c = 3 \times 10^8\text{ m/s}$ is the speed of light and $\Delta t$ is the nanosecond-level round-trip flight time.
* **Laser Wavelength:** $850\text{ nm}$ Near-Infrared (NIR) Class 1 eye-safe VCSEL.
* **Operating Range:** $0.20\text{ m} \text{ to } 8.00\text{ m}$ ($\ge 90\%$ target reflectivity).
* **Sampling Rate:** Configurable from $1\text{ Hz} \text{ to } 250\text{ Hz}$ (paced at $60\text{--}65\text{ Hz}$ in firmware to eliminate USB buffer backlog).
* **Communication Interface:** UART (115200 Baud, 8-N-1) using a standard 9-byte packet protocol with checksum validation.
* **Optical Field of View (FoV):** $2.0^\circ$ narrow collimated beam spot.
* **Supply Voltage & Power:** $3.7\text{--}5.2\text{ V DC}$, current consumption $\le 70\text{ mA}$ ($< 0.35\text{ W}$).
* **Form Factor & Weight:** $35\text{ mm} \times 21.2\text{ mm} \times 13.5\text{ mm}$, mass $< 5\text{ grams}$.

#### Why the TF-Luna was Chosen for Phase 1:
1. **Ultra-Lightweight & Low Power:** Weighing under 5 grams and consuming under 350 mW, it can be mounted directly on micro-drones, pan-tilt servo gimbals, or handheld lightweight wand assemblies without destabilizing flight dynamics or draining batteries.
2. **High Update Rate (Up to 250 Hz):** Allows continuous dynamic sweeps across wall surfaces without skipping physical facets.
3. **Low Unit Cost ($<\$25):** Low-cost prototyping compared to multi-thousand-dollar commercial scanners.
4. **Hardware Constraints Solved via Software:**
   * *Blind Zone ($0\text{--}20\text{ cm}$):* Due to physical lens parallax between emitter and receiver, targets closer than 20 cm do not strike the photodiode focal spot. The system enforces an automated blind zone warning alert when $d < 20\text{ cm}$.
   * *Zero-Point Housing Offset ($+3.20\text{ cm}$):* Direct regression modeling on physical tape benchmarks eliminates housing delay.

#### Firmware Linear Calibration Model:
Raw integer distance exhibits an intrinsic optical casing offset of $+3.20\text{ cm}$ and a minor distance-scaling slope deviation. Through 2-point physical calibration against certified steel tape measures at $39.0\text{ cm}$ and $61.4\text{ cm}$, the exact linear regression model was derived:
$$y = 1.0228 \cdot x_{\text{raw}} + 3.20\text{ cm}$$
* Determination Coefficient: $R^2 = 1.0000$
* Root Mean Square Error: $\text{RMSE} = \pm 0.02\text{ cm}$ ($0.2\text{ mm}$ residual error)
* Sub-Centimeter Smoothing: 8-sample continuous ring-buffer oversampling executed on the ESP-32.

---

### 2.2 Upcoming Sensor: 2D 360° Planar LiDAR
For the next engineering phase (Revision 1 / Final Implementation), the system incorporates a **2D 360° Rotating Laser Range Scanner** (such as the RPLiDAR A1/A2 or LD06 / YDLidar series).

```
       ┌──────────────────────────────────────────────────────────┐
       │             2D 360° LIDAR SCANNING SCHEMATIC             │
       │                                                          │
       │                    North (0°)                            │
       │                        ▲                                 │
       │                        │                                 │
       │      West (270°) ◄─── ( ⟳ ) ───► East (90°)              │
       │                        │   360° Continuous               │
       │                        ▼   Spinning Head                 │
       │                    South (180°)                          │
       │                                                          │
       │   Point(i) = [ r * cos(θ),  r * sin(θ) ]                 │
       └──────────────────────────────────────────────────────────┘
```

#### Specifications:
* **Scanning Mechanism:** Brushless motor rotating a laser transceiver head at $5.5\text{ Hz} \text{ to } 12\text{ Hz}$ ($330\text{--}720\text{ RPM}$).
* **Field of View (FoV):** Full $360^\circ$ continuous omnidirectional planar coverage.
* **Ranging Distance:** $0.15\text{ m} \text{ to } 12.00\text{ m}$.
* **Sampling Frequency:** $2,000 \text{ to } 8,000 \text{ sample points per second}$.
* **Angular Resolution:** $0.5^\circ \text{ to } 1.0^\circ$ across the complete $360^\circ$ perimeter.
* **Data Protocol:** Cartesian $(X, Y)$ coordinate stream decomposed from Polar $(r_i, \theta_i)$ tuples:
  $$X_i = r_i \cdot \cos(\theta_i), \quad Z_i = r_i \cdot \sin(\theta_i)$$

#### Why Transition to 2D 360° LiDAR in Next Phase:
1. **Instant Omnidirectional Capture:** Instead of requiring manual left-to-right laser sweeping across 4 individual walls, a single 2D revolution captures the complete room perimeter profile in under $100\text{ ms}$.
2. **Elimination of Hand/Servo Angular Jitter:** Eliminates mechanical gear backlash and human sweeping non-uniformities.
3. **Simultaneous Localization and Mapping (SLAM):** Enables 2D SLAM algorithms (Hector SLAM, Cartographer, Gmapping) to autonomously register robot position and room geometry concurrently.
4. **Volumetric 3D Twin via Vertical Trajectory Extrusion:** By translating the 2D planar LiDAR vertically along the $Y$-axis (via drone altitude climb or linear lead screw), a dense, watertight 3D volumetric model is reconstructed automatically.

---

### 2.3 Comprehensive Metrology & Sensor Comparison Table

| Parameter / Feature | Current Sensor: TF-Luna (1D) | Upcoming Sensor: 2D 360° LiDAR |
| :--- | :--- | :--- |
| **Dimensionality** | 1D Single-Point Vector Rangefinder | 2D Omnidirectional Planar Slice |
| **Field of View (FoV)** | $2.0^\circ$ Narrow Spot | $360.0^\circ$ Continuous Circular |
| **Measurement Range** | $0.20\text{ m} \text{ to } 8.00\text{ m}$ | $0.15\text{ m} \text{ to } 12.00\text{ m}$ |
| **Sampling Speed** | Up to $250\text{ Hz}$ ($60\text{ Hz}$ paced) | $2,000 \text{ to } 8,000\text{ points/sec}$ |
| **Sensor Mass (Payload)** | **$< 5\text{ grams}$** | $170\text{--}200\text{ grams}$ |
| **Power Consumption** | **$< 0.35\text{ W}$ ($70\text{ mA}$ @ 5V)** | $1.5\text{--}2.5\text{ W}$ ($300\text{--}500\text{ mA}$ @ 5V) |
| **Cost** | **$<\$25$ USD** | $\$80\text{--}\$180$ USD |
| **Moving Parts** | Completely solid-state (zero motors) | Motorized mechanical rotating turret |
| **Wall Acquisition Mode** | Sequential 4-wall sweep (North $\rightarrow$ East $\rightarrow$ South $\rightarrow$ West) | Simultaneous 360° instantaneous perimeter capture |
| **Point Cloud Density** | $1,500 \text{--} 10,000$ points per room model | $50,000 \text{--} 200,000$ points per room scan |
| **Microcontroller Compatibility**| Direct GPIO UART on ESP-32 / Arduino Uno | ESP-32 high-speed DMA UART / Raspberry Pi / ROS |
| **Best-Fit Deployment** | Drone stand-off safety hold & ultra-light payload | Autonomous ground rovers & 360° SLAM navigation |

---

## 3. Dynamic Coordinate Frame & Translation Tracking Model

### 3.1 The Guide's Core Concept: Origin Initialization & Dynamic Displacement
During physical metrology and room scanning, a stationary sensor measures only from a single static perspective. When an operator or robotic mobile platform translates or drags the sensor through the physical environment, the system must maintain spatial continuity.

```
       Y (Elevation)
       ▲
       │         Target Object P_target = (X_p, Y_p, Z_p)
       │            *
       │           /
       │          / Distance vector d
       │         /
       │    [ Sensor Frame ] P_sensor(t) = (ΔX, ΔY, ΔZ)
       │       *
       │      /
       │     / Translation vector T(t)
       │    /
       └───*────────────────────────► X (Width)
     Origin Datum (0, 0, 0)
    /
   ▼
  Z (Depth)
```

### 3.2 Mathematical Formulation
1. **Initial Coordinate Origin Datum:**
   At the initialization of the scan ($t = 0$), the physical datum at the sensor's starting position is defined as the absolute World Origin:
   $$\vec{P}_{\text{sensor}}(0) = \begin{bmatrix} X_0 \\ Y_0 \\ Z_0 \end{bmatrix} = \begin{bmatrix} 0.000 \\ 0.000 \\ 0.000 \end{bmatrix}$$

2. **Kinematic Translation Vector (Dragging / Moving):**
   As the operator moves, drags, or flies the sensor through space over time $t$, the sensor position vector changes dynamically:
   $$\vec{P}_{\text{sensor}}(t) = \vec{P}_{\text{sensor}}(0) + \Delta \vec{T}(t) = \begin{bmatrix} 0 + \Delta X(t) \\ 0 + \Delta Y(t) \\ 0 + \Delta Z(t) \end{bmatrix}$$
   Where:
   * $\Delta X(t)$ represents lateral displacement (left/right across room width).
   * $\Delta Y(t)$ represents vertical displacement (elevation change/altitude climb).
   * $\Delta Z(t)$ represents longitudinal displacement (forward/backward depth).

3. **Global Target Point Transformation:**
   For any distance reading $d_{\text{calib}}(t)$ returned by the LiDAR at pan angle $\theta(t)$ and tilt angle $\phi(t)$, the true coordinates of the surface point in the fixed room frame are computed via rigid coordinate transformation:
   $$\vec{P}_{\text{target, global}}(t) = \vec{P}_{\text{sensor}}(t) + \mathbf{R}(\theta, \phi) \cdot \begin{bmatrix} 0 \\ 0 \\ d_{\text{calib}}(t) \end{bmatrix}$$
   Where $\mathbf{R}(\theta, \phi)$ is the 3D Euler rotation matrix:
   $$\mathbf{R}(\theta, \phi) = \begin{bmatrix} 
   \cos\theta & 0 & \sin\theta \\
   -\sin\theta\sin\phi & \cos\phi & \cos\theta\sin\phi \\
   -\sin\theta\cos\phi & -\sin\phi & \cos\theta\cos\phi
   \end{bmatrix}$$

4. **Expanded Cartesian Form:**
   $$\begin{cases}
   X_{\text{global}}(t) = \Delta X(t) + d_{\text{calib}}(t) \cdot \sin\theta(t) \cdot \cos\phi(t) \\
   Y_{\text{global}}(t) = \Delta Y(t) + d_{\text{calib}}(t) \cdot \sin\phi(t) \\
   Z_{\text{global}}(t) = \Delta Z(t) + d_{\text{calib}}(t) \cdot \cos\theta(t) \cdot \cos\phi(t)
   \end{cases}$$

### 3.3 Practical Implication for 3D Twin Reconstruction
* **Prevents Overwrite Collisions:** Instead of projecting all measurements into a single stationary cone, every motion of the sensor expands the mapped spatial envelope.
* **Sequential Wall Alignment:** When moving between Wall 1 (North), Wall 2 (East), Wall 3 (South), and Wall 4 (West), the sensor coordinate updates to the correct wall baseline offset, resulting in a closed $4.8\text{ m} \times 4.8\text{ m}$ rectangular envelope.

---

## 4. 3D Digital Twin Architecture & Structural Feature Classification

### 4.1 4-Wall Sequential Room Sweep Pipeline
The software pipeline coordinates a sequential 4-wall inspection workflow:
1. **Wall 1 (North / Front Wall):** Laser sweeps left-to-right across the baseline ($Z = +D_N$).
2. **Wall 2 (East / Right Wall):** Laser sweeps left-to-right across the baseline ($X = +D_E$).
3. **Wall 3 (South / Back Wall):** Laser sweeps left-to-right across the baseline ($Z = -D_S$).
4. **Wall 4 (West / Left Wall):** Laser sweeps left-to-right across the baseline ($X = -D_W$).

```
                      [ WALL 1 (NORTH): 4.8 m ]
                 NW ────────────────────────────── NE
                 │                                  │
                 │                                  │
 [ WALL 4        │                                  │ [ WALL 2
  (WEST): 4.8 m] │           ROOM CENTER            │  (EAST): 4.8 m]
                 │             (0, 0)               │
                 │                                  │
                 │                                  │
                 SW ────────────────────────────── SE
                      [ WALL 3 (SOUTH): 4.8 m ]
```

### 4.2 Structural Feature Classification Rules
The algorithm segments and color-codes all points into 3 distinct architectural classes based on baseline planar deviation $\Delta d$:

$$\Delta d = d_{\text{measured}} \cdot \cos(\theta) - d_{\text{baseline}}$$

```
  ┌────────────────────────────────────────────────────────────────────────┐
  │ Color Code │ Structural Element    │ Metrology Rule                   │
  ├────────────────────────────────────────────────────────────────────────┤
  │ 🟦 Cyan     │ Normal Flat Wall      │ |Δd| < 15 cm (Planar baseline)   │
  │ 🟧 Orange   │ Almari / Furniture    │ Δd ≤ -15 cm (Inward Bulge)       │
  │ 🟩 Green    │ Gate / Doorway Recess │ Δd ≥ +15 cm (Outward Recess)     │
  └────────────────────────────────────────────────────────────────────────┘
```

1. **🟦 Normal Wall Baseline ($| \Delta d | < 15\text{ cm}$):**
   * **Color:** Cyan (`#00E5FF`, RGB: `0, 229, 255`).
   * **Metrology:** Flat orthogonal perimeter walls, noise-filtered with a rolling median filter ($window = 5$).
2. **🟧 Inward Protrusion — Almari / Furniture ($\Delta d \le -15\text{ cm}$):**
   * **Color:** Warm Amber / Orange (`#FF8C00`, RGB: `255, 140, 0`).
   * **Physical Meaning:** An object (wardrobe, bookcase, desk, column) standing in front of the wall, reducing the measured distance.
   * **Model Rendering:** Points step inward into the room volume by the exact measured depth (e.g., $65\text{ cm}$ Almari depth). Vertical drop lines connect the high-elevation dimension badge to the object top.
3. **🟩 Outward Recess — Gate / Open Doorway ($\Delta d \ge +15\text{ cm}$):**
   * **Color:** Emerald Green (`#00E676`, RGB: `0, 230, 118`).
   * **Physical Meaning:** An opening, doorframe, corridor, or alcove indented past the nominal wall line, increasing the measured distance.
   * **Model Rendering:** Points step outward past the wall baseline (e.g., $60\text{ cm}$ door recess depth).

---

## 5. Software Stack, Data Formats & User Interfaces

```
  ┌───────────────────────┐       UART 115200       ┌────────────────────────┐
  │  TF-Luna LiDAR Sensor │ ──────────────────────► │ ESP-32 Microcontroller │
  └───────────────────────┘                         └───────────┬────────────┘
                                                                │ USB CDC Serial
                                                                ▼
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                           PYTHON DSP ENGINE                              │
  │  - serial_reader.py: Paced frame parser & ring-buffer oversampling       │
  │  - continuous_multi_point_scanner.py: Median filter & wall extrusion     │
  │  - reconstruct_3d_mesh.py: Delaunay 2.5D triangulation & OBJ generation  │
  └─────────────┬────────────────────────────────────────────┬───────────────┘
                │                                            │
                ▼                                            ▼
  ┌───────────────────────────┐                ┌─────────────────────────────┐
  │   3D POINT CLOUD & MESH   │                │   FULL-STACK WEB PLATFORM   │
  │ - data/room_mesh.ply      │                │ - Streamlit Dashboard (8501)│
  │ - data/room_mesh.obj      │                │ - Three.js WebGL 3D Viewer  │
  │ - reports/continuous_scan │                │ - real_scan_3d_viewer.html  │
  └───────────────────────────┘                └─────────────────────────────┘
```

### 5.1 Telemetry Packet Format
The ESP-32 firmware streams sanitized CSV records over serial at 115200 baud:
$$\text{yaw\_deg},\; \text{pitch\_deg},\; \text{distance\_cm},\; \text{flux}$$
Example: `0,0,61.40,1850` (Distance: $61.40\text{ cm}$, Signal Strength / Optical Flux: $1850$).

### 5.2 3D Model Export Specifications
* **`.PLY` Format (ASCII 1.0):** 9,969 vertices containing $[X, Y, Z, R, G, B]$ values. Compatible with MeshLab, CloudCompare, Blender, and Three.js `PLYLoader`.
* **`.OBJ` Format (Wavefront CAD):** Geometric vertices with normalized RGB color channels for AutoCAD and Revit import.
* **HTML WebGL Viewer:** Standalone browser viewer with OrbitControls, toggleable dimension banners, and camera presets (`View_3D_Room.bat`).

---

## 6. Project Roadmap & Revision Plan

* **Revision 0 (R0) — Current Baseline:**
  * ✅ TF-Luna 1D ToF sensor integration on ESP-32 via HardwareSerial.
  * ✅ Linear regression calibration ($y = 1.0228x + 3.20\text{ cm}$, $R^2 = 1.0$).
  * ✅ Continuous 4-wall sequential sweep with Almari/Gate feature classification.
  * ✅ Three.js WebGL interactive viewer with 3D dimension lines and badges.
  * ✅ GitHub repository synchronization and clean version control.
* **Revision 1 (R1) — Upcoming Engineering Milestones:**
  * 🔄 Hardware mount for 2D 360° LiDAR with high-speed UART DMA interface.
  * 🔄 Dynamic translation tracking: Integrating IMU (MPU6050) / optical flow odometry to compute continuous $(\Delta X, \Delta Y, \Delta Z)$ translation from initial $(0,0,0)$ origin.
  * 🔄 Real-time 2D SLAM planar occupancy grid generation.
  * 🔄 Automated multi-defect concrete spalling and crack classification engine.

---

## 7. Document Verification & Sign-Off

| Role | Name | Responsibility | Status |
| :--- | :--- | :--- | :--- |
| **Lead Developer** | Nisarg Joshi | LiDAR Integration, DSP Calibration & 3D WebGL Engine | **Verified (R0)** |
| **Hardware Engineer**| Team Member 2 | Sensor Mount, Pan-Tilt Mechanism & Power Subsystem | Verified (R0) |
| **Telemetry Lead** | Team Member 3 | UART Serial Pipeline & Streamlit Web Platform | Verified (R0) |
| **AI Specialist** | Mudit | Defect Feature Segmentation & Point Classification | Verified (R0) |
| **Drone Lead** | Aryan | ESP32-CAM Wireless Link & Flight Controller Interface | Verified (R0) |

*Document compiled and archived in repository: `docs/TF_LUNA_PROJECT_DOCUMENT_R0.md` & `TF_LUNA_PROJECT_DOCUMENT_R0.docx`.*
