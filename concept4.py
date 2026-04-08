# ChatPromptTemplate - For structured prompts + System & Human Message Template + 
# ... Multi-variable templates
import os 

from pydantic import SecretStr
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise ValueError("The OPENAI API KEY is not set in your environment. Check your imports and .env file")

# Create a chat prompt template with variable system message
prompt = ChatPromptTemplate.from_messages([(
    "system",
    "You're a professional English to {language} translator. Translate only in {language}."
), ("human", "{input}")])

# Initialize the LLM
llm = ChatOpenAI(model="gpt-5-nano", temperature=0, api_key=SecretStr(OPENAI_API_KEY))

output_parser = StrOutputParser()

# Create LCEL chain
chain = (prompt | llm | output_parser)

# Invoking the chain
english_prompt = "LLM's are one of the most powerful tools available today."

french_translation = chain.invoke({
    "input": english_prompt,
    "language": "French"
})
print("French:", french_translation)

japanese_translation = chain.invoke({
    "input": english_prompt,
    "language": "Japanese"
})
print("Japanese:", japanese_translation)