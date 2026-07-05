#2. Define a custom exception InsufficientBalanceError and raise it inside the BankAccount class from Day 4.

class InsufficientBalanceError(Exception):
    pass

class BankAccount:
    def __init__(self, balance):
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientBalanceError(f"Attempted {amount}, but balance is only {self.balance}")
        self.balance -= amount
        return self.balance

wallet = BankAccount(100)

try:
    wallet.withdraw(500)
except InsufficientBalanceError as e:
    print(f"Transaction Blocked: {e}") 
