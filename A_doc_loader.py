# Chapter-1 Document Loaders 
import os
import bs4
from langchain_community.document_loaders import (
    ArxivLoader,
    CSVLoader,
    PyPDFLoader, 
    TextLoader,
    WebBaseLoader,
    WikipediaLoader
)
from pprint import pprint

## I. TextLoader 
speech_docs = os.path.join("documents", "speech.txt")
loader = TextLoader(speech_docs)
print(loader)

text_documents = loader.load()
# print(text_documents)

print("------------------------------------------------------")
## II. PyPDFLoader 
treasure_hunt_path = os.path.join("documents", "treasure_hunt.pdf")

pdf_loader = PyPDFLoader(treasure_hunt_path)
print(pdf_loader)

pdf_documents = pdf_loader.load()
#print(pdf_documents[:5])

print("-------------------------------------------------------")
## III. Web-Based Loader 

web_loader = WebBaseLoader(web_paths=(
    "https://lilianweng.github.io/posts/2025-05-01-thinking/",
    "https://lilianweng.github.io/posts/2024-11-28-reward-hacking/",
    "https://lilianweng.github.io/posts/2024-07-07-hallucination/"
))

web_info = web_loader.load()
# print(web_info)

## Extract relevant web content 
web_loader2 = WebBaseLoader(web_paths=(
    "https://lilianweng.github.io/posts/2025-05-01-thinking/",
    "https://lilianweng.github.io/posts/2024-11-28-reward-hacking/",
    "https://lilianweng.github.io/posts/2024-07-07-hallucination/"
), bs_kwargs=dict(parse_only=bs4.SoupStrainer(class_=("post-content",
"post-header"))))

web_info2 = web_loader2.load()
# print(web_info2)

print("-------------------------------------------------------")
# ArxivLoader 
arxiv_loader = ArxivLoader(query="1706.03762", load_max_docs=2).load()
#pprint(arxiv_loader)

print("-------------------------------------------------------")
# WikipediaLoader 
wiki_loader = WikipediaLoader(query="Albert Einstein", load_max_docs=2).load()
#pprint(wiki_loader)

print("-------------------------------------------------------")
# CSVLoader 
file_path1 = os.path.join("documents", "pokemon.csv")
csv_loader = CSVLoader(file_path=file_path1, encoding="utf-8")
print(csv_loader)

csv_documents = csv_loader.load()
#pprint(csv_documents)