#1. Write a program to check whether a number is prime.

n = int(input("Enter a number to check if it is prime: "))

is_prime = True

if n <= 1:
    is_prime = False
else:
    # We only need to check up to the square root of n
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            is_prime = False
            break 

if is_prime:
    print(f"{n} is a prime number.")
else:
    print(f"{n} is not a prime number.")
