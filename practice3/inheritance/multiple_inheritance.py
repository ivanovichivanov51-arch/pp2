class Father:
    def skills(self):
        print("Gardening")

class Mother:
    def talents(self):
        print("Cooking")

class Child(Father, Mother):
    pass

c = Child()
c.skills()
c.talents()

class A:
    def show(self):
        print("Class A")

class B:
    def show(self):
        print("Class B")

class C(A, B):
    pass

obj = C()
obj.show()