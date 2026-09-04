import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=1000, key="refresh")
# Read CSV
df = pd.read_csv("data/distance_data.csv")

# Dashboard Title
st.title("TF-Luna Distance Dashboard")

# Latest distance
current_distance = df["Distance"].iloc[-1]

st.metric(
    label="Current Distance",
    value=f"{current_distance} cm"
)

# Graph
st.subheader("Distance Graph")
st.line_chart(df["Distance"])

# Raw Data
st.subheader("Raw Data")
st.dataframe(df)