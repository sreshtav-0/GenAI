# Embeddings:- Helps to convert words into vectors
import os
from pprint import pprint
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from pydantic import SecretStr
load_dotenv()
# I. OpenAI Embeddings
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    api_key=SecretStr(os.environ["OPENAI_API_KEY"])
)
# pprint(embeddings)
text = "This is a sessions on Langchain, embeddings and RAG"
query_result = embeddings.embed_query(text)
pprint(len(query_result))
embeddings_1024 = OpenAIEmbeddings(model="text-embedding-3-large", api_key=SecretStr(os.environ["OPENAI_API_KEY"]), dimensions=1024)
query_result_1024 = embeddings_1024.embed_query(text)
pprint(len(query_result_1024))

print("-------------------------------------------------------")
# II. Gemini's Embedding
gemini_embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=SecretStr(os.environ["GEMINI_API_KEY"]))
text = "This is a sessions on Langchain, embeddings and RAG"
query_result = gemini_embeddings.embed_query(text)
pprint(len(query_result))

print("-------------------------------------------------------")
# III. Hugging Face Embeddings
