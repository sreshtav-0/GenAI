import random
import timeit

# List and Tuples
fruit_list = ["apple", "banana", "mango", "pineapple"]
spares_tuple = ("Screw", "Bolts", "Nails", "Drill")

## I. General Property
### I. Concatenation
fruit_list += ["strawberry"]
spares_tuple += ("Screw-Driver",)

print("Fruit list after concatenation:", fruit_list)
print("Spares List after Concatenation:", spares_tuple)

print()
### II. Multiply by an Integer 
state_list = [True] * 10 
state_tuple = (False,) * 10
print(state_list)
print(state_tuple)

print("------------------------------------")
# II. Specific Properties
# Indexing, Slicing and Stepping 
print("List:")
print(fruit_list[0], fruit_list[-5])
print(fruit_list[1], fruit_list[-4])
print(fruit_list[2], fruit_list[-3])
print(fruit_list[3], fruit_list[-2])
print(fruit_list[4], fruit_list[-1])

print("Tuple:")
print(spares_tuple[0], spares_tuple[-5])
print(spares_tuple[1], spares_tuple[-4])
print(spares_tuple[2], spares_tuple[-3])
print(spares_tuple[3], spares_tuple[-2])
print(spares_tuple[4], spares_tuple[-1])

print("=" * 8)
# Slicing from the begining
## The direction of slicing is left to right 
## [lower index: upper index + 1]
fruit_list = ["apple", "banana", "mango", "pineapple", "strawberry"]

# Slicing from the beginning- ["apple", "banana", "mango"]
print(fruit_list[0:3])
print(fruit_list[-5:-2])
print(fruit_list[:3])
print(fruit_list[:-2])

print()
# Slicing in between- ["mango", "pineapple"]
print(fruit_list[2:4])
print(fruit_list[-3:-1])

print()
# Slicing till the end- ["mango", "pineapple", "strawberry"]
print(fruit_list[2:5])
print(fruit_list[2:])
print(fruit_list[-3:])  

print("=" * 8)
spares_tuple = ("Screw", "Bolts", "Nails", "Drill", "Screw-Driver")
print(spares_tuple[:])
print(spares_tuple[::1])
print(spares_tuple[::2])

print()
print(spares_tuple[::-1])
print(spares_tuple[::-2])

print("=" * 15)
# Mutability
print("List:")
fruit_list = ["apple", "banana", "mango", "pineapple", "strawberry"]

print("Fruit list before:", fruit_list)
fruit_list[0] = "apricot"
fruit_list[-1] = "watermelon"
fruit_list[1:4] = ["cherry", "grape", "dragonfruit"]
print("Fruit List After:", fruit_list)

print("------------------------------------")
# III. List & Tuple Functions 

## List:- 
# .append(), .insert()
fruit_list = ["apple", "banana", "mango", "pineapple", "strawberry"]
print("Fruit List before:", fruit_list)
fruit_list.append("blueberries")
fruit_list.append("watermelon")

# Add `guava` between blueberries and watermelon
fruit_list.insert(-1, "guava")
print("Fruit List after `append` and `insert`", fruit_list)

print()
# .pop()|.pop(index)  .remove(value)- Deletes the first occurence of the value
fruit_list.pop() # watermelon
fruit_list.pop() # guava 
fruit_list.pop(1) # Banana 

print("Fruit list after popping:", fruit_list, sep="\n")
fruit_list.remove("apple")
fruit_list.remove("strawberry")
print("Fruit list after remove:", fruit_list, sep="\n")

print()
# sorted()-In-built | .sort()-In-place
nums_list = [78, 45, 88, 92, 55, 32, 5]
fruit_list = ["apple", "banana", "mango", "pineapple", "strawberry"]
random.shuffle(fruit_list)

print("Original Nums List:", nums_list, sep="\n")
sorted_nums_list = sorted(nums_list)
print("Sorted Nums List:", sorted_nums_list, sep="\n")
reverse_sorted_nums_list = sorted(nums_list, reverse=True)
print("Reverse Sorted Nums List:", reverse_sorted_nums_list, sep="\n")

print()
print("Original fruit List:", fruit_list, sep="\n")
sorted_fruit_list = sorted(fruit_list)
print("Sorted  fruit List:", sorted_fruit_list, sep="\n")
reverse_sorted_fruit_list = sorted(fruit_list, reverse=True)
print("Reverse Sorted  fruit List:", reverse_sorted_fruit_list, sep="\n")

print("============")
nums_list.sort()
fruit_list.sort()

print("Sorted Original Nums List:", nums_list, sep="\n")
print("Sorted Original Fruit List:", fruit_list, sep="\n")

nums_list.sort(reverse=True)
fruit_list.sort(reverse=True)

print("Reverse Sorted Original Nums List:", nums_list, sep="\n")
print("Reverse Sorted Original Fruit List:", fruit_list, sep="\n")
print("============")
# key = function()
list_tuple = [(44, 27), (33, 36), (55, 18), (22, 45)]

# Sort the list based on
# I. Based on the 0-index 
print("0th-Index", sorted(list_tuple)) 

# II. Based on the 1st-index
print("Ist-Index", sorted(list_tuple, key=lambda x:x[1]))

# III. Based on sum of both the Indicies
print("Sum of both indicies", sorted(list_tuple, key=lambda x:sum(x)))

# IV. Based on  the base difference of both indicies
print("Difference of both indicies", sorted(list_tuple, key=lambda x:abs(x[0] - x[1])))

print()
# .count(value), .index(value, start_index, end_index)
spares_tuple = ("Nail", "Bolt", "Nail", "Nail", "Bolt", "Bolt", "Nail")

print("Counting the frequncy of `Nail`", spares_tuple.count("Nail"))
print("First Index:", spares_tuple.index("Nail"))
print("Second Index:", spares_tuple.index("Nail", 1, len(spares_tuple)))
print("Third Index:", spares_tuple.index("Nail", 3, len(spares_tuple)))
print("Forth Index", spares_tuple.index("Nail", 4, len(spares_tuple)))

print()
# .copy() to create a copy in memory for list 
fruit_list = ["apple", "banana", "mango", "pineapple", "strawberry"]

fruit_copy = fruit_list # ❌
fruit_copy = fruit_list.copy() # ✅

print(fruit_list is fruit_copy)
print("------------------------------------")
# Unpacking of tuples and list
subjects_tuple = ("Maths", "English", "French", "History", "Science")

var_1, var_2, var_3, var_4, var_5 = subjects_tuple
print(var_1, var_2, var_3, var_4, var_5)

maths, english, *other_subjects = subjects_tuple
print(maths, english)
print(other_subjects)

*other_subjects, history, science = subjects_tuple
print(history, science) 
print("------------------------------------")
# Speed Comparsion in List and Tuple
list_speed = timeit.timeit("x=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]", number=100_000_000)
tuple_speed = timeit.timeit("x=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)", number=100_000_000)

print(f"Time execution for List: {list_speed * 1000:.2f} ms")
print(f"Time execution for Tuple: {tuple_speed * 1000:.2f} ms")