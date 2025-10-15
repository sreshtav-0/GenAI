"""
Python:-
1. Intrepreted Language
2. High Level:- Focus on logic rather than memory management 
3. Object-Oriented and Functional 
4. Dynamic Typing 
5. Large Standard libraries:- Comprehensive
"""
a = "🌍"
print("Hello World", a)
b = "👋"
print("Goodbye World", b)

# print function
## sep, end & file arguments 

### sep - separation
print("Hello to the World of Python!", sep="(*__*)")
print("Hello", "to", "the", "World", "of", "Python!", sep="(*__*)")

print()
print("Hello to the World of Python!", sep="-")
print("Hello", "to", "the", "World", "of", "Python!", sep="-") 

### end - argument- Anchorage of next, character/characters at end
print()
print("This is line no. 1")
print("This is line no. 2")

print()
print("This is line no. 1", end="! ")
print("This is line no. 2")

print()
for row in range(0, 5):
    for col in range(0, row+1):
        print("*", end=" ")
    print()

### file arguments- Writing something in a file
with open("sample.txt", mode="w") as f:
    print("Hello to the file!", file=f) 

print("--------------------------------------------")
# input()- Ask for user input - str 

name = "Alex" #input("Hello may I know your name: ") or "Shawn"
print(f"Nice to meet you {name}.") 

## Type Conversion/Casting- int(), float(), str()

### int()- Helps converting a float/string value to an integer
a_float = 2.999999
a_string = "45"
b_string = "9.81824"

float_to_integer = int(a_float)
print(float_to_integer, type(float_to_integer)) 

string_to_integer1 = int(a_string)
print(string_to_integer1, type(string_to_integer1))

string_to_integer2 = int(float(b_string))
print(string_to_integer2, type(string_to_integer2))

print()
### float()- Helps converting a int/string value to a float
an_integer = -78

int_to_float = float(78)
print(int_to_float, type(int_to_float))

str_to_float1 = float(a_string)
print(str_to_float1, type(str_to_float1))

str_to_float2 = float(b_string)
print(str_to_float2, type(str_to_float2))

print()
### str()- Helps converting int/float to a string
int_to_str = str(an_integer)
print(int_to_str, type(int_to_str))

float_to_str = str(a_float)
print(float_to_str, type(float_to_str))

print("--------------------------------------------")
# Literal in python 
var1 = 5
var2 = 3.141
var3 = "Hello World!🌍"
var4 = True 
var5 = None
var6 = b"Hello World!"

print(var1, type(var1))
print(var2, type(var2))
print(var3, type(var3))
print(var4, type(var4))
print(var5, type(var5))
print(var6, type(var6))

print("=================================")
## Data-Types
a_list = [10, 20, 30, "Hello! there"]

a_tuple = (88, 92, 85, 90)

a_dict = {1:"1", 1.01:"2", False:"3", "1":"4", (1,):"5"}

a_set = {10, 20, 30, 10, 20, 30, 10, 20, 30}

print("List:", a_list, "Tuple:", a_tuple, "Dictionary:", a_dict, "Set:", a_set, sep="\n")
