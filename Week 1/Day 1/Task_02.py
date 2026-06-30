#2. Reverse a string without using slicing or a built-in reverse function.

s = input("Enter a string to reverse: ")

reversed_str = ""

for char in s:
    reversed_str = char + reversed_str 

print(reversed_str)
