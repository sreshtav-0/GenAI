import altair as alt
import seaborn as sns
import pandas as pd
import streamlit as st
import numpy as np

st.title("Charts-2")
st.header("Advanced Chart elements")

st.subheader("st.altair_chart")

data1 = pd.DataFrame({
    "Product": ["A", "B", "C", "D", "E"],
    "Sales": [23, 45, 12, 67, 34],
    "Profit": [5, 15, 7, 20, 10]
})
chart = alt.Chart(data1).mark_bar().encode(
    x='Product',
    y='Sales',
    color='Profit'
).properties(title='Product Sales and Profit')

st.altair_chart(chart, use_container_width=True)

