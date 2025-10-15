# Sets 

## Properties- Unique Values, Unordered, Mutable 
a_set = {10, 10, 10, 20, 30, 30, 40, 40, 40, 40, 50}
b_set = {"apple", "apple", "banana", "banana", "mango", "mango", "pineapple", 
"guava", "watermelon"}

print(a_set)
print(b_set)
print("--------------------------------------")
## Set Methods 
### Group-I Adding values to a set 
### .add(value), .update(setB)
set_a = {10, 20, 30}
set_b = {"a", "b", "c"}

print("Set A Before: ", set_a)
for num in [10, 20, 30, 40, 50, 60]:
    set_a.add(num)

print("Set A After: ", set_a)

set_a.update(set_b)
print("Set A after update: ", set_a)

print("=================================================")
### Group-II Deleting values from set
### .pop(), .remove(value), .discard(value)

### .pop()- Deletes first value 
print("Set A before pop: ", set_a)
set_a.pop()
set_a.pop()
print("Set A after pop: ", set_a)

### .remove(value), .discard(value)
### .remove() will throw an error if a value is not found 
### .discard() will not throw an error if the value is not present
# set_a.remove(10)
# set_a.remove("d")-KeyError: 'd'
set_a.discard(50)
set_a.discard("d")

print("Set A after remove/discard: ", set_a)
print("=================================================")
### Group-III 
### .union(), .intersection()/.intersection_update(), 
### .difference()/.difference_update(), 
### .symmetric_difference()/.symmetric_difference_update()

set1 = {10, 20, 30, 40, 50}
set2 = {40, 50, 60, 70, 80}
### .union()
print("Union:", set1.union(set2))
### .interesection()
print("Intersection:", set1.intersection(set2)) 
### .difference()
diff_12 = set1.difference(set2)
diff_21 = set2.difference(set1)
print("Difference in Set1 w.r.t Set2", diff_12)
print("Difference in Set2 w.r.t Set1", diff_21)
### .symmetric_difference()
sym_diff = set1.symmetric_difference(set2)
print("Symmetric Difference", sym_diff)

print("=================================================")
### Group-IV 
### .isdisjoint(), .issubset(), .isuperset()

### .isdisjoint()- True if two set have no common element
set3 = {10, 20, 30}
set4 = {"a", "b", "c"}

print(set3.isdisjoint(set4))

### .issuperset(), .issubset()
set5 = {10, 20, 30, 40, 50, 60}
set6 = {10, 20, 30}

# set5 will be the superset of set6
print(set5.issuperset(set6))

# set6 will be the subset of set 5
print(set6.issubset(set5))

print("=================================================")
### Group-V 
### .copy()
set_copy = set_a
print(set_copy is set_a)

set_a_copy = set_a.copy()
print(set_a_copy is set_a)