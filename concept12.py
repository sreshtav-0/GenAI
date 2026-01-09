import streamlit as st
import os
import time

st.set_page_config(page_title="Streamlit Layout and Containers")

st.header("Layout and Containers", divider="rainbow")

#Containers with columns

with st.container(width="stretch", key="my-streamlit"):
    st.write("st.container inserts an invisible container into " \
    "your app that can be used to hold multiple elements")
    st.write("st.columns(N) inserts containers laid out as " \
    "side-by-side columns")
    vertical_alignment = st.selectbox("Vertical Alignment", 
    ["top", "center", "bottom"], index=2)
    col1, col2, col3 = st.columns(3, vertical_alignment=vertical_alignment, border=True)


    with col1:
        st.header("A cat")
        st.image("https://static.streamlit.io/examples/cat.jpg")

    with col2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg")

    with col3:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg")

st.markdown(
"""
<style>
    .st-key-my-streamlit{
        background-color: gray;
        padding: 1rem;
        backdrop-filter: blur(15px);
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.divider()

#st.expander
st.subheader("st.expander()")
with st.expander("See more details"):
    st.write("Here's the hidden content until expanded")

with st.expander("Give feedback"):
    st.text_area(label="Your Feedback", width="stretch")

my_expander = st.expander("Programmatically controlled expander", expanded=False)
my_expander.write("You can control the expanded state of this expander using the expanded parameter")
my_expander.image(os.path.join("StreamLit/Assets", "streamlit_logo.png"))
st.divider()

#st.sidebar
st.subheader("st.sidebar()")

st.sidebar.header("Filters")

#Object Notation
option = st.sidebar.selectbox(
    "How would you like to be contacted",
    ("Email", "Home phone", "Mobile phone")
)

#Can only have 1 sidebar
#Context Manager - st.with
# Other potential context managers are st.echo, st.spinner, st.toast
with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express(2-5 days)")
    )

    with st.echo():
        st.write("This code will be printed to the sidebar")

    with st.spinner("Loading..."):
        time.sleep(2)
    st.success("Done")
st.divider()

#st.tabs
st.subheader("st.tabs()")
tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

with tab1:
    st.header("A cat")
    st.image("https://static.streamlit.io/examples/cat.jpg")

with tab2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg")

with tab3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg")

st.divider()

tab4, tab5, tab6 = st.tabs(["Overview", "Settings", "Feedback"])
tab4.header("Overview Section")
tab4.write("Display key metrics or summaries here.")

tab5.header("Settings")
tab5.checkbox("Enable feature")
tab5.slider("Set Level", 0, 100)

tab6.header("Feedback")
tab6.text_area("Your Suggestions")

st.divider()

#st.page_link

st.subheader("st.page_link()")
st.page_link("concept12.py", label="Home")
st.page_link("pages/about.py", label="About")
st.page_link("pages/page_1.py", label="Go to Page 1")
st.page_link("pages/page_2.py", label="Go to Page 2")
st.page_link("https://www.google.com", label="Search Google")

st.divider()

#st.empty
st.subheader("st.empty()")
with st.empty():
    for seconds in range(10):
        st.write(f"{seconds} seconds have passed")
        time.sleep(1)
        st.write(":material/check: 10 seconds over!")
        st.button(f"{seconds}", key=f"button-{seconds}")

st.divider()

#st.popover
st.subheader("st.popover()")
with st.popover("Open popover"):
    st.markdown("Hello World 👋")
    name = st.text_input("What's your name?")

st.write("Your name:", name)

st.divider()

#st.space
st.subheader("st.space()")
with st.container(horizontal=True):
    st.button("Left")
    st.space("stretch")
    st.button("Right")

st.divider()

