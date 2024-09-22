"""
Operator Management Module

This module defines the Operator class, which represents a telecom operator
in a customer billing system. It provides methods for calculating various
costs and managing customer bills.

Classes:
    Operator: Represents a telecom operator with methods for cost calculation and bill management.

Dependencies:
    - src.bill.Bill
    - customer.Customer (for type checking)
"""

from typing import TYPE_CHECKING, Dict

from src.bill import Bill

if TYPE_CHECKING:
    from customer import Customer


class Operator:
    """
    Represents a telecom operator in a customer billing system.

    This class provides methods for calculating costs of various services
    (talking, messaging, network usage) and managing customer bills.

    Attributes:
        id (int): Unique identifier for the operator.
        message_cost (float): Cost per message.
        talking_charge (float): Charge per minute of talking.
        network_charge (float): Charge per unit of network usage.
        discount_rate (float): Discount rate applied to certain customers or services.
        customer_bills (Dict[int, Bill]): Dictionary of customer bills, keyed by customer ID.
    """

    def __init__(self, identifier: int, message_cost: float,
                 talking_charge: float, network_charge: float,
                 discount_rate: float) -> None:
        """
        Initialize an Operator object.

        Args:
            identifier (int): Unique identifier for the operator.
            message_cost (float): Cost per message.
            talking_charge (float): Charge per minute of talking.
            network_charge (float): Charge per unit of network usage.
            discount_rate (float): Discount rate applied to certain customers or services.

        Returns:
            None
        """
        self.id: int = identifier
        self.message_cost: float = message_cost
        self.talking_charge: float = talking_charge
        self.network_charge: float = network_charge
        self.discount_rate: float = discount_rate
        self.customer_bills: Dict[int, Bill] = {}

    def _check_if_customer_has_bill(self, customer_id: int) -> bool:
        """
        Check if a customer already has a bill.

        Args:
            customer_id (int): The ID of the customer to check.

        Returns:
            bool: True if the customer has a bill, False otherwise.
        """
        return customer_id in self.customer_bills

    def get_bill(self, customer_id: int) -> Bill:
        """
        Retrieve a customer's bill.

        Args:
            customer_id (int): The ID of the customer whose bill to retrieve.

        Returns:
            Bill: The customer's bill.

        Raises:
            KeyError: If the customer does not have a bill.
        """
        return self.customer_bills[customer_id]

    def calculate_talking_cost(self, duration: float, customer: 'Customer') -> None:
        """
        Calculate and add the cost of a call to a customer's bill.

        Applies a discount for customers under 18 or over 65 years old.

        Args:
            duration (float): The duration of the call in minutes.
            customer (Customer): The customer who made the call.

        Returns:
            None
        """
        cost = self.talking_charge * duration
        if customer.age < 18 or customer.age > 65:
            cost *= (1 - self.discount_rate)
        self._write_bill(cost, customer)

    def calculate_network_cost(self, amount: float, customer: 'Customer') -> None:
        """
        Calculate and add the cost of network usage to a customer's bill.

        Args:
            amount (float): The amount of network usage.
            customer (Customer): The customer who used the network.

        Returns:
            None
        """
        cost = self.network_charge * amount
        self._write_bill(cost, customer)

    def calculate_message_cost(self, quantity: float, customer: 'Customer', other_customer: 'Customer') -> None:
        """
        Calculate and add the cost of messages to a customer's bill.

        Applies a discount if the recipient is also a customer of this operator.

        Args:
            quantity (float): The number of messages sent.
            customer (Customer): The customer who sent the messages.
            other_customer (Customer): The customer who received the messages.

        Returns:
            None
        """
        cost = self.message_cost * quantity
        if self._check_if_customer_has_bill(other_customer.id):
            cost *= (1 - self.discount_rate)
        self._write_bill(cost=cost, customer=customer)

    def _write_bill(self, cost: float, customer: 'Customer') -> None:
        """
        Add a cost to a customer's bill, creating a new bill if necessary.

        Args:
            cost (float): The cost to add to the bill.
            customer (Customer): The customer whose bill to update.

        Returns:
            None
        """
        if self._check_if_customer_has_bill(customer_id=customer.id):
            self.customer_bills[customer.id].add(cost)
        else:
            bill = Bill(customer_id=customer.id)
            self.customer_bills[customer.id] = bill
            print(f"New bill for customer {customer.first_name} is created")
            bill.add(cost)