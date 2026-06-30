#3. Print the Fibonacci series up to n terms.

n = int(input("Enter the number of Fibonacci terms to print: "))

if n <= 0:
    print("Please enter a positive integer.")
else:
    a, b = 0, 1
    for _ in range(n):
        print(a, end=" ") 
        a, b = b, a + b