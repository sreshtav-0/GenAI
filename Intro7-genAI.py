# Dictionaries 
"""
Properties:- 
1. Key:value (separated by :), 
2. Key should be unique and immutable(int, float, string, tuple)
3. Values can be anything 
4. Dictionaries are ordered
5. Dictionaries are mutable
"""
# I. Key-Value Pair 
a_dict = {
    "name": "Alex Smith", 
    "age": 19, 
    "profession": ["student", "blogger", "content creator"]
}

# II. Dictionary Methods
# Group-I:- .keys(), .values(), .items()
a_dict["mail"] = "alexsmith@gmail.com"
a_dict["blood type"] = "A+ve"

# .keys()
print("Extracting keys of the dictionary:", a_dict.keys(), sep="\n")

# .values()
print("Extracting values of the dictionary:", a_dict.values(), sep="\n")

# .items()- Tuple(key, value)
print("Extracting key-value pair of the dictionary:", a_dict.items(), sep="\n")

print("=================================================")
# Group-II .setdefault(), .update(), .fromkeys()
# .setdefault()
subject_dict = {"physics": "A+", "maths": "A++", "chemistry": "B"}

print("Subject dict before:", subject_dict, sep="\n")
subject_dict.setdefault("physics", "B++")
subject_dict.setdefault("maths", "A+")
subject_dict.setdefault("english", "B+")
print("Subject dict after:", subject_dict, sep="\n")

# .update()
subject_dictII = {"physical sessions": "A++", "cultural activity": "B+"}
subject_dict.update(subject_dictII)

print("Updated subject dict:", subject_dict, sep="\n")

print()
fruits_list = ["apple", "banana", "mango", "orange", "pineapple"]

fruit_dict1 = dict.fromkeys(fruits_list)
print(fruit_dict1)

fruit_dict2 = dict.fromkeys(fruits_list, "To be added")
print(fruit_dict2)
print("==============================================================")
# Group-III Deletion Group
# .pop(key), .popitem()-Last key-value pair

print("Subject dict:", subject_dict, sep="\n")
subject_dict.popitem() # "cultural activity"
subject_dict.popitem() # "physical sessions"

print("Subject dict after popitem:", subject_dict, sep="\n")

subject_dict.pop("maths")
subject_dict.pop("chemistry")

print("Subject dict after popping `maths` & `chemistry`:", subject_dict, sep="\n")
print("==============================================================")
# Group-IV Check if a key exists or not
# .get()
subject_dict = {"physics": "A+", "maths": "A++", "chemistry": "B"}

print(subject_dict.get("physics")) # "A+"
print(subject_dict.get("maths")) # "A++"
print(subject_dict.get("history")) # None 
print(subject_dict.get("history", "Sorry key does'nt exist")) 

print("==============================================================")
# .copy() to create a copy in memory for list 
fruit_dict = {"apple":40, "banana":20, "mango":10, "pineapple":5, "strawberry":200}

fruit_dict_copy = fruit_dict # ❌
fruit_dict_copy = fruit_dict.copy() # ✅
print(fruit_dict is fruit_dict_copy)