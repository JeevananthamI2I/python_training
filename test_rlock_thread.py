import threading

rlock = threading.RLock()

class BankAccount:
    def __init__(self):
        self.balance = 1000

    def deposit(self, amount):
        with rlock:
            print(f"Depositing {amount}...")
            self.balance += amount
            self.show_balance()

    def withdraw(self, amount):
        with rlock:
            if self.balance >= amount:
                print(f"Withdrawing {amount}...")
                self.balance -= amount
                self.show_balance()
            else:
                print("Insufficient funds!")

    def show_balance(self):
        with rlock:  
            print(f"Current Balance: {self.balance}")

account = BankAccount()

t1 = threading.Thread(target=account.deposit, args=(500,))
t2 = threading.Thread(target=account.withdraw, args=(200,))

t1.start()
t2.start()

t1.join()
t2.join()
