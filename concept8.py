# Concept-8 Testing Chatbot Memory
import os 

from pydantic import SecretStr
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    trim_messages
)
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise ValueError("The OPENAI API KEY is not set in your environment. Check your imports and .env file")

# Initialize LLM
llm = ChatOpenAI(model="gpt-5-nano", temperature=0.2, 
    api_key=SecretStr(OPENAI_API_KEY))

trimmer = trim_messages(
    max_tokens=30,
    strategy="last",
    token_counter=llm,
    allow_partial=True,
    start_on="human"
)

messages = [
    SystemMessage(content="You're a helpful assistant. Be concise."),
    HumanMessage(content="Hi, my name is Sam Altman"),
    AIMessage(content="Hello, Mr. Altman"),
    HumanMessage(content="I like vanilla Ice-cream"),
    AIMessage(content="Good for you!"),
    HumanMessage(content="What's my name?"),
    AIMessage(content="Your name is Sam Altman!"),
    HumanMessage(content="Thanks!"),
    AIMessage(content="You're welcomed. Let me know if any other queries if have.")
]

trimmed_chat = trimmer.invoke(messages)
print(trimmed_chat)