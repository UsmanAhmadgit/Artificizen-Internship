#2. Use map() and a lambda to square every number in a list.

numbers = [1,2,3,4,5]
squared_numbers = list(map(lambda x : x**2, numbers))
print(squared_numbers)