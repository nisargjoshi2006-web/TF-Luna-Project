import streamlit as st
import pandas as pd
import json
import os
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="TF-Luna LiDAR Dashboard & 3D Viewer", layout="wide")

# Tabs for 2D Live Dashboard and 3D PLY Viewer
tab1, tab2 = st.tabs(["📊 Live Calibrated 2D Monitor", "🌐 Interactive 3D Point Cloud & Mesh Viewer"])

with tab1:
    # Refresh every second
    st_autorefresh(interval=1000, key="refresh_tab1")

    st.title("🎯 TF-Luna LiDAR Calibrated Dashboard")

    # Check Calibration status
    calib_offset = 0.0
    calib_status = "No calibration file found (Offset = 0.0 cm)"
    if os.path.exists("data/calibration.json"):
        try:
            with open("data/calibration.json", "r") as f:
                calib_info = json.load(f)
                calib_offset = calib_info.get("offset_error_cm", 0.0)
                calib_status = f"✅ Active (Offset: {calib_offset:+.2f} cm | Ref: {calib_info.get('true_distance_cm', 'N/A')} cm)"
        except Exception:
            pass

    st.info(f"**Calibration Status:** {calib_status}")

    DATA_PATH = "data/distance_data.csv"

    def load_data(filepath):
        if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
            return pd.DataFrame()
        try:
            df = pd.read_csv(filepath, on_bad_lines='skip')
            return df
        except Exception:
            return pd.DataFrame()

    df = load_data(DATA_PATH)

    if not df.empty:
        num_cols = len(df.columns)
        
        if num_cols >= 2:
            raw_col = df.columns[0]
            cal_col = df.columns[1]
        else:
            raw_col = df.columns[0]
            cal_col = df.columns[0]

        df[raw_col] = pd.to_numeric(df[raw_col], errors='coerce')
        if cal_col != raw_col:
            df[cal_col] = pd.to_numeric(df[cal_col], errors='coerce')
        df = df.dropna().tail(200)

        if not df.empty:
            col1, col2 = st.columns(2)

            latest_raw = df[raw_col].iloc[-1]
            latest_cal = df[cal_col].iloc[-1]

            with col1:
                st.metric(label="Raw Sensor Distance", value=f"{latest_raw:.2f} cm")
            with col2:
                st.metric(label="Calibrated Distance (Accurate)", value=f"{latest_cal:.2f} cm", delta=f"{calib_offset:+.2f} cm")

            # Live Graph
            st.subheader("📈 Live Distance Comparison")
            if cal_col != raw_col:
                st.line_chart(df[[raw_col, cal_col]])
            else:
                st.line_chart(df[raw_col])

            # Recent Data Table
            st.subheader("📋 Recent Measurement Logs")
            st.dataframe(df.tail(15))
        else:
            st.warning("Waiting for numeric data from sensor...")
    else:
        st.warning("No data file found yet. Run `python data_collection/serial_reader.py` to start logging.")

with tab2:
    st.title("🌐 PLY·FORGE — 3D LiDAR Point Cloud & Mesh Suite")
    st.markdown("Load any `.ply` point cloud file (or click **Load Demo** inside the viewer) to interactively rotate, downsample, remove noise, create triangular meshes, and export.")
    
    html_path = "dashboard/templates/ply_forge.html"
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        components.html(html_content, height=720, scrolling=False)
    else:
        st.error("Viewer template not found.")
