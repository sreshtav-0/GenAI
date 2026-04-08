# Basic LLM Invocation
import os

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import OpenAI
from pydantic import SecretStr
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise ValueError("The OPENAI API KEY is not set in your environment. Check your imports and .env file")

messages = [
    SystemMessage(content="You're helpful travel assistant?"),
    HumanMessage(content="What's likely be the weather today?")
]

llm = OpenAI(api_key=SecretStr(OPENAI_API_KEY))
response = llm.invoke(messages)
print(response)