
#   Tuples are immutable
tuple = (5,)

#   tuple = (1) this will consider integer not tuple

tuple = (1,2,3,4,True)
print(tuple)

list = list(tuple) #    now i can modify it
print(list)