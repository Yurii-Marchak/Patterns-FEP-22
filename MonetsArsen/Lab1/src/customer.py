"""
Customer Management Module

This module defines the Customer class, which represents a customer in a
telecommunication system. It provides methods for various customer actions
such as talking, messaging, and using network data.

Classes:
    Customer: Represents a customer with methods for telecom actions.

Dependencies:
    - src.bill.Bill
    - src.operator.Operator (for type checking)
"""

import string
from typing import List, TYPE_CHECKING, Self, Dict

from src.bill import Bill

if TYPE_CHECKING:
    from src.operator import Operator


class Customer:
    """
    Represents a customer in a telecommunication system.

    This class provides methods for various customer actions such as
    talking, messaging, and using network data. It interacts with
    Operator objects to calculate costs and manage bills.

    Attributes:
        id (int): Unique identifier for the customer.
        first_name (str): Customer's first name.
        last_name (str): Customer's last name.
        age (int): Customer's age.
        operators (Dict[int, 'Operator']): Dictionary of operators associated with the customer.
    """

    def __init__(self, identifier: int, first_name: str, last_name: str,
                 age: int, operators: List['Operator']) -> None:
        """
        Initialize a Customer object.

        Args:
            identifier (int): Unique identifier for the customer.
            first_name (str): Customer's first name.
            last_name (str): Customer's last name.
            age (int): Customer's age.
            operators (List['Operator']): List of operators associated with the customer.

        Returns:
            None
        """
        self.id: int = identifier
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.age: int = age
        self.operators: Dict[int, 'Operator'] = {operator.id: operator for operator in operators}

    def talk(self, duration: float, other_customer: Self, operator_id: int) -> None:
        """
        Record a phone call made by the customer.

        This method calculates the cost of the call and updates the customer's bill.

        Args:
            duration (float): Duration of the call in minutes.
            other_customer (Self): The customer being called.
            operator_id (int): ID of the operator used for the call.

        Returns:
            None
        """
        operator = self.operators[operator_id]
        operator.calculate_talking_cost(duration=duration, customer=self)
        bill = operator.get_bill(customer_id=self.id)
        _print_with_check(f"{self.first_name} has talked to {other_customer.first_name} for {duration} minutes", bill)

    def message(self, quantity: float, other_customer: Self, operator_id: int) -> None:
        """
        Record messages sent by the customer.

        This method calculates the cost of the messages and updates the customer's bill.

        Args:
            quantity (float): Number of messages sent.
            other_customer (Self): The customer receiving the messages.
            operator_id (int): ID of the operator used for messaging.

        Returns:
            None
        """
        operator = self.operators[operator_id]
        operator.calculate_message_cost(quantity=quantity, customer=self, other_customer=other_customer)
        bill = operator.get_bill(customer_id=self.id)
        _print_with_check(f"{self.first_name} has sent {quantity} message(s) to {other_customer.first_name}", bill)

    def connection(self, amount: float, operator_id: int) -> None:
        """
        Record network data usage by the customer.

        This method calculates the cost of the data usage and updates the customer's bill.

        Args:
            amount (float): Amount of data used in megabytes.
            operator_id (int): ID of the operator used for the data connection.

        Returns:
            None
        """
        operator = self.operators[operator_id]
        operator.calculate_network_cost(amount=amount, customer=self)
        bill = operator.get_bill(customer_id=self.id)
        _print_with_check(f"{self.first_name} has used {amount} megabyte(s)", bill)

    def get_bill(self, operator_id: int) -> Bill:
        """
        Retrieve the customer's bill for a specific operator.

        Args:
            operator_id (int): ID of the operator for which to retrieve the bill.

        Returns:
            Bill: The customer's bill for the specified operator.
        """
        operator = self.operators[operator_id]
        return operator.get_bill(self.id)


def _print_with_check(text: str, bill: 'Bill') -> None:
    """
    Print the given text if the bill has not reached its limit.

    Args:
        text (str): The text to print.
        bill (Bill): The bill to check.

    Returns:
        None
    """
    if not bill.is_reached_limit():
        print(text)