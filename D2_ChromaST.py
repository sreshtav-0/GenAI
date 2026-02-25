import os
import streamlit as st

from D1_ChromaDB import chromadb

from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title = "PDF Q&A Assistant"
    layout = "centered"
)

if "pdf_chat" not in st.session_state:
    st.session_state.pdf_chat = None
if "document_loaded" not in st.session_state:
    st.session_state.document_loaded = None
if chat_history not in st.session_state:
    st.session_state.chat_history = []

def initialize_pdf_taller():
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            st.error("Google Gemini API Key not found in the environment variable")
            st.stop()
        
        pdf_conversation = ChromaRAG(gemini_api_key = api_key)
        return pdf_conversation
    except Exception as e:
        st.error(f"Error initializing the system: {str(e)}")
        st.stop()

def load_pdf(upload_file):
    try:
        with st.spinner("Processing PDF"):
            pdf_bytes = upload_file.read()
            num_chunks = st.session_state.pdf_chat.load_pdf_from_bytes(
                pdf_bytes,
                filename = upload_file.name
            )
            st.session_state.document_loaded = True
            st.session_state.chat_history = []
            return num_chunks
    except Exception as e:
            st.error(f"Error loading PDF {str(e)}")
            return None

def main():
    st.markdown("Upload a PDF and ask questions about the contents.")

    if st.session_state.pdf_chat is None:
        st.session_state.pdf_chat = initialize_pdf_taller()

    with st.sidebar:
        st.header("Upload PDF")
        upload_file = st.file_uploader("Choose a PDF file", type="pdf", help="Upload a PDF document for analysis")

        if upload_file is not None:
            if st.button("Process PDF", type="primary"):
                num_chunks = load_pdf(upload_file)
                if num_chunks:
                    st.success(f"PDF processed! Created {num_chunks} text chunks.")
                    st.rerun()
        if st.session_state.document_loaded:
            st.markdown("...")
            st.subheader("Document Information")
            doc_info = st.session_state.pdf_chat.get_document_info()
            st.write(f"Document: {doc_info['document']}")
            st.write(f"Chunks: {doc_info['chunks']}")
            st.write(f"Vector DB: {doc_info['chromadb_info']['collection_count']} docs.")

    if not st.session_state.document_loaded:
        st.info("Please upload and process a PDF to start asking questions.")
        st.markdown("""
        **How to use.**
        1. Upload a PDF file using the sidebar.
        2. Click "Process PDF" for document analysis.
        3. Ask your questions about the contents in the chat below.                
""")
    else:
        st.subheader("Ask Questions")    