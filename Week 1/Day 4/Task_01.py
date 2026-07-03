#1. Create a Car class with attributes (brand, model, year) and a method that displays the car’s info.

class Car:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year

    def display_info(self):
        return(f"Car's Information: {self.brand} {self.model} {self.year}")

car1 = Car("Toyota", "Corolla", "2022")
car2 = Car("Porsche", "911", "2026")

print(car1.display_info())
print(car2.display_info())