import streamlit as st
from utils.llm_handler import LLMHandler, encode_image 

st.set_page_config(
    page_title="Chat",
    page_icon="🗨️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🗨️ Chat Interface")

# Sidebar controls
with st.sidebar:
    st.header("Chat Controls")

    # Display current settings
    st.info(f"""
    **Provider:** {st.session_state.settings['provider'].upper()}
    **Model:**: {st.session_state.settings['model']}
    **Temperature:**: {st.session_state.settings['temperature']}
    """)

    # Image upload
    st.markdown("---")
    uploaded_image = st.file_uploader("Upload Image (Optional)", type=["png", "jpg", "jpeg", "webp"])

    if uploaded_image:
        st.image(uploaded_image, caption="Uploaded Image", use_column_width="auto")

    # Clear chat button
    st.markdown("---")
    if st.button("🚮Clear Chat Hisotry", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Check if API keys are set
settings = st.session_state.settings
api_key_field = f"{settings['provider']}_api_key"
api_key = settings.get(api_key_field, "")

if not api_key:
    st.warning(f"🤚🚫Please set your {settings['provider']} API key in the Settings page.")
    st.stop()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Initialize LLM handler
                llm = LLMHandler(
                    provider = settings["provider"],
                    api_key=api_key   ,
                    model=settings["model"],
                    temperature=settings["temperature"],
                    max_tokens=settings["max_tokens"]
                )
                # Process image if uploaded 
                image_data = None
                if uploaded_image:
                    uploaded_image.seek(0) # Reset file pointer 
                    image_data = encode_image(uploaded_image)

                # Get response 
                response = llm.chat(st.session_state.messages, image_data)

                # Display and save response 
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content":response})

            except Exception as e:
                error_msg = f"Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                st.stop()


# Show message count
st.sidebar.markdown(f"**Messages:** {len(st.session_state.messages)}")