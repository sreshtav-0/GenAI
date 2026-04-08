# First LCEL Chain
import os

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise ValueError("The OPENAI API KEY is not set in your environment. Check your imports and .env file")

prompt = PromptTemplate.from_template("Tell me a joke about {topic}")

llm = ChatOpenAI(model="gpt-5-nano", api_key=SecretStr(OPENAI_API_KEY))

output_parser = StrOutputParser()

# Langchain Expression
chain = prompt | llm | output_parser

# Invoke It
result1 = chain.invoke({"topic": "programming"})
print(result1)

result2 = chain.invoke({"topic": "sponge bob square pants"})
print(result2)

result3 = chain.invoke({"topic": "politics"})
print(result3)