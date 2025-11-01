import numpy as np
import pandas as pd
import streamlit as st

st.title("Charts-1")
st.header("Simple Chart elements")
st.subheader("Area Chart")

data = pd.DataFrame({
    "Day": pd.date_range(start="2023-01-01", periods=10),
    "Rainfall": np.random.randint(0, 100, size=10),
    "Temperature": np.random.randint(20, 40, size=10)
})

st.title("Weekly Weather Data")
st.area_chart(data.set_index("Day"))

st.markdown("Monthly Rainfall and Temperature Data")
st.area_chart(data=data, x="Day", y=["Rainfall", "Temperature"], color=["blue", "red"], use_container_width=True)

st.divider()

st.subheader("Bar Chart")
data1 = pd.DataFrame({
    "Product": ["A", "B", "C", "D"],
    "Sales": [150, 200, 300, 250],
    "Profit": [50, 80, 120, 90]
})

st.bar_chart(data=data1, x="Product", y=["Sales", "Profit"], color=["green", "orange"], use_container_width=True)

st.divider()

st.subheader("Line Chart")
st.line_chart(data=data1, x="Product", y=["Sales", "Profit"], color=["purple", "cyan"], use_container_width=True)
st.markdown("Monthly Visitors and Signups Data")

st.divider()

st.subheader("Map Chart")
data2 = pd.DataFrame({
  "latitude": [
    26.9239, 26.9149, 26.9228, 26.9850, 26.9257,
    26.9745, 26.9602, 26.9067, 26.8929, 26.8906, 
    26.8839, 26.8550, 26.9044, 26.9680, 26.9863, 
    26.7551, 26.8850, 26.9791, 27.0097, 27.0984
  ],
  "longitude": [
    75.8267, 75.8245, 75.8235, 75.8510, 75.8185,
    75.8552, 75.8450, 75.8166, 75.8181, 75.8672,
    75.8497, 75.8073, 75.8066, 75.8468, 75.8507,
    75.8596, 75.8500, 75.8475, 76.6166, 76.2625
  ]
})

st.map(data2, zoom=5, use_container_width=True)

st.divider()
st.subheader("Histogram Chart")
st.scatter_chart(
    data = data1,
    x = "Sales",
    y = "Profit",
    size="Product",
    color="green",
    use_container_width=True
)

