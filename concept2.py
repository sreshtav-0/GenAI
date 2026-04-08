# Messages class and Manual Message History
import os

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise ValueError("The OPENAI API KEY is not set in your environment. Check your imports and .env file")

# Add to conversation history
messages = [
    SystemMessage("You're a helpful assistant. Assume the role of expert in field of mathematics to answer the asked questions."),
    HumanMessage("Can you help me with a problem?"),
    AIMessage("I'd be happy to help you with that question!"),
    HumanMessage("Great! What is factorial of 5?")
]

llm = ChatOpenAI(model="gpt-5-nano", temperature=0, api_key=SecretStr(OPENAI_API_KEY))

response = llm.invoke(messages)
print(response.text)