
#   Lists in python
#   Lists are mutable unlike strings which are immutable

marks = [2,5,6,4,6,65]
list = [True,3.65,"hi",4,[3,5]]
marks[4] = 43
print(list)
print("len: ",len(list))
print(type(marks))

marks.append("new value")
marks.insert(6,"insertion")
marks.remove(4) #   take value to remove
marks.pop(1) #  take index 

print("updated list:",marks)

#   Slicing in lists

print(marks[1:4])

input().split()