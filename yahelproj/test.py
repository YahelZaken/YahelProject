import random
from bank import Bank, Employee, Customer
if __name__ == '__main__':
    bank = Bank()
    employee1 = Employee("Dor", 32, random.randint(0, 9000))
    customer = Customer("Yahel", 30, random.randint(0, 9000))

    employee1.display()
    customer.display()

    customer.bank_account.deposit(1000)
    customer.bank_account.withdraw(500)
    customer.bank_account.get_balance()

