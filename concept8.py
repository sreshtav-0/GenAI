import streamlit as st
import os

st.title("Streamlit Input Elements")
st.header("Button Element", divider="rainbow")

if st.button("Click Me"):
    st.write("Button clicked!")

st.divider()

with st.form("drive school"):
    name = st.text_input("Name: ")
    age = st.number_input("Age: ", min_value=0, max_value=100, step=1)
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write(f"Name: {name}, Age: {age}")

st.divider()

st.download_button("Download Data", data="Sample data", 
file_name=os.path.join("Assets", "fetal_health.csv"))

st.divider()
st.link_button("Go to Streamlit", url="https://streamlit.io")

st.page_link("pages/about.py", "About Page")