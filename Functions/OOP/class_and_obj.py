

#   procedural -> functional -> Object Oriented Programming

class Student:
    
    #   class variable

    def __init__(self,name,sub1,sub2,sub3):
        self.name = name #  instance varible
        self.sub1 = sub1
        self.sub2 = sub2
        self.sub3 = sub3


    def avg(self):
        return (self.sub1 + self.sub2 + self.sub3) / 3
    

    def display(self):
        print(f"Name: {self.name}")
        print(f"Avg: {self.avg()}")


std1 = Student("arooj",70,67,45)
std1.display()