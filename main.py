import math
from datetime import date


class User:
    def __init__(self):
        self.name = 'giorgio'
        self.email = 'gior@mail.com'
        self.wealth = 200000


class Account:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount: int) -> None:
        self.balance += amount

    def withdraw(self, amount: int) -> int:
        self.balance -= amount
        return amount


class Expense:
    def __init__(self, amount: int, name: str,
                 category: str, description=''):
        self.amount = amount
        self.name = name
        self.description = description
        self.description = category
        self.created_at = str(date.today())


class Card:
    def __init__(self, balance=0):
        self.card_num = ''
        self.balance = balance
        self.exp_date = 0

    def spend(self, expense: Expense) -> None:
        self.balance -= expense.amount


class CreditCard(Card):
    pass


class DebitCard(Card):
    pass


class BankAccount(Account):
    def __init__(self, bank):
        super().__init__()
        self.acc_num = '0987898'
        self.spei_num = '1234567890'
        self.bank = bank

    main_card = DebitCard()


class Savings(Account):
    def __init__(self, rate, name, balance=0):
        super().__init__(balance)
        self.interest_rate = rate
        self.name = name

    def earnings(self, months):
        years = months/12
        cmp_int = 12
        ir = self.interest_rate/100
        return self.balance * ((math.pow((1 + (ir/cmp_int)), years * cmp_int)) - 1)


if __name__ == '__main__':
    ba = BankAccount('Bancomer')
    ba.deposit(1000)
    cheese = Expense(500, 'chis', 'food')
    cetes = Savings(11.1, 'cetes', 20000)
    print(cetes.earnings(24))
