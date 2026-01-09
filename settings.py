import streamlit as st

st.set_page_config(page_title="Settings", layout = "wide", initial_sidebar_state = "expanded")

st.title("Settings")

col1, col2 = st.columns(2)

with col1:
    st.subheader("AI Provider")
    provider = st.selectbox(
        "Select Provider", 
        ["groq", "openai", "gemini"],
        index = ["groq", "openai", "gemini"].index(
        st.session_state.settings['provider']
    )
    )
    st.session_state.settings['provider'] = provider

with col2:
    st.subheader("Model Selection")

    model_options = {
        "groq": [
            "openai/gpt-oss-120b",
            "openai/gpt-oss-20b",
            "groq/compound",
            "llama-3.1-8b-instant",
            "meta-llama/llama-guard-4-12b",
            "moonshotai/kimi-k2-instruct-0905",
            "qwen/qwen3-32b"
        ],
        "openai": [
            "gpt-4o-mini",
            "gpt-4.1",
            "gpt-4.1-mini",
            "gpt-4.1-nano"
        ],
        "gemini": [
            "models/gemini-2.5-pro",
            "models/gemini-flash-latest",
            "models/gemini-flash-lite-latest",
            "models/gemini-2.5-flash",
            "models/gemini-2.5-flash-lite"
        ]
    }

    current_model = st.session_state.settings["model"]
    available_models = model_options[provider]
    if current_model not in available_models:
        current_model = available_models[0]

    model = st.selectbox(
        "Select Model",
        available_models,
        index = available_models.index(current_model)
    )
    st.session_state.settings["model"] = model

#API Keys
st.subheader("API Keys")

col1, col2, col3 = st.columns(3)

with col1:
    groq_key = st.text_input(
        "Groq API Key", 
        value=st.session_state.settings["groq_api_key"], 
        type="password", 
        help="Get your key from: https://console.groq.com"
    )
    st.session_state.settings["groq_api_key"] = groq_key

with col2:
    openai_key = st.text_input(
        "OpenAI API Key", 
        value=st.session_state.settings["openai_api_key"], 
        type="password", 
        help="Get your key from: https://platform.openai.com"
    )
    st.session_state.settings["openai_api_key"] = openai_key

with col3:
    gemini_key = st.text_input(
        "Gemini API Key", 
        value=st.session_state.settings["gemini_api_key"], 
        type="password", 
        help="Get your key from: https://aistudio.google.com/api-keys"
    )
    st.session_state.settings["gemini_api_key"] = gemini_key

#Model Parameters
st.markdown("-----")
st.subheader("Model Parameters")

col1, col2, = st.columns(2)

with col1:
    temperature = st.slider(
        "Temperature",
        min_value = 0.0,
        max_value = 2.0,
        value = st.session_state.settings["temperature"],
        step = 0.1,
        help = "Higher values make output more random, lower values are more focused"
    )
    st.session_state.settings["temperature"] = temperature

with col2:
    max_tokens = st.number_input(
        "Max Tokens",
        min_value = 1,
        max_value = 8192,
        value = st.session_state.settings["max_tokens"],
        step = 256,
        help = "Maximum length of the response"
    )
    st.session_state.settings["max_tokens"] = max_tokens

st.markdown("-----")
if st.button("Save Settings", type="primary", use_container_width = True):
    st.success("Settings saved successfully")
    st.balloons()

st.markdown("-----")
with st.expander("Current Configuration"):
    st.json(st.session_state.settings, expanded = True)