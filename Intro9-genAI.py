# Iteration 
## Iteration-A cyclic process of repetition, where values and states can increase/descrease or may remain constant based on a condition. 
## Iterator- Iterator is something that is capable of running iterations.
## E.g For loop, while loop, map function, recursion
## Iterable- A iterable is something that is capable of providing continous values for iterations.

## The range class 
print(type(range))
# range(start limit, end limit + 1, step)
## 0-9
for i in range(0, 10):
    print(i, end=" ")

print()
## 1-10
for i in range(1, 11):
    print(i, end=" ")

print()
# Generate all odd numbers from 30<->60 [both inclusive]
for var in range(30, 61):
    if var % 2 != 0:
        print(var, end=" ")

print()
# Generate all odd numbers from 30<->60 [both inclusive]
for var in range(31, 61, 2):
    print(var, end=" ")

print()
# Generate all the multiples of 7 till 0-100 [inclusive]
for var in range(0, 101, 7):
    print(var, end=" ")

print()
# Using range for -ve numbers 
# Generate numbers from -10 to -1.
for var in range(-10, 0):
    print(var, end=" ")

print()
# Create a NASA-style counter for lauching SpaceX Rocket 
for var in range(10, -1, -1):
    print(var, end=" ")

print()
print("---------------------------------------------------")
# Running for loops -> Strings 
string = "Hello World!"

# Ist Way:- Running the for loop directly [Prefered]
for char in string:
    print(char, end=" ")

# IInd Way:- Using range function 
print()
for index in range(0, len(string)):
    print(string[index], end=" ")

## Illustration-1:- Convert the vowels of the string to upper case characters
string1 = "sreshtav"
result = ""

for char in string1:
    if char in "aeiou":
        result += char.upper()
    else:
        result += char

print("\nResult:", result)

## Illustration-2:- Reverse a string 
string = "Hello World!"
reverse = ""

for char in string:
    reverse = char + reverse

print(f"The reverse of the string {string} is {reverse}.")

## Illustration-3:- Find total words in a string 
string3 = "It's raining like cats and dogs."

# Ist Approach 
count = 1 if len(string3) else 0 

for char in string3:
    if char == " ":
        count += 1

print(f"The number of words in the string are: {count}")

# IInd Approach
string_list = string3.split()

print(f"The number of words in the string are: {len(string_list)}")

## Illustration-4:- Highlight the word `tiger` in the given paragraph
paragraph = "Tigers are the largest members of the cat family and are renowned for their power, grace, and striking appearance. With bold black stripes over a fiery orange coat, each tiger's pattern is as unique as a fingerprint. Native to Asia, they thrive in diverse habitats—from dense jungles to snowy forests. Tigers are solitary hunters, relying on stealth and strength to ambush prey like deer and wild boar. Sadly, their numbers have dwindled due to habitat loss and poaching, making conservation efforts critical. Despite their fierce reputation, tigers play a vital role in maintaining the balance of their ecosystems, symbolizing both beauty and strength in the wild."

para_list = paragraph.split()
highligted_text = ""

print(para_list[:5])

for word in para_list:
    if "tiger" in word.lower():
        highligted_text += " " + "\033[33;1m" + word + "\033[0;0m"
    else:
        highligted_text += " " + word

print("Highlighted Paragraph:", highligted_text, sep="\n")

print()
print("---------------------------------------------------")
# Running for loops for lists 

fruits_list = ["apple", "banana", "grape", "mango", "strawberry"]

## I. Way:- Direct Way- ❌ Cannot mutate the original list
for fruit in fruits_list:
    print(fruit, end=" ") 

print()
## II. Way:- Using the range function ✅ Can mutate the original list
for index in range(0, len(fruits_list)):
    print(fruits_list[index], end=" ")

print()
### III. Way:- Using the enumerate function ✅ Can mutate the original list
for index, value in enumerate(fruits_list):
    print(index, value)

print()
### IV. Way:- List Comprehensive 
fruits_list_upper = [fruit.upper() for fruit in  fruits_list]
print(fruits_list_upper)

## Illustration 1:-> 
## In the numbers list find the perfect square and convert the value in the original list as True and the else cases as False
nums_list = [12, 16, 21, 36, 45, 49, 54, 81]

print("Nums List:", nums_list)
### Ist Way:- Using Enumerate 
for index, num in enumerate(nums_list):
    sqrt = int(num ** 0.5) 
    if sqrt ** 2 == num:
        nums_list[index] = True
    else:
        nums_list[index] = False

print("Nums List Op:", nums_list)

print()
nums_list = [12, 16, 21, 36, 45, 49, 54, 81]
print("Nums List:", nums_list)
nums_list = [True if (int(num ** 0.5) ** 2) == num else False for num in nums_list]
print("Nums List Op:", nums_list)

## Illustration 2:-> Create a chess board using list comprehension
chess_board = [[(alpha, num) for alpha in "ABCDEFGH"] for num in range(8, 0, -1)]
for rows in chess_board:
    print(rows)

print("---------------------------------------------------")
# Running for loops for tuples

# Illustration 3:-> Find the highest and lowest marks from the marks tuple 

marks_tuple = (77, 87, 91, 93, 80, 88, 71)

high_marks = float("-inf")
low_marks = float("inf")

for marks in marks_tuple:
    if marks > high_marks:
        high_marks = marks
    if marks < low_marks:
        low_marks = marks

print(f"The highest marks are {high_marks} and the lowest marks are {low_marks}.") 
print(f"The highest marks are {max(marks_tuple)} and the lowest marks are {min(marks_tuple)}.")