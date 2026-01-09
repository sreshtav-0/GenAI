import streamlit as st

st.set_page_config(
    page_title = "Multi-Model multi models AI Chat",
    layout = "wide",
    initial_sidebar_state = "expanded"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "settings" not in st.session_state:
    st.session_state.settings = {
        "provider" : "groq",
        "model" : "llama-3.3-70b-versatile",
        "temperature" : 0.7,
        "max_tokens" : 1024,
        "groq_api_key" : "",
        "openai_api_key" : "",
        "gemini_api_key" : ""
    }

st.title("Multi-Modal AI Bot")
st.info("Select a page from the sidebar to get started.")
st.write("""
Features
- Multiple AI Providers: Gemini, Groq, and OpenAI
- Vision Capabilities: Able to perform image analysis         
- Conversation History: Maintains context across images
- Customizable Settings: Model and parameter adjustments are possible
""")

