from typing import List
from bill import Bill
from my_customer import Customer
from my_operator import Operator

class Main:

    def __init__(self) -> None:
        
        self.operators: List[Operator] = [
            Operator(id=1, name="Life Cell",message_cost=3,talking_charge=3,network_charge=2,discount_rate=10),
            Operator(id=2, name="Kyivstar",message_cost=5,talking_charge=2,network_charge=3,discount_rate=10),
            Operator(id=3, name="Vodaphone",message_cost=6,talking_charge=25,network_charge=5,discount_rate=5)
        ] 

        self.customers: List[Customer] = [Customer(
            id=1, first_name="John", last_name="Brown", age=31, operators=self.operators, limiting_amount=200
        ),
            Customer(
            id=2, first_name="Alex", last_name="Smith", age=18, operators=self.operators, limiting_amount=100
        ),
            Customer(
            id=3, first_name="Anna", last_name="Barabarosa", age=18, operators=self.operators, limiting_amount=150
        )]

        # self.operators = operators
        

    def test_talks(self):
        john = self.customers[0]
        alex = self.customers[1]
        anna = self.customers[2]
        
        operator1 = self.operators[0]
        operator2= self.operators[1]
        
        
        alex.talk(6, john, 1)
        # alex.talk(100, anna, 1)
        
        alex_bill = operator1.customer_bills[alex.id]
        alex_bill.pay(120)
        
        anna.talk(10, alex, 1 )
        
        

    def test_chat(self):
        pass
        # run all methods for messages
        john = self.customers[0]
        alex = self.customers[1]
        anna = self.customers[2]
        
        operator1 = self.operators[0]
        operator2= self.operators[1]
        
        alex.message(5, 1, anna)
        
        

    def test_networking(self):
        
        # run all methods for networking
        john = self.customers[0]
        alex = self.customers[1]
        anna = self.customers[2]
        
        operator1 = self.operators[0]
        operator2= self.operators[1]
        
        alex.connection(100, 1)
        alex_bill = operator1.customer_bills[alex.id]
        # print(alex_bill.limiting_amount)
        alex_bill.change_limit(200)
        alex_bill.pay(100)
        # print(alex_bill.limiting_amount)
        # print(alex_bill.current_debt)
        alex.connection(100, 1)
        

main = Main()
main.test_talks()
print('')
main.test_chat()
print('')
main.test_networking()
