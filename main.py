from __future__ import annotations
from math import pow
from datetime import date, timedelta
from dataclasses import dataclass, field
from typing import List
import sqlite3

con = sqlite3.connect('extracker.db')
cur = con.cursor()

def init_db():
    with open('schema.sql') as f:
        cur.executescript(f.read())

def create_exp():
    cur.execute('''
        INSERT INTO expenses
        (amount, name, category, length, description)
        VALUES (700, 'taboo', 'food', 1, 'tea')
        ''')
    con.commit()

def find_many():
    return cur.execute('''
        SELECT *
        FROM expenses
        ''').fetchone()
# init_db()
# create_exp()
# res = find_many()
# print(res[2])
con.close()

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


@dataclass
class Expense:
    amount: float
    name: str
    category: str
    pay_date: date
    description: str
    spend_date: date = date.today()
    length: int = 1

@dataclass
class Item:
        name: str
        total_amount: float
        length: int
        amount_left: float
        amount_month: float

@dataclass
class Month:
        name: str
        items: List[Item] = field(default_factory=list)
        expenses: List[Expense] = field(default_factory=list)
        debt: float = 0


class Card:
    def __init__(self, balance=0):
        self.card_num = ''
        self.balance = balance
        self.exp_date = 0

    def spend(self, expense: Expense) -> None:
        self.balance -= expense.amount


class CreditCard:
    def __init__(self, cut:int, expiration: int, balance: float, rate: float):
        self.cut = cut
        self.expiration = expiration
        self.balance = balance
        self.rate = rate
        self.debt = 0
        self.expenses = []
        self.paytime = timedelta(days=20)
        self.months = [
            Month('january'),
            Month('february'),
            Month('march'),
            Month('april'),
            Month('may'),
            Month('june'),
            Month('july'),
            Month('august'),
            Month('October'),
        ]

    def spend(self, amount: float, name: str, category:str, description='', sd=date.today()):
        self.balance -= amount

        if sd.day > self.cut:
            if sd.month == 12:
                pay_date = sd.replace(year=sd.year + 1, month=1, day=self.cut) + self.paytime
            else:
                pay_date = sd.replace(month=sd.month + 1, day=self.cut) + self.paytime
        else:
            pay_date = sd.replace(day=self.cut) + self.paytime

        self.expenses.append(Expense(amount, name, category, pay_date, description))


    def deposit(self, amount):
        self.balance += amount


    def history_ex(self, months):
        res = filter(lambda exp: exp.pay_date.month in months, self.expenses)
        for exp in res:
            print(exp)

    def add_msi(self, exp: Expense) -> None:
        i = date.today().month
        amount_paid = 0
        for it in range(exp.length):
            amount_month = exp.amount / exp.length
            amount_paid += amount_month
            amount_left = exp.amount - amount_paid
            self.months[i].debt += amount_month
            msi_item = Item(exp.name, exp.amount,
                            exp.length, amount_left,
                            amount_month)
            self.months[i].items.append(msi_item)
            i += 1

    def history(self) -> None:
        for exp in self.months[date.today().month].expenses:
            print(vars(exp))


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
        years = months / 12
        cmp_int = 12
        ir = self.interest_rate / 100
        return self.balance * ((pow((1 + (ir / cmp_int)), years * cmp_int)) - 1)


if __name__ == '__main__':
    likeu = CreditCard(17, 28, 32000, 33)
    likeu.spend(700, 'sushi', 'food')
    likeu.spend(200, 'cacahuates', 'food', sd=date(2024,2,6))
    likeu.spend(1200, 'dogfood', 'pet', sd=date(2024,2,27))
    likeu.spend(600, 'roses', 'gift', sd=date(2024,2,20))
    likeu.spend(200, 'christmas gifft', 'life', sd=date(2024,12,20))
    likeu.history_ex(months=[3])
    # ba = BankAccount('Bancomer')
    # ba.deposit(1000)
    # day = date.today()
    # cheese = Expense(500, 'chis', 'food', day, day)
    # taboo = Expense(600, 'taboo', 'food', day, day)
    # likeu = CreditCard(23, 27, 50000, 34)
    # likeu.spend(cheese)
    # kitchen = Expense(4000, 'kitchen', 'housing', day, day, length=4)
    # dogfood = Expense(700, 'dogfood', 'pet', day, day, length=2)
    # likeu.add_msi(kitchen)
    # likeu.add_msi(dogfood)

    # for month in likeu.months:
    #     print(f'In month {month.name} the debt is {month.debt}')
    #     if len(month.items) > 0:
    #         print('by items')
    #         for item in month.items:
    #             print(f'''{item.name} with total of {item.total_amount}
    #             to pay this month {item.amount_month}
    #             and debt remaining {item.amount_left}''')
