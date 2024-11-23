from typing import List
from src.customer import Customer
from src.c_operator import Operator
from bill import Bill


class Main:
    def __init__(self) -> None:
        """
        Initialize the main class with sample data for customers and operators.
        """

        self.operators: List[Operator] = [
            Operator(id=0, message_cost=0.05, talking_charge=0.10, network_charge=0.02, discount_rate=10),
            Operator(id=1, message_cost=0.07, talking_charge=0.12, network_charge=0.03, discount_rate=15)
        ]


        self.customers: List[Customer] = [
            Customer(id=0, name="Denys", age=25, operators=self.operators, bills=[Bill(limiting_amount=100)],
                     limitingAmount=100),
            Customer(id=1, name="Bob", age=30, operators=self.operators, bills=[Bill(limiting_amount=150)],
                     limitingAmount=150)
        ]

    def test_talks(self) -> None:
        """
        Test the talking functionality between customers.
        """
        alice = self.customers[0]
        bob = self.customers[1]

        print("Testing talks...")
        alice.talk(minutes=10, other=bob)
        bob.talk(minutes=5, other=alice)

        for customer in self.customers:
            for bill in customer.get_bills():
                print(
                    f"Customer {customer.name} - Bill Limit: {bill.get_limiting_amount()}, Current Debt: {bill.get_current_debt()}")

    def test_chat(self) -> None:
        """
        Test the messaging functionality between customers.
        """
        alice = self.customers[0]
        bob = self.customers[1]

        print("Testing chat...")
        alice.message(quantity=15, other=bob)
        bob.message(quantity=10, other=alice)

        for customer in self.customers:
            for bill in customer.get_bills():
                print(
                    f"Customer {customer.name} - Bill Limit: {bill.get_limiting_amount()}, Current Debt: {bill.get_current_debt()}")

    def test_networking(self) -> None:
        """
        Test the internet data usage functionality.
        """
        alice = self.customers[0]
        bob = self.customers[1]

        print("Testing networking...")
        alice.connection(amount=100)
        bob.connection(amount=50)

        for customer in self.customers:
            for bill in customer.get_bills():
                print(
                    f"Customer {customer.name} - Bill Limit: {bill.get_limiting_amount()}, Current Debt: {bill.get_current_debt()}")


if __name__ == "__main__":
    main = Main()
    main.test_talks()
    main.test_chat()
    main.test_networking()
