
class Bank:

    def __init__(self):
        self.employee = []
        self.customer = []


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


class Employee(Person):
    def __init__(self, name, age, employee_id):
        super().__init__(name, age)
        self.employee_id = employee_id

    def display(self):
        print("The employee name is "+self.name+" her/his age is:", self.age, "and employee id:", self.employee_id)


class Customer(Person):
    def __init__(self, name, age, customer_id):
        super().__init__(name, age)
        self.customer_id = customer_id
        self.bank_account = BankAccount()

    def display(self):
        print("The customer name is "+self.name+" her/his age is:", self.age, "and customer id:",self.customer_id)


class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance

    def withdraw(self, money):
        self.balance = self.balance - money

    def get_balance(self):
        print("The current balance is: ", self.balance)

    def deposit(self, money):
        self.balance = self.balance + money



