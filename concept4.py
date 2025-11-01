import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import time

st.title("Streamlit Main Text Elements")
st.header("Introduction to text Elemts", divider="rainbow")
st.subheader("write() and write_streamlit()")

code = """
<code>Hello Sreshtav</code>
"""
st.write("Hello", "World!", code, ":smile", unsafe_allow_html = True)
st.write(42, 3.14, True, None)
st.write(
    pd.DataFrame(
        {
            "First Column": [10, 20, 30, 40],
            "Second Column": ["100", "200", "300", "400"],
        }
    )
)

df = pd.DataFrame(np.random.randn(200, 3), columns=["a", "b", "c"])
chart = alt.Chart(df).mark_circle().encode(x="a", y="b", size="c", color="c", tooltip=["a", "b", "c"])
st.write(chart)

st.divider()
LOREM_IPSUM = """
Lorem ipsum dolor sit amet, 
consectetur adipiscing elit, 
sed do eiusmod tempor incididunt 
ut labore et dolore magna aliqua.
Ut enim ad minim veniam
"""

def stream_data():
    for word in LOREM_IPSUM.split():
        yield word
        time.sleep(0.02)

if st.button("Stream Data"):
    st.write_stream(stream_data)

st.divider()
"""
Main Text Elements in Streamlit
✅ st.write()
✅ st.text()
✅ st.markdown()
✅ st.title()
✅ st.header()
✅ st.subheader()
✅ st.caption()
✅ st.code()
✅ st.latex()
"""

st.text("This is plain text output using st.text()")

st.markdown("**This is bold text using st.markdown()**")
st.markdown("*This is italic text using st.markdown()*")
st.markdown("~~This is strikethrough text using st.markdown()~~")
st.markdown("'This is code markdown text using st.markdown'")

st.caption("This is a caption using st.caption()")

code_snippet = """
    def hello_world():
        print("Hello, World!")
"""
st.code(code_snippet, language="python", line_numbers=True)

code_snippet1 = """
function addition(num1, num2) {
    return num1 + num2;
}
"""

st.code(code_snippet1, language="javascript", line_numbers=True)

st.latex("""
a^2 + b^2 = c^2
""")

with st.echo():
    st.write("This code block shows both the code and its output.")


st.divider()
st.success("This is a success message")
st.error("This is an error message")
st.warning("This is a warning message")
st.info("This is an informational message")

try:
    1 / 0
except Exception as e:
    st.exception(e)
    
st.divider()
st.subheader("Utilities")

st.html("<h1 style='color:blue;'>This is an HTML heading</h1>")
st.help(st.write_stream)