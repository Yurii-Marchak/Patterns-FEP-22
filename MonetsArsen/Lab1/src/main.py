"""
Main

This module contains a test suite for the telecom system, including tests for
customer operations, billing, and various scenarios involving different
operators and customer types.

Classes:
    Main: A test suite for the telecom system.

Dependencies:
    - src.customer.Customer
    - src.operator.Operator
"""

from typing import List

from src.customer import Customer
from src.operator import Operator


class Main:
    """
    A test suite for the telecom system.

    This class initializes a set of operators and customers, and provides
    methods to test various aspects of the system including talking, messaging,
    network usage, bill limits, age-based discounts, and operator-based discounts.
    """

    def __init__(self) -> None:
        """
        Initialize the test suite with a set of operators and customers.
        """
        self.operators: List[Operator] = [
            Operator(identifier=0, message_cost=2, talking_charge=10, network_charge=1, discount_rate=0.5),
            Operator(identifier=1, message_cost=1.5, talking_charge=8, network_charge=1.2, discount_rate=0.4),
            Operator(identifier=2, message_cost=2.5, talking_charge=12, network_charge=0.8, discount_rate=0.3),
            Operator(identifier=3, message_cost=2, talking_charge=9, network_charge=1.5, discount_rate=0.6),
            Operator(identifier=4, message_cost=1.8, talking_charge=11, network_charge=1.1, discount_rate=0.45)
        ]

        self.customers: List[Customer] = [
            Customer(identifier=0, first_name="Alice", last_name="Johnson", age=29, operators=self.operators),
            Customer(identifier=1, first_name="Bob", last_name="Smith", age=34, operators=self.operators),
            Customer(identifier=2, first_name="Carol", last_name="Davis", age=22, operators=self.operators),
            Customer(identifier=3, first_name="Dave", last_name="Wilson", age=45, operators=self.operators),
            Customer(identifier=4, first_name="Eve", last_name="Brown", age=38, operators=self.operators)
        ]

    def test_talks(self):
        """Test the talking functionality for all customers and operators."""
        for i, customer in enumerate(self.customers):
            for j, operator in enumerate(self.operators):
                next_customer = self.customers[(i + 1) % len(self.customers)]
                customer.talk(8, next_customer, j)
                bill = customer.get_bill(j)
                bill.pay(8 * operator.talking_charge)
                assert bill.limiting_amount == 100, "Bill limit changed unexpectedly"
        print("Talk test completed successfully.\n")

    def test_chat(self):
        """Test the messaging functionality for all customers and operators."""
        for i, customer in enumerate(self.customers):
            for j, operator in enumerate(self.operators):
                next_customer = self.customers[(i + 1) % len(self.customers)]
                customer.message(8, next_customer, j)
                bill = customer.get_bill(j)
                bill.pay(8 * operator.message_cost)
                assert bill.limiting_amount == 100, "Bill limit changed unexpectedly"
        print("Chat test completed successfully.\n")

    def test_networking(self):
        """Test the network usage functionality for all customers and operators."""
        for i, customer in enumerate(self.customers):
            for j, operator in enumerate(self.operators):
                customer.connection(50, j)
                bill = customer.get_bill(j)
                bill.pay(50 * operator.network_charge)
                assert bill.limiting_amount == 100, "Bill limit changed unexpectedly"
        print("Networking test completed successfully.\n")

    def test_reaching_and_changing_limit(self):
        """Test reaching and changing the bill limit for a customer."""
        customer = self.customers[0]
        operator_id = 0
        customer.connection(50, operator_id)
        customer.connection(50, operator_id)
        customer.get_bill(operator_id).pay(50)
        print(f"{customer.first_name} paid 50")
        customer.connection(50, operator_id)
        customer.get_bill(operator_id).pay(50)
        print(f"{customer.first_name} paid 50")
        customer.get_bill(operator_id).change_limit(150)
        customer.connection(50, operator_id)
        customer.connection(50, operator_id)
        customer.get_bill(operator_id).pay(100)
        print(f"{customer.first_name} paid 100")
        print("Limit change test completed successfully.\n")

    def test_people_with_different_age(self):
        """Test age-based discounts for customers of different ages."""
        customers_with_different_ages: List[Customer] = [
            self.customers[0],
            Customer(identifier=5, first_name="Linda", last_name="Johnson", age=14, operators=self.operators),
            Customer(identifier=6, first_name="Tom", last_name="Smith", age=75, operators=self.operators),
        ]
        operator_id = 0
        for customer in customers_with_different_ages:
            customer.talk(8, self.customers[1], operator_id)

        print("Middle-aged:", customers_with_different_ages[0].get_bill(operator_id).current_debt)
        customers_with_different_ages[0].get_bill(operator_id).pay(80)
        print("Teenager:", customers_with_different_ages[1].get_bill(operator_id).current_debt)
        print("Old man:", customers_with_different_ages[2].get_bill(operator_id).current_debt)
        print("Age-based discount test completed successfully.\n")

    def test_message_discount(self):
        """Test message discounts for customers with the same and different operators."""
        customers_with_different_and_same_operators: List[Customer] = [
            self.customers[0],
            self.customers[1],
            Customer(
                identifier=7,
                first_name="John",
                last_name="Smith",
                age=34,
                operators=[
                    Operator(identifier=5, message_cost=1.8, talking_charge=11, network_charge=1.1, discount_rate=0.45)]
            ),
        ]
        operator_id = 0
        customers_with_different_and_same_operators[0].message(8, customers_with_different_and_same_operators[1],
                                                               operator_id)
        print("Current debt (same operator):",
              customers_with_different_and_same_operators[0].get_bill(operator_id).current_debt)
        customers_with_different_and_same_operators[0].get_bill(operator_id).pay(100)
        customers_with_different_and_same_operators[0].message(8, customers_with_different_and_same_operators[2],
                                                               operator_id)
        print("Current debt (different operators):",
              customers_with_different_and_same_operators[0].get_bill(operator_id).current_debt)
        print("Message discount test completed successfully.\n")


def run_tests():
    """Run all tests in the test suite."""
    test_suite = Main()
    test_suite.test_chat()
    test_suite.test_talks()
    test_suite.test_networking()
    test_suite.test_reaching_and_changing_limit()
    test_suite.test_people_with_different_age()
    test_suite.test_message_discount()


if __name__ == "__main__":
    run_tests()
