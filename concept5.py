import pandas as pd
import streamlit as st
import numpy as np

data = {
    "Name": ["Alice", "Bob", "Charlie", "David"],
    "Age": [24, 30, 22, 35],
    "City": ["New York", "Los Angeles", "Chicago", "Houston"]
}

df = pd.DataFrame(data)
st.dataframe(df)

st.markdown("### Editable Data Table using st.data_editor")
st.write("You can edit the data directly in the table below:")

edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

st.markdown("### Updated Data Table")
st.dataframe(edited_df, use_container_width=True)

column_types = {
    "Text Column": ["Hello", "Streamlit"],
    "Number Column": [10, 20],
    "Checkbox Column": [True, False],
    "Selectbox Column": ["Option 1", "Option 2"],
    "Datetime Column": [
        pd.to_datetime(["2023-01-01", "2023-06-01"])
    ],
    "Date Column": [
        pd.to_datetime(["2023-01-01", "2023-06-01"]).date()
    ],
    "Time Column": [
        pd.to_datetime(["12:00", "15:30"]).time()
    ],
    "JSON Column": [{"key1": "value1", "key2": 2}, {"keyA": "valueA", "keyB": 3}],
    "List Column": [[1, 2, 3], ["a", "b", "c"]],
    "Link Column": ["https://streamlit.io", "https://streamlit.io"],
    "Image Column": ["https://streamlit.io/images/brand/streamlit-mark-color.png", "https://streamlit.io/images/brand/streamlit-mark-color.png"],
    "Area Chart Column": [np.random.randint(0, 100), np.random.randint(0, 100)],
    "Line Chart Column": [np.random.randint(0, 100), np.random.randint(0, 100)],
    "Bar Chart Column": [np.random.randint(0, 100), np.random.randint(0, 100)],
    "Progress Column": [np.random.randint(0, 100), np.random.randint(0, 100)]
}

df = pd.DataFrame(column_types)
st.dataframe(df, column_config={
    "Text Column": st.column_config.TextColumn("This is a text column"),
    "Number Column": st.column_config.NumberColumn("This is a number column"),
    "Checkbox Column": st.column_config.CheckboxColumn("This is a checkbox column"),
    "Selectbox Column": st.column_config.SelectboxColumn("This is a selectbox column", options=["Option 1", "Option 2", "Option 3"]),
    "Datetime Column": st.column_config.DatetimeColumn("This is a datetime column"),
    "Date Column": st.column_config.DateColumn("This is a date column"),
    "Time Column": st.column_config.TimeColumn("This is a time column"),
    "JSON Column": st.column_config.JSONColumn("This is a JSON column"),
    "List Column": st.column_config.ListColumn("This is a list column"),
    "Link Column": st.column_config.LinkColumn("This is a link column"),
    "Image Column": st.column_config.ImageColumn("This is an image column"),
    "Area Chart Column": st.column_config.AreaChartColumn("This is an area chart column"),
    "Line Chart Column": st.column_config.LineChartColumn("This is a line chart column"),
    "Bar Chart Column": st.column_config.BarChartColumn("This is a bar chart column"),
    "Progress Column": st.column_config.ProgressColumn("This is a progress column")
    }, use_container_width=True)
    
st.divider()
st.table(df)
st.metric(label="Temperature", value=70, delta="1.2 °F")
st.metric(
    label="Revenue", 
    value="$12,000",
    delta="+15%",
    help="Metric shos the percentage increase in revenue."
)

st.divider()
data_dict = {
    "name": ["Eve Frank"],
    "age": 28,
    "skills": ['Python', 'Data Analysis'],
    "details": {
        "city": "San Francisco",
        "country": "USA",
        "website": "https://evefrank.dev"
    }
}

st.json(data_dict)