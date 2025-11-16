import altair as alt
import seaborn as sns
import pandas as pd
import streamlit as st
import numpy as np
import graphviz
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
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

data2 = pd.DataFrame({
    "Product": ["Amazon", "Google", "Microsoft", "Apple", "Facebook"],
    "Stock Price": [3200, 2800, 300, 150, 350]
})

chart2 = alt.Chart(data2).mark_line(point=True).encode(
    x='Product',
    y='Stock Price'
).properties(title='Stock Prices of Tech Companies')

st.altair_chart(chart2, use_container_width=True)

st.divider()
st.subheader("st.graphviz_chart")

dot = graphviz.Digraph()
dot.node('A', 'Start')
dot.node('B', 'Process')
dot.node('C', 'Decision')
dot.edges(['AB', 'BC'])
dot.edge('C', 'A', constraint='false')

st.graphviz_chart(dot)

graph = """
digraph G {
    A -> B
    A -> C
    B -> D
    B -> E
    C -> F
    C -> G
}"""

st.graphviz_chart(graph, use_container_width=True)
st.text("Recursive Tree Example")

st.divider()
st.subheader("Streamlit Graphviz Chart")
iris_df = px.data.iris()

fig = px.scatter(iris_df, 
    x="sepal_width", y="sepal_length", color="species", size="petal_length",
    hover_data=["petal_width"])

event = st.plotly_chart(fig, key="iris", on_select="rerun", use_container_width=True)
event.selection

iris_df_corr = iris_df.drop(columns=["species"]).corr()
st.text("Scatter Plot for Iris Dataset")
fig2 = go.Figure(go.Heatmap(
    z=iris_df_corr.values,
    x=iris_df_corr.columns,
    y=iris_df_corr.columns,
    colorscale="rainbow",
))

st.plotly_chart(fig2, use_container_width=True)
st.text("Heatmap of Iris Dataset Correlation")

st.divider()
st.subheader("Matplotlib Chart")

x=np.linspace(0, 10, 100)
y=np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y, label='Sine Wave')
ax.set_title("Sine Wave Plot")
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.legend()

st.pyplot(fig)
st.text("Matplotlib Sine Wave Example")