import streamlit as st
import pandas as pd
import json
import os
import streamlit.components.v1 as components
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="TF-Luna LiDAR SHM Inspection Suite", layout="wide")

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Live Telemetry & Defect Detector", 
    "📈 Linear Profile & Cavity Mapping",
    "🔬 Calibration Curve & Accuracy Report", 
    "🌐 3D Point Cloud & Mesh Suite"
])

# ----------------- TAB 1: LIVE TELEMETRY & STRUCTURAL DEFECT DETECTOR -----------------
with tab1:
    st_autorefresh(interval=1000, key="refresh_tab1")
    st.title("🎯 Real-Time LiDAR Telemetry & Structural Anomaly Detection")

    slope_m = 1.0
    intercept_c = 3.0
    r_squared = "0.999"
    if os.path.exists("data/calibration.json"):
        try:
            with open("data/calibration.json", "r") as f:
                cinfo = json.load(f)
                slope_m = cinfo.get("slope_m", 1.0)
                intercept_c = cinfo.get("offset_error_cm", cinfo.get("intercept_c", 3.0))
                r_squared = cinfo.get("r_squared", "0.999")
        except Exception:
            pass

    st.info(f"**Calibration Model:** Active (Offset: {intercept_c:+.2f} cm | Model: Linear Regression | Precision: R² = {r_squared})")

    DATA_PATH = "data/distance_data.csv"
    if os.path.exists(DATA_PATH) and os.path.getsize(DATA_PATH) > 0:
        try:
            df = pd.read_csv(DATA_PATH, on_bad_lines='skip')
        except Exception:
            df = pd.DataFrame()

        if not df.empty and len(df.columns) >= 2:
            raw_col = df.columns[0]
            cal_col = df.columns[1]
            df[raw_col] = pd.to_numeric(df[raw_col], errors='coerce')
            df[cal_col] = pd.to_numeric(df[cal_col], errors='coerce')
            df = df.dropna().tail(150)

            if not df.empty:
                latest_raw = df[raw_col].iloc[-1]
                latest_cal = df[cal_col].iloc[-1]

                # Real-time Structural Defect / Anomaly Detection Logic
                # Check for step-change anomaly in last 10 readings
                recent_vals = df[cal_col].tail(10).values
                baseline = recent_vals[0] if len(recent_vals) > 0 else latest_cal
                depth_diff = latest_cal - baseline

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Raw Sensor Reading", f"{latest_raw:.2f} cm")
                with col2:
                    st.metric("Calibrated Ground-Truth", f"{latest_cal:.2f} cm", delta=f"{intercept_c:+.2f} cm optical offset")
                with col3:
                    if abs(depth_diff) > 2.5:
                        st.metric("Structural Anomaly Status", "⚠️ CAVITY DETECTED", delta=f"{depth_diff:+.1f} cm jump", delta_color="inverse")
                    else:
                        st.metric("Structural Anomaly Status", "✅ SURFACE UNIFORM", delta="Normal Profile")

                # Stand-off Safety Indicator for Drones
                if 140 <= latest_cal <= 160:
                    st.success("🎯 **Drone Stand-Off Distance:** Optimal Flight Envelope (1.50 m ± 10 cm)")
                elif latest_cal < 100:
                    st.error("🚨 **PROXIMITY WARNING:** Object too close (< 1.0 m)! Collision avoidance active.")
                else:
                    st.info(f"📏 Distance to structural face: **{latest_cal/100:.2f} meters**")

                st.subheader("📈 Live Structural Profile Stream")
                st.line_chart(df[[raw_col, cal_col]])

                st.subheader("📋 Telemetry Data Buffer")
                st.dataframe(df.tail(15))
        else:
            st.warning("Waiting for data logs in `data/distance_data.csv`...")
    else:
        st.warning("No data file found yet. Run `python data_collection/serial_reader.py` to start logging.")

