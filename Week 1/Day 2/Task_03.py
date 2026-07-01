#3. Find duplicate elements in a list using a set.

numbers = [10, 25, 10, 3, 40, 25, 50, 3, 10]

seen = set()
duplicates = set()

for num in numbers:
    if num in seen:
        duplicates.add(num)
    else:
        seen.add(num)

print(f"Original list: {numbers}")
print(f"Duplicate elements: {list(duplicates)}")
