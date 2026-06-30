#6. Given a list of numbers, find the largest and smallest without using min()/max().

user_input = input("Enter numbers separated by spaces: ")

string_list = user_input.split()

numbers = []

for x in string_list:
    numbers.append(int(x))

if not numbers:
    print("The list is empty. No numbers were provided.")
else:
    smallest = numbers[0]
    largest = numbers[0]

    for num in numbers:
        if num < smallest:
            smallest = num
        elif num > largest:
            largest = num
            
    print(f"The given list: {numbers}")
    print(f"Smallest: {smallest}")
    print(f"Largest: {largest}")