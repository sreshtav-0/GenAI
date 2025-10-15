# Functions 
"""
1. DRY (Don't Repeat Yourself)
* If a piece of code is repeating itself, we wrap our code inside of a function, then we call.
2. It helps in containing errors and keeping code modular.
"""
'''
for i, val in range(0, 10):
    print("Hello World!")

print()
for j in range(0, 12):
    print("Goodbye Again!")

print()
for k in range(0, 15):
    print("Hello World Again!")
'''
# Part-I Creating a function
## limit and message are the parameters
def first_function(limit:int, message:str="Hello World")->None:
    for i in range(0, limit):
        print(message)

# Part-II Calling the function
first_function(limit=10) # 10 & "Hello World" are the arguments

print()
first_function(12, "Goodbye World!") # 12 & "Goodbye World" are the arguments

print()
first_function(15, "Hello World Again!") # 15 & "Hello World Again!" are the arguments

print("-----------------------------------------------------------")
def addition(a:int|float, b:int|float, c:int|float):
    print("a:", a, "b:", b, "c:", c)
    print("Sum:", a + b + c)

# Positional Arguments Passing 
addition(10, 20, 30)

# Keyword Argument Passing 
addition(a=10, b=20, c=30)
addition(c=30, b=20, a=10)
addition(b=20, a=10, c=30)

print()
# Mixed Argument Passing
# Positional argument should come first followed by keyword arguments 
addition(10, b=20, c=30)
addition(10, c=30, b=20)

# addition(a=10, b=20, 30)- SyntaxError: positional argument follows keyword argument