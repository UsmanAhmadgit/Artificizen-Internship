#5. Check if a given string is a palindrome.

s = input("Enter a string to check if it is a palindrome: ")

cleaned_s = ""
for char in s:
    if char.isalnum():         
        cleaned_s += char.lower()

if cleaned_s == cleaned_s[::-1]:
    print("It is a palindrome!")
else:
    print("Not a palindrome.")