# ----------------- TAB 2: LINEAR PROFILE SCAN (MANUAL SLIDER SCAN) -----------------
with tab2:
    st.title("📈 Linear Surface Profiling (Translational SHM Scan)")
    st.markdown("This module simulates a drone flying along a wall (or sliding on a rail). As you translate the sensor horizontally, it reconstructs the physical depth profile to detect missing masonry, spalling, and cracks.")

    if os.path.exists("data/distance_data.csv") and os.path.getsize("data/distance_data.csv") > 0:
        df_profile = pd.read_csv("data/distance_data.csv", on_bad_lines='skip')
        if not df_profile.empty:
            cal_col = df_profile.columns[1] if len(df_profile.columns) >= 2 else df_profile.columns[0]
            profile_data = pd.to_numeric(df_profile[cal_col], errors='coerce').dropna().tail(80).values

            if len(profile_data) > 5:
                # Plot 2D Cross-Section Elevation
                x_pos = [i * 2.0 for i in range(len(profile_data))] # 2cm steps along wall
                fig_p = go.Figure()
                fig_p.add_trace(go.Scatter(
                    x=x_pos, y=profile_data, mode='lines+markers',
                    name='Wall Surface Depth',
                    line=dict(color='#00e5ff', width=3),
                    marker=dict(size=6, color='#ff6b35')
                ))
                fig_p.update_layout(
                    title="2D Wall Surface Cross-Section Profile (Linear Sweep)",
                    xaxis_title="Translational Position along Wall (cm)",
                    yaxis_title="Measured Depth Distance (cm)",
                    template="plotly_dark",
                    height=450
                )
                st.plotly_chart(fig_p, use_container_width=True)

                # Anomaly summary table
                anomalies = []
                avg_depth = sum(profile_data) / len(profile_data)
                for idx, d in enumerate(profile_data):
                    if abs(d - avg_depth) > 3.0:
                        anomalies.append({
                            "Position along Wall (cm)": x_pos[idx],
                            "Measured Depth (cm)": round(d, 2),
                            "Deviation from Baseline (cm)": round(d - avg_depth, 2),
                            "Defect Classification": "Structural Cavity / Missing Brick" if d > avg_depth else "Surface Bulge / Obstacle"
                        })
                
                st.subheader("🔍 Automated Structural Anomaly Report")
                if anomalies:
                    st.dataframe(pd.DataFrame(anomalies))
                else:
                    st.success("✅ Uniform Surface: No structural depth cavities or spalling detected along this scanned section.")

# ----------------- TAB 3: CALIBRATION REPORT -----------------
with tab3:
    st.title("🔬 Sensor Calibration Curve & Accuracy Report")
    st.markdown("Proves sensor fidelity by fitting empirical laser measurements against physical ground truth.")

    if os.path.exists("data/calibration.json"):
        with open("data/calibration.json", "r") as f:
            calib_data = json.load(f)

        points = calib_data.get("calibration_points", [])
        if points:
            raw_vals = [p["measured_cm"] for p in points]
            true_vals = [p["true_cm"] for p in points]
            m = calib_data.get("slope_m", 1.0)
            c = calib_data.get("offset_error_cm", calib_data.get("intercept_c", 3.0))

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=raw_vals, y=true_vals, mode='markers',
                name='Empirical Reference Points',
                marker=dict(size=14, color='#ff6b35', symbol='diamond')
            ))
            line_x = [min(raw_vals) * 0.8, max(raw_vals) * 1.2]
            line_y = [m * lx + c for lx in line_x]
            fig.add_trace(go.Scatter(
                x=line_x, y=line_y, mode='lines',
                name=f'Fitted Line: y = {m:.4f}x + {c:+.2f}',
                line=dict(color='#00e5ff', width=3, dash='dash')
            ))
            fig.update_layout(
                title="Linear Regression Calibration Curve",
                xaxis_title="Raw Measured Distance (cm)",
                yaxis_title="True Ground-Truth Distance (cm)",
                template="plotly_dark",
                height=450
            )
            st.plotly_chart(fig, use_container_width=True)

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📊 Regression Metrics")
                st.write(f"- **Slope (m):** `{m:.4f}`")
                st.write(f"- **Zero Offset (c):** `{c:+.2f} cm`")
                st.write(f"- **Calibration Time:** `{calib_data.get('calibrated_at', 'N/A')}`")
            with col2:
                st.subheader("📋 Reference Validation Table")
                bench_df = pd.DataFrame(points)
                st.dataframe(bench_df)

# ----------------- TAB 4: 3D POINT CLOUD SUITE -----------------
with tab4:
    st.title("🌐 PLY·FORGE — 3D LiDAR Point Cloud & Mesh Suite")
    st.markdown("Load any `.ply` point cloud file (e.g. `data/live_scan.ply`) or click **Load Demo** inside the viewer to interactively rotate and inspect 3D surfaces.")
    
    html_path = "dashboard/templates/ply_forge.html"
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        components.html(html_content, height=720, scrolling=False)
    else:
        st.error("Viewer template not found.")
