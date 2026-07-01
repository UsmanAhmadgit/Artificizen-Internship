#1. Use a list comprehension to extract all even numbers from a list in one line.

numbers = [12, 5, 7, 22, 19, 104, 3, 8]

even_numbers = [num for num in numbers if num % 2 == 0]

print(f"Original list: {numbers}")
print(f"Even numbers:  {even_numbers}")