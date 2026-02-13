class Student:
    def __init__(self, name, age):
        self.name = name      # instance variable
        self.age = age        # instance variable

s1 = Student("Ali", 20)
s2 = Student("Aruzhan", 22)

print(s1.name)  # Ali
print(s2.name)  # Aruzhan