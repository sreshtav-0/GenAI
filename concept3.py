import streamlit as st
import time

@st.cache_data
def expensive_computation(x):
    time.sleep(5)  # Simulate a time-consuming computation
    return x * x

st.title("Streamlit DataFlow Example")
number = st.slider("Select a number", 0, 100, 50)
result = expensive_computation(number)
st.write(f"The square of {number} is {result}")

def my_callback():
    st.write("Button clicked!")

st.button("Click me!", on_click=my_callback)