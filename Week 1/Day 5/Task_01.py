#1. Create a base class Animal with a speak() method, and Dog/Cat subclasses that override it.

class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "(Generic animal sound)"

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)

    def speak(self):
        return f"{self.name} says Woof!"

class Cat(Animal):
    def speak(self):
        return f"{self.name} says Meow!"

dog = Dog("Rex", "German Shepherd")
cat = Cat("Luna")

print(dog.speak()) 
print(cat.speak()) 