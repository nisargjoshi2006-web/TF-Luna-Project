import streamlit as st
import pandas as pd
import json
import os
import streamlit.components.v1 as components
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="TF-Luna LiDAR Dashboard & 3D Viewer", layout="wide")

tab1, tab2, tab3 = st.tabs([
    "📊 Live Calibrated Monitor", 
    "📈 Calibration Curve & Scientific Report", 
    "🌐 3D Point Cloud & Mesh Suite"
])

# ----------------- TAB 1: LIVE MONITOR -----------------
with tab1:
    st_autorefresh(interval=1000, key="refresh_tab1")
    st.title("🎯 TF-Luna LiDAR Real-Time Monitor")

    # Load Calibration Info
    slope_m = 1.0
    intercept_c = 0.0
    r_squared = "N/A"
    calib_badge = "No Calibration Model Found"

    if os.path.exists("data/calibration.json"):
        try:
            with open("data/calibration.json", "r") as f:
                cinfo = json.load(f)
                slope_m = cinfo.get("slope_m", 1.0)
                intercept_c = cinfo.get("intercept_c", 0.0)
                r_squared = cinfo.get("r_squared", "N/A")
                calib_badge = f"✅ Linear Regression Active: Distance = ({slope_m:.4f} × Raw) + ({intercept_c:+.2f}) | R² = {r_squared}"
        except Exception:
            pass

    st.info(f"**Model Status:** {calib_badge}")

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
                col1, col2, col3 = st.columns(3)
                latest_raw = df[raw_col].iloc[-1]
                latest_cal = df[cal_col].iloc[-1]
                error_diff = latest_cal - latest_raw

                with col1:
                    st.metric("Raw Sensor Measurement", f"{latest_raw:.2f} cm")
                with col2:
                    st.metric("Calibrated Ground-Truth", f"{latest_cal:.2f} cm", delta=f"{error_diff:+.2f} cm corrected")
                with col3:
                    st.metric("Model Precision (R²)", f"{r_squared}")

                st.subheader("📈 Live Distance Tracking")
                st.line_chart(df[[raw_col, cal_col]])

                st.subheader("📋 Recent Measurement Logs")
                st.dataframe(df.tail(15))
        else:
            st.warning("Waiting for data logs in `data/distance_data.csv`...")
    else:
        st.warning("No data file found yet. Run `python data_collection/serial_reader.py` to start logging.")

# ----------------- TAB 2: CALIBRATION CURVE & REPORT -----------------
with tab2:
    st.title("📈 Sensor Calibration Curve & Accuracy Report")
    st.markdown("This section proves sensor fidelity by fitting empirical laser measurements against physical ground truth across multiple benchmarks.")

    if os.path.exists("data/calibration.json"):
        with open("data/calibration.json", "r") as f:
            calib_data = json.load(f)

        points = calib_data.get("calibration_points", [])
        if points:
            raw_vals = [p["measured_cm"] for p in points]
            true_vals = [p["true_cm"] for p in points]
            m = calib_data.get("slope_m", 1.0)
            c = calib_data.get("intercept_c", 0.0)
            r2 = calib_data.get("r_squared", 1.0)

            # Interactive Plotly Calibration Curve
            fig = go.Figure()
            # Measured data points
            fig.add_trace(go.Scatter(
                x=raw_vals, y=true_vals, mode='markers',
                name='Empirical Benchmark Points',
                marker=dict(size=12, color='#ff6b35', symbol='diamond')
            ))
            # Fitted line
            line_x = [min(raw_vals) * 0.8, max(raw_vals) * 1.2]
            line_y = [m * lx + c for lx in line_x]
            fig.add_trace(go.Scatter(
                x=line_x, y=line_y, mode='lines',
                name=f'Fitted Curve: y = {m:.4f}x + {c:+.2f}',
                line=dict(color='#00e5ff', width=3, dash='dash')
            ))

            fig.update_layout(
                title=f"Sensor Calibration Curve (R² = {r2})",
                xaxis_title="Raw Measured Distance (cm)",
                yaxis_title="True Ground-Truth Distance (cm)",
                template="plotly_dark",
                height=450
            )
            st.plotly_chart(fig, use_container_width=True)

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📊 Regression Parameters")
                st.write(f"- **Slope / Scale Factor (m):** `{m:.4f}`")
                st.write(f"- **Zero-Offset / Intercept (c):** `{c:+.4f} cm`")
                st.write(f"- **Coefficient of Determination (R²):** `{r2:.5f}`")
                st.write(f"- **Timestamp:** `{calib_data.get('calibrated_at', 'N/A')}`")
            with col2:
                st.subheader("📋 Empirical Benchmark Table")
                bench_df = pd.DataFrame(points)
                bench_df["Error (cm)"] = bench_df["true_cm"] - bench_df["measured_cm"]
                bench_df.columns = ["True Distance (cm)", "Raw Measured (cm)", "Std Dev (cm)", "Error Offset (cm)"]
                st.dataframe(bench_df)
    else:
        st.warning("No calibration data recorded yet. Run `python data_collection/calibrate.py` to record multi-point data.")

# ----------------- TAB 3: 3D VIEWER -----------------
with tab3:
    st.title("🌐 PLY·FORGE — 3D LiDAR Point Cloud & Mesh Suite")
    st.markdown("Load any `.ply` point cloud file or click **Load Demo** inside the viewer to interactively rotate, zoom, and inspect 3D surfaces.")
    
    html_path = "dashboard/templates/ply_forge.html"
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        components.html(html_content, height=720, scrolling=False)
    else:
        st.error("Viewer template not found.")
