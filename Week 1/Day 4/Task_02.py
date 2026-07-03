#2. Create a BankAccount class with deposit() and withdraw() methods; prevent withdrawals beyond the balance.

class BankAccount:
    def __init__(self, owner, initial_balance=0):
        self.owner = owner
        self.balance = initial_balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return(f"Deposited Amount: Rs.{amount}. New Balance: Rs.{self.balance}")
        return("Invalid Deposit Amount")
    
    def withdraw(self, amount):
        if amount > self.balance:
            return("Transaction Denied: Insufficient Balance")
        elif amount > 0:
            self.balance -= amount
            return(f"Withdrew Amount: Rs.{amount}. Remaining Balance: Rs.{self.balance}")
        return("Invalid Withdrawal Amount")

wallet = BankAccount("Usman", 1000)
print(wallet.withdraw(1500))
print(wallet.deposit(200))
