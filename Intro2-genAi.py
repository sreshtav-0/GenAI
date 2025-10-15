import copy

# Operators in Python
## 1. Arithematic Operators (+, -, *, /, //, %, **)
## 2. Comparsion Operators (==, != , > , >=, <, <=)
## 3. Logical Operators (and, or, not)
## 4. Membership Operation (in)
## 5. Identity Operator (is)
## 6. Assignment Operator (=, +=, -=, *=, /=, //=, %=, **=)
## 7. Bitwise Operators 
"""
& - Bitwise AND
| - Bitwise OR
^ - Bitwise XOR
~ - Bitwise NO
<< - Shift Left
>> - Shift Right
"""

# Membership Operator- in 
string = "Can canner can't can as can as canner can can."

search = "as can"

if search in string:
    print(f"`{search}` is the part of the string.")
else:
    print(f"`{search}` is not the part of the string.")

print()

fruit_list = ["apple", "banana", "mango", "pineapple", "watermelon"]

fruit = "strawberry"

if fruit in fruit_list:
    print(f"`{fruit}` is the part of the fruit list.")
else:
    print(f"`{fruit}` is not the part of the fruit list.")

print()

fruits_dict = {"apple":20, "banana":10, "mango":50, "pineapple": 10, "watermelon": 3}

if fruit in fruits_dict:
    print(f"{fruit} is the part of the dictionary with value {fruits_dict[fruit]}.")
else:
    print(f"{fruit} is not the part of the dictionary.")

print("--------------------------------------------------")
# Identity Operator- is [check if two things share same memory location]

# Immutable - Stack Memory
a_num = 120
b_num = 120 
print(a_num is b_num)
print(id(a_num), id(b_num))

a_string = "Hello"
b_string = "Hello"
print(a_string is b_string)

a_string += " " + "World"
print(a_string is b_string)

print()
# Call by Reference- [list, dictionary, sets]
a_list = ["andre", "brian", "Eshwar"]
b_list = ["andre", "brian", "Eshwar"]

print(a_list is b_list)

copy_list = a_list
print(a_list is copy_list)

a_list.append("fiona")
a_list.append("girish")

copy_list.pop(0)
copy_list.pop(0)

print(f"{a_list=}\n{copy_list=}")

print("==========================")
a_list = ["andre", "brian", "Eshwar"]

# Ist Way:-All the three mutable datatype have copy function
# copy_list = a_list.copy() 

# IInd Way:- Creating a shallow copy
copy_list = copy.copy(a_list)

a_list.append("fiona")
a_list.append("girish")

copy_list.pop(0)
copy_list.pop(0)

print(f"{a_list=}\n{copy_list=}")

# Case where shallow copy will fail
stu_grades = [
    ["A+", "A", "B", "A+"],
    ["A", "B", "A+", "B"],
    ["A+", "B+", "A", "A"]]

stu_grades_copy = copy.copy(stu_grades)

stu_grades[0][0] = "A+"
stu_grades[0][1] = "A+"
stu_grades[0][2] = "A+"
stu_grades[0][3] = "A+"

print(f"{stu_grades}", f"{stu_grades_copy}", sep="\n")

print()
# Case where shallow copy will fail
stu_grades = [
    ["A+", "A", "B", "A+"],
    ["A", "B", "A+", "B"],
    ["A+", "B+", "A", "A"]]

stu_grades_copy = copy.deepcopy(stu_grades)

stu_grades[0][0] = "A+"
stu_grades[0][1] = "A+"
stu_grades[0][2] = "A+"
stu_grades[0][3] = "A+"

print(f"{stu_grades}", f"{stu_grades_copy}", sep="\n")
print("--------------------------------------------------")
a_num = 12
b_num = 15

print(a_num & b_num)
print(a_num | b_num)