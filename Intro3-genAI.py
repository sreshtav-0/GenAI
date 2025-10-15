# I/O Operations 
import json
import sqlite3
from pprint import pprint
## 1. File-based operations
### Standard operations on file
# 1. Read-r Helps to read a file
# 2. Write-w Helps to write into a file
# 3. Append-a Helps to add more content in a file 

### Reading a file
## with- Context Manager
original_data = """If you can imagine a furry humanoid seven feet tall, with the face of an intelligent gorilla and the braincase of a man, you'll have a rough idea of what they looked like -- except for their teeth. The canines would have fitted better in the face of a tiger, and showed at the corners of their wide, thin-lipped mouths, giving them an expression of ferocity.
Sometimes it's the first moment of the day that catches you off guard. That's what Wendy was thinking. She opened her window to see fire engines screeching down the street. While this wasn't something completely unheard of, it also wasn't normal. It was a sure sign of what was going to happen that day. She could feel it in her bones and it wasn't the way she wanted the day to begin.
"""

with open("sample.txt", mode="r") as f:
    content = f.read()

print(content, type(content))

with open("sample.txt", mode="r") as f:
    content = f.readlines() # List of strings (Each string represent one line)

print(content, type(content))

some_data = "Although Scott said it didn't matter to him, he knew deep inside that it did. They had been friends as long as he could remember and not once had he had to protest that something Joe apologized for doing didn't really matter. Scott stuck to his lie and insisted again and again that everything was fine as Joe continued to apologize. Scott already knew that despite his words accepting the apologies that their friendship would never be the same."

### write operation
with open("another_sample.txt", mode="w") as f:
    content = f.write(some_data + "\n") 

### Append operation
with open("sample.txt", mode="a") as f:
    content = f.write(original_data + "\n") 

print("---------------------------------------------------------")

## Binary IO
### Reading 
with open("planet.png", "rb") as f:
    content = f.read()

with open("planet3.png", "wb") as f:
    f.write(content)

## JSON File - {Javascript Object Notation}
data = {"name":"Alex Smith", "age":21, "hobbies":["photography", "blogging"]}

### I. How to write a JSON File
with open("data.json", mode="w") as file:
    content = json.dump(data, file, sort_keys=True, indent=4)

### II. Reading a JSON File 
with open("country_info.json", mode="r") as file:
    content = json.load(file)

pprint(content)
