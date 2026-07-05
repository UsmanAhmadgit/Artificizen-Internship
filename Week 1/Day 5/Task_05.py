#5. Implement __str__ and __repr__ for a Point(x, y) class so printing an instance gives readable output.

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point at ({self.x}, {self.y})"

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

p1 = Point(10, 25)

print(p1)       
print(repr(p1)) 