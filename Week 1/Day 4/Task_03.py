#3. Demonstrate the difference between instance and class variables: track how many objects of a class have been created.

"""
DIFFERENCE BETWEEN INSTANCE AND CLASS VARIABLES:

1. Class Variables: 
    Shared globally by all objects of that class. 
    Defined directly inside the class, outside of any methods. 
    If you modify it using the class name, the change is reflected everywhere.

2. Instance Variables: 
    Completely unique to each specific object. 
    Defined inside the __init__ constructor using the 'self' keyword. 
    Changing an instance variable on one object has no effect on other objects.
"""

class UserAccount:
    total_accounts_created = 0 
    
    def __init__(self, username):
        self.username = username 
        
        UserAccount.total_accounts_created += 1

user1 = UserAccount("Usman")
user2 = UserAccount("Ahmad")

print(f"User 1: {user1.username}")
print(f"User 2: {user2.username}")
print(f"Total Accounts Created: {UserAccount.total_accounts_created}") 