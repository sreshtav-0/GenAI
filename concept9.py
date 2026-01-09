import streamlit as st
import os
import numpy as np

st.set_page_config("Streamlit Media and Chat Elements")
st.title("Streamlit Media and Chat Elements")
st.header("Media Elements", divider="rainbow")

#StreamLit Logo
st.logo(os.path.join("StreamLit/Assets", "streamlit_logo.png"), size = "medium")
st.divider()

st.subheader("Audio Element")
audio_file = os.path.join("StreamLit/Assets", "yoo.mp3")
st.audio(audio_file, format="audio/mp3")

sample_rate = 44100
seconds = 3
frequency_la = 440

t = np.linspace(0, seconds, seconds * sample_rate, False)
note_la = 0.5 * np.sin(2 * np.pi * frequency_la * t)
st.audio(note_la, sample_rate=sample_rate)
st.divider()

st.subheader("Neural Networks Image")
st.image(os.path.join("StreamLit/Assets", "neural_networks.png"), caption="Neural Networks", use_container_width=True)
st.write("A picture is a simple perception.")
st.divider()

#Streamlit Video Element
st.subheader("Video Element")
st.video(os.path.join("StreamLit/Assets", "TheGreatTreasureHunt.mp4"), format="video/mp4")
st.divider()

#Video Link Element
st.subheader("Video Element")
st.video("https://www.youtube.com/watch?v=JESyTQqJn0Y")
st.divider()

#PDF Element
st.subheader("PDF Element")
try:
    st.pdf(os.path.join("StreamLit/Assets", "StreamlitInputElement.pdf"))
except Exception as e:
    st.exception(e)
st.divider()



