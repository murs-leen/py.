
#   Sets
#   sets are mutable;(elms are immutable) and unordered (no indices)
#   duplicates are not allowed

nums = {1,2,2,3,"hello"}
emptySet = set () #  empty set
emptySet.add(1)
emptySet.add(2)
emptySet.add((1,2,3))
print(emptySet)
emptySet.remove(1)
print(nums)
print(type(nums))

set1 = {1,2,3}  
set2 = {3,4,5}
print("Union:", set1.union(set2))
print("Intersection: ", set1.intersection(set2))