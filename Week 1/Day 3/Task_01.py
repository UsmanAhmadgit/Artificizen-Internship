#1. Write a function that accepts any number of arguments and returns their sum (use *args).

def calculate_sum(*args):
    return sum(args)

print (calculate_sum(5,10,20))
