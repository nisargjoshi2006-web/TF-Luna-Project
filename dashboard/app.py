import streamlit as st
import pandas as pd

df = pd.read_csv("data/distance_data.csv")

st.title("TF-Luna Distance Dashboard")

current_distance = df["Distance"].iloc[-1]

st.metric(
    label="Current Distance",
    value=f"{current_distance} cm"
)

st.subheader("Distance Graph")
st.line_chart(df["Distance"])

st.subheader("Raw Data")
st.dataframe(df)