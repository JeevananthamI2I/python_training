#Siglelevel inheritance
class Animal:
    def __init__(self, name):
        self.name = name

    def make_sound(self):
        return "Some sound"

class Dog(Animal): 
    def make_sound(self):
        return "Bark!"

dog = Dog("Leo")
print(dog.name)         
print(dog.make_sound())

