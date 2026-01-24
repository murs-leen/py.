

a = int(input("Enter number1: "))
b = int(input("Enter number2: "))
c = int(input("Enter number3: "))
d = int(input("Enter number4: "))

if(a >= b and a >= c and a >= d):
    print("a is largest", a)
elif(b >= c and b >= d):
    print("b is largest: ", b)
elif(c >= d):
    print("c is largest", c)
else:
    print("d is largest",d)

largest = max(a,b,c,d)