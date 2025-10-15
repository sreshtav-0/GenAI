print("-" * 15, "STRING", "-" * 15)
"""
# Strings, Lists, Tuples, Dictionaries & Set
"""
string1 = "Hello"
string2 = "World"

# General Properties 
## I. Concatenation 
print(string1 + string2)

## II. Multiply by an Integer 
print(string1 * 5)

# Specific Properties 
## Indexing, Slicing & Stepping, Immutable 
string1 = "Hello"
# L-> R [0 -> n-1] 
# R-> L [-1 -> -n]
print(string1[0], string1[-5])
print(string1[1], string1[-4])
print(string1[2], string1[-3])
print(string1[3], string1[-2])
print(string1[4], string1[-1])

print("=" * 8)
## Slicing 
## [start index: end index + 1]
## The direction of slicing is left to right 
string3 = "Hello World!"

print()
## 1. Slicing from the beginning - "Hello"
print(string3[0:5])
print(string3[-12:-7])
print(string3[:5])
print(string3[:-7])

print()
## 2. Slicing in the between - "llo Wo"
print(string3[2:8])
print(string3[-10:-4])

print()
## 3. Slicing till the end - "World!"
print(string3[6:12])
print(string3[-6:0]) # Will not work
print(string3[6:])
print(string3[-6:])

print("=" * 8)
## Stepping  
print(string3[:])
print(string3[::1])
print(string3[::2])
print(string3[::3])

print()
print(string3[::-1])
print(string3[::-2])

print("=" * 8)
# .split(), .join()
string1 = "Hello to the World of Python!"
string2 = "Hello-to-the-World-of-Python!"

print(string1.split(" "))
print(string2.split("-"))

string_join = ['Hello', 'to', 'the', 'World', 'of', 'Python!']
print("".join(string_join))
print(" ".join(string_join))
print("-".join(string_join))