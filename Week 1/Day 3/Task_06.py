#6. Write a function with a default argument, and add a comment explaining why mutable default arguments (like a list) are risky in Python.

def create_account(email, role="user"):
    return f"Account created for {email} with role: {role}"

print(create_account("usman@gmail.com"))


"""
EXPLANATION: Why mutable default arguments (like a list) are risky in python.

In Python, default arguments are created exactly once when the function is first 
defined, not every time the function is called. If you use a mutable object 
(like a list or dictionary), that exact same memory address is shared by every 
single function call that relies on the default. Modifying it for one user would permanently 
change the default for everyone else.

WRONG WAY CODE EXAMPLE:

def add_to_cart(item, cart=[]): 
    cart.append(item)
    return cart

 USER 1 adds a Speaker
print(add_to_cart("Speaker"))  
 Output: ['Speaker']

 USER 2 adds a Laptop, but accidentally gets User 1's Speaker too.
print(add_to_cart("Laptop")) 
 Output: ['Speaker', 'Laptop'] 
"""