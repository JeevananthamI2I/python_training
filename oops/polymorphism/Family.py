class Parent:
    def show(self):
        print("This is the Parent class method.")

class Child(Parent):
    def show(self):
        print("This is the Child class method (Overwritten).")

parent_obj = Parent()
child_obj = Child()

parent_obj.show()  
child_obj.show() 



class Sample:
    def show(self, a=None, b=None):
        if a is not None and b is not None:
            print(f"Method with two arguments: {a}, {b}")
        elif a is not None:
            print(f"Method with one argument: {a}")
        else:
            print("Method with no arguments")

obj = Sample()

obj.show()       
obj.show(10)     
obj.show(10, 20)

