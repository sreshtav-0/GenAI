import time
import streamlit as st

st.set_page_config(page_title="StreamLit Status Elements")

st.header("Callouts", divider="rainbow")

st.subheader("Success!")
st.success("Mission Accomplished")
st.divider()

st.subheader("Information")
st.info("The apps update daily at midnight")
st.divider()

st.subheader("Warning!")
st.warning("This action may have unintended consequences. "
"Are you sure to proceed?")
st.divider()

st.subheader("Error!")
st.error("An error has occurred during request processing.")
st.divider()

st.subheader("Exception!")
st.exception(Exception("An exception has occurred!"))
st.divider()

st.header("Status Indicators", divider="rainbow")

#Progress Bar
st.subheader("Progress Bar")
progress_bar = st.progress(0, text="Fetching...", width="stretch")
time.sleep(2)
for percent_complete in range(0, 100):
    time.sleep(0.1)
    progress_bar.progress(percent_complete + 1, text=f"{percent_complete + 1}% Complete", width="stretch")

#Spinner Element
st.subheader("Spinner")
with st.spinner("Fetching data...", show_time=True, width="stretch"):
    time.sleep(3)
    st.success("Successfully fetched data!")

#Empty Element
st.subheader("Empty")
with st.empty():
    for seconds in range(10):
        st.write(f"{seconds} seconds have passed")
        time.sleep(1)
        st.write(":material/check: 10 seconds over!")
        st.button(f"{seconds}", key=f"button-{seconds}")
st.divider()

#Toast Element
st.subheader("Toast Element")
st.toast("This is a celebratory toast message")

if st.button("Three cheers"):
    st.toast("Hip!")
    time.sleep(0.5)
    st.toast("Hip!")
    time.sleep(0.5)
    st.toast("Hooray!", icon="🎉")

st.divider()

