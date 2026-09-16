import os
from pprint import pprint 
from langchain.chat_models import init_chat_model 
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

# Loading the Enivronment Variable
load_dotenv()

#ChatGPT 5.4 Nano Model Integration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    RuntimeError("OPENAI_API_KEY is not found in the .env file. Check your configurations again.")

chat_model = init_chat_model(model="gpt-5.4-nano") 
print(chat_model)
## Invoke this Model
response = chat_model.invoke("Where is The Lost Stadium of Magnesia?")
# pprint(response)

print(response.content)

print("------------------------------------------")

# Google Gemini Model Integration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    RuntimeError("GEMINI_API_KEY is not found in the .env file. Check your configurations again.")
# chat_model2 = init_chat_model("google_genai:gemini-3-flash-preview")
# response = chat_model2.invoke("What is 12 % 4 = ?")
# print(response.content)
gemini_model = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", google_api_key=GEMINI_API_KEY)
response = gemini_model.invoke("What is 12 % 4 = ?")
print(response.content)

print("------------------------------------------")

#Groq Model Integration
GROQ_API_KEY= os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    RuntimeError("GROQ_API_KEY is not found in the .env file. Check your configurations again.")
groq_model = init_chat_model("groq:qwen/qwen3-32b")
response = groq_model.invoke("Where is Bali located?")
print(response.content)