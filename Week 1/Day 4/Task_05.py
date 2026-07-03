# 5. Add a @classmethod to a Person class that works as an alternate constructor, e.g. Person.from_birth_year(name, year).

from datetime import date

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        return (f"Hi, I'm {self.name} and I am {self.age} years old.")

    @classmethod
    def from_birth_year(cls, name, birth_year):
        current_year = date.today().year
        calculated_age = current_year - birth_year
        return cls(name, calculated_age)

    @staticmethod
    def is_adult(age):
        return age >= 18

user1 = Person("Ali", 25)

user2 = Person.from_birth_year("Usman", 2004)

print(user2.introduce())         
print(Person.is_adult(user2.age)) 