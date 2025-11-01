import streamlit as st
st.title("Balloons and Snowflakes")
st.write("Click a button to see some fun effects!")
if st.button("Celebrate with Balloons!"):
    st.balloons()
    st.success("Balloons released!")
if st.button("Let it Snow!"):
    st.snow()
    st.success("Snow is falling!")