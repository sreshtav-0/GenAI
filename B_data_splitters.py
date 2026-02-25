import os
import json

import requests

from pprint import pprint
from langchain_text_splitters import (
    CharacterTextSplitter,
    HTMLHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
    RecursiveJsonSplitter
)
import A_doc_loader as docs_loader

# A. RecursiveCharacter Text splitter
"""
This text splitter is recommended one for generic text. It is parameterized by a list of characters. It tries to split on them in order until chunks are small enough. The default list is ["\n\n", "\n", " ", ""].

This has the effect of trying to keep all paragraphs (and then sentences, and then words) together as long as possible, as those would generically seem to be having strong semantic meaning.
1. How the text would be split: By list of characters.
2. How the chunk size is measured: By number of characters.
"""

recursive_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
splitted_pdf_docs = recursive_splitter.split_documents(docs_loader.pdf_documents)
# pprint(splitted_pdf_docs[0])
# pprint(splitted_pdf_docs[1])

# B. On a simple text document
recursive_splitter2  = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=20)
splitted_text_docs = recursive_splitter2.split_documents(docs_loader.text_documents)
# pprint(splitted_text_docs[0])
# pprint(splitted_text_docs[1])
print("-------------------------------------------------------")

# B. Character Text Splitter 
"""
One of the simplest splitter. This splits based on a given character sequence, which defaults `\n\n`. Chunk length is measured by number of characters.
1. How the text is split: by single character separators.
2. How the chunk size is measured: by number of characters.
"""
character_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
splitted_text_docs2 = character_splitter.split_documents(docs_loader.text_documents)
# pprint(splitted_text_docs2[0])
# pprint(splitted_text_docs2[1])

print("-------------------------------------------------------")

# C. HTML Header Text Splitter
"""
HTMLHeaderTextSplitter is a "structure-aware" chunker that splits text at the HTML element level and adds metadata for header "relevant" to any given chunck. It can return chunk elements or combine elements with same metadata, with objective of
A.) Keeping related text grouped (more or less) semantically, and
B.) Preversing context-rich information encoded in document structures. It can be used with other text splitterss as a part of chunking pipelines.
"""

with open(os.path.join("documents", "sample.html"), mode="r", encoding="utf-8") as file:
    html_string = file.read()
# print(html_string)

headers_to_split_on = [
    ("h1", "Header 1"),
    ("h2", "Header 2"),
    ("h3", "Header 3"),
]

html_splitter = HTMLHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
splitted_html_docs = html_splitter.split_text(html_string)

# pprint(splitted_html_docs)

## II. Real Website Example 
url = "https://lilianweng.github.io/posts/2025-05-01-thinking/"

headers_to_split_on_2 = [
    ("h1", "Header 1"),
    ("h2", "Header 2"),
    ("h3", "Header 3"),
    ("h4", "Header 4")
]

web_html_splitter = HTMLHeaderTextSplitter(headers_to_split_on=headers_to_split_on_2)

splitted_web_html_docs = web_html_splitter.split_text_from_url(url)
# pprint(splitted_web_html_docs)

print("-------------------------------------------------------")
# D. RecursiveJSONSplitter 
"""
This JSON text splitter splits json data while allowing control over chunk size. It traverses json data depth first and builds json chunks.
It attempts to keep nested json objects whole but split them, if needed to keep between min_chunk_size and max_chunk_size/

If the value is not a nested json but rather a very larget string it will not be spitted. If you need a hard cap on the chunk-size consider composing this with a Recursive Text splitting on those chunks.
"""

with open(os.path.join("documents", "quiz.json"), mode = "r", encoding = "utf-8") as file:
    json_data = json.load(file)

json_splitter = RecursiveJsonSplitter(max_chunk_size = 50)
json_chunks = json_splitter.split_json(json_data)
docs = json_splitter.create_documents(text = [json_data])
texts_in_json = json.splitter.split_text(json_data)
pprint(texts_in_json)
