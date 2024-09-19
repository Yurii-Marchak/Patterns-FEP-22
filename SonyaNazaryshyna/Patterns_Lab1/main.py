from customer import Customer
from operator_1 import Operator
from bill import Bill
from typing import List

class Main:

    def __init__(self) -> None:
        self.operators: List[Operator] = [
            Operator(id=1, talkingCharge=2.5, messageCost=1.2, networkCharge=0.8, discountRate=25), 
            Operator(id=2, talkingCharge=3.2, messageCost=1.8, networkCharge=1.2, discountRate=10)
        ]
        
        self.customers: List[Customer] = [
            Customer(id=1, name="Jane", age=15, operators=self.operators, limitingAmount=150), 
            Customer(id=2, name="John", age=66, operators=self.operators, limitingAmount=100),
            Customer(id=3, name="Alex", age=32, operators=self.operators, limitingAmount=100)
        ]

    def test_talks(self):
        Jane = self.customers[0]
        John = self.customers[1]
        Alex = self.customers[2]
        operator_1 = self.operators[0]
        operator_2 = self.operators[1]
        Jane.talk(10, John, 1)
        John.talk(5, Alex, 2)
        jane_bill = operator_1.customers_bills[Jane.id]
        john_bill = operator_2.customers_bills[John.id]
        john_bill.pay(20)

    def test_chat(self):
        Jane = self.customers[0]
        John = self.customers[1]
        Alex = self.customers[2]
        operator_1 = self.operators[0]
        operator_2 = self.operators[1]
        John.message(6, 2, Jane, 2)
        Alex.message(11, 1, John, 2)
        alex_bill = operator_1.customers_bills[Alex.id]
        alex_bill.changeTheLimit(20)
        

    def test_networking(self):
        Jane = self.customers[0]
        John = self.customers[1]
        Alex = self.customers[2]
        operator_1 = self.operators[0]
        operator_2 = self.operators[1]
        John.connection(120, 1)
        Alex.connection(80, 2)
        alex_bill = operator_2.customers_bills[Alex.id]
        alex_bill.pay(70)
        
        
        
main = Main()
print('Talk')
main.test_talks()
print('\t')
print('Chat')
main.test_chat()
print('\t')
print('Net')
main.test_networking()
print('\t')
