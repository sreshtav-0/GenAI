import streamlit as st
import os
import time

st.set_page_config(page_title="StreamLit Chat Elements")

st.header("Chat Elements", divider="rainbow")

with st.chat_message("user"):
    st.write("Hello")

with st.chat_message("assistant"):
    st.write("Hi, how can i help you")

with st.chat_message("system"):
    st.write("This is a system message.")

with st.status("Downloading data...", expanded=True) as status:
    st.write("Searching for data...")
    time.sleep(2)
    st.write("Found URL.")
    time.sleep(1)
    st.write("Downloading data...")
    time.sleep(1)
    status.update(
        label="Download complete!", state="complete", expanded=False
    )

st.button("Rerun")