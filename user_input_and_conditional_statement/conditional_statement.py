
 #  Conditional Statments

light = "red"
if (light == "red"):
    print("stop")
elif (light == "yellow"):
    print("ready")
elif (light == "green"):
    print("go")
else: print("light is broken")

#   Ternery Operator

food = input("food: ")
eat = "Yes" if food == "cake" else "no"
print(eat)

 #  <st1> if <condition> else <st2>

print("sweet") if food == "cake" or food == "jalebi" else print("not sweet")

#   Clever if <var> = (false,true) [<condition>]

salary = 50000
tax = salary *(0.1,0.2) [salary > 50000]