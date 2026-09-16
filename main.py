"""
Voice RAG Agent - ElevenLabs Editions
=====================================
Pipeline:
    Microphone -> ElevenLabs Scribe (STT) -> LangChain agent + RAG -> ElevenLabs TTS + Speaker
Stack:
    STT: ElevenLabs Scribe (scribe_v1)
    Reasoning: gpt-5.6-luna via a LangChain tool-calling agent
    Retireval: FAISS vector store + OpenAI Embeddings 
    TSS: ElevenLabs (eleven_flash_v2_5 - low latency)
    UI: Gradio
Run:
    export OPENAI_API_KEY = "sk-..." # Stll needed: LLM + embeddings
    export ELEVENLABS_API_KEY = "..."
    python main.py
"""

import os
import tempfile
from typing import List

import gradio as gr
from elevenlabs.client import ElevenLabs
from openai import OpenAI

from langchain.agents import create_pbi_agent
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.tools.retriever import create_retriever_tool

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

missing = [k for k in ("OPENAI_API_KEY", "ELEVENLABS_API_KEY") if not os.getenv(k)]
if missing:
    raise SystemExit(f"Please set: {", ".join(missing)}")

LLM_MODEL = "gpt-5.6-luna"
EMBED_MODEL = "text-embedding-3-small"

STT_MODEL = "scribe_v1"
TTS_MODEL = "eleven_flash_v2_5"

VOICES = {
    "Rachel (calm, narration)": "21m00Tcm4TlvDq8ikWAM",
    "Adam (deep, confident)":   "pNInz6obpgDQGcFmaJgB",
    "George (warm, British)":   "JBFqnCBsd6RMkjVDRZzb",
    "Sarah (soft, friendly)":   "EXAVITQu4vr4xnSDxMaL",
}
DEFAULT_VOICE = "Rachel (calm, narration)"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 225
TOP_K = 4

SYSTEM_PROMPT = (
    "You are a helpful voice assistant that answers questions using the user's "
    "uploaded documents.\n\n"
    "Rules:\n"
    "- Always call the `search_documents` tool before answering a question about "
    "the documents.\n"
    "- Ground every answer in the retrieved text. If the answer is not in the "
    "documents, say so plainly instead of guessing.\n"
    "- Your reply will be read aloud, so keep it conversational and concise. Do "
    "not use markdown, bullet points, headings, or code blocks."
)

eleven = ElevenLabs(api_key = ELEVENLABS_API_KEY)

def transcribe(audio_path:str)->str:
    with open(audio_path, "rb") as audio_file
        result = eleven.speech_to_text.convert(
            file = audio_file,
            model_id = STT_MODEL
        )
    return result.text.strip()

def synthesize(text:str, voice_name:str=DEFAULT_VOICE)->str:
    voice_id = VOICES.get(voice_name, VOICES[DEFAULT_VOICE])
    audio_stream = eleven.text_to_speech.convert(
        voice_id = voice_id,
        model_id = TTS_MODEL
        output_format = "mp3_44100_128"
        text = text
    )
    fd, out_path = tempfile.mkstemp(suffix = ".mp3")
    os.close(fd)
    with open(out_path, "wb") as f:
        for chunk in audio_stream:
            if chunk:
                f.write(chunk)
    return out_path

class VoiceRAG_Agent:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model = EMBED_MODEL)
        self.llm = ChatOpenAI(model = LLM_MODE, temperature = 0)
        self.agent = None

    def build(self, file_paths:List[str])->str:
        documents = []
        for path in file_paths:
            loader = (PyPDFLoader(path) 
            if path.lower().endswith(".pdf") 
            else TextLoader(path, encoding="utf-8")    
        )
        documents.extend(loader.load())
        if not documents:
            raise ValueError("No readable content found in the uploaded files.")
        splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
        chunks = splitter.split_documents(documents)
        vector_store = FAISS.from_documents(chunks, self.embeddings)
        retriever = vector_store.as_retriever(search_kwargs={"k":TOP_K}) 

        retriever_tool = create_retriever_tool(
            retriever,
            name="search_documents",
            description=(
                "Searches the user's uploaded documents and returns the most"
                "relevant excerpts. Use this for every question about the documents."
            )
        )
        self.agent = create_agent(self.llm, [retriever_tool], system_prompt=SYSTEM_PROMPT)
        return f"Knowledge base ready - {len(chunks)} chunks from {len(file_paths)} file(s)."


def build_knowledge_base(files):
    if not files:
        return None, "Please upload at least one PDF or text file."
    paths = [f if isinstance(f, str) else f.name for f in files]
    agent = VoiceRAG_Agent()
    try:
        status = agent.build(paths)
    except Exception as exc:
        return None, f"Failed to build knowledge base: {exc}"

    return agent, status

def to_chatbot(history:List[BaseMessage]):
    return [
        {
            "role": "user" if isinstance(msg, HumanMessage) else "assistant",
            "content": msg.content
        }
        for msg in history
    ]

def handle_turn(audio_path, agent, history, voice_name):
    history = history or []

    if agent is None:
        gr.Warning("Build the knowledge base before asking a question.")
        return to_chatbot(history), None, history
    if audio_path is None:
        gr.Warning("No audio detected. Please record your question.")
        return to_chatbot(history), None, history

    question = transcribe(audio_path)

    if not question:
        gr.Warning("Could not understand the audio. Please try again.")
        return to_chatbot(history), None, history

    answer = agent.ask(question, history)
    audio_reply = synthesize(answer, voice_name)
    history = history + [HumanMessage(content=question), AIMessage(content=answer)]
    return to_chatbot(history), audio_reply, history

def clear_conversation():
    return [], None, []

def build_ui():
    with gr.Blocks(title = "Voice RAG Agent + ElevenLabs", theme=gr.themes.Soft()) as demo:
        gr.Markdown(
            "Voice RAG Agent - ElevenLabs Edition \n"
            "Upload your documents, then ask questions about them by voice"
        )
        agent_state = gr.State(None)
        history_state = gr.State([])

        with gr.Row():
            with gr.Column(scale = 1):
                gr.Markdown("### 1 * Build your knowledge")
                files = gr.File(
                    label = "Upload PDFs or text files",
                    file_count = "multiple",
                    file_type = [".pdf", ".txt", ".md"]
                )
                build_btn = gr.button("Build Knowledge Base", variant="primary")
                kb_status = gr.Markdown("No documents loaded yet.")
                voice = gr.Dropdown(
                    choices = list(VOICES.keys()),
                    value = DEFAULT_VOICE,
                    label = "Assistant Voice"
                )

            with gr.Column(scale = 2):
                gr.Markdown("### 2 * Talk to your documents.")
                chatbot = gr.Chatbot(type = "messages", height = 300, label = "Conversations")
                audio_in = gr.Audio(sources = ["microphone"], type = "filepath", label = "Record your question, then stop to send.")
                audio_out = gr.Audio(label = "Assistant Reply", type="filepath", autoplay = True)
                clear_btn = gr.Button("Clear Conversation")

        build_btn.click(build_knowledge_base, inputs = [files], outputs=[agent_state, kb_status])
        audio_in.stop_recording(handle_turn, inputs = [audio_in, agent_state, history_state, voice], outputs = [chatbot, audio_out, history_state])
        clear_btn.click(clear_conversation, outputs = [chatbot, audio_out, history_state])
        return demo

if __name__ == "__main__":
    build_ui().launch(debug = True)