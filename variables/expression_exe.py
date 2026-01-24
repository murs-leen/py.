
# String operations

A,B,C = 2,3,None
Txt = "@"
print(A*Txt*B) # output: @@@@@@
print((str(A)+Txt)*B)  

# division -> float result

result = A/B
print("Float result:", result)

# division -> integer result

result = A//B
print("Integer result:",result)

#   result of %(operator) will same as of denominator
""" a % b = a − b * floor(a / b) comment :)""" 

x,y = -5,6
z = y % x
print ("z: ",z)