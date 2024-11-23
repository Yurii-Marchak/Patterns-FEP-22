from typing import Dict, TYPE_CHECKING
from bill import Bill
from src import bill

if TYPE_CHECKING:
    from src.customer import Customer

class Operator:
    """Represents an operator with cost and discount details."""

    def __init__(self, id: int, message_cost: float, talking_charge: float, network_charge: float, discount_rate: float) -> None:
        self.id: int = id
        self.message_cost: float = message_cost
        self.talking_charge: float = talking_charge
        self.network_charge: float = network_charge
        self.discount_rate: float = discount_rate
        self.customer_bills: Dict[int, Bill] = {}

    def _check_if_customer_has_bill(self, customer_id: int) -> bool:
        """Check if the customer has a bill."""
        return customer_id in self.customer_bills

    def calculate_talking_cost(self, minutes: int, customer: 'Customer') -> float:
        """
        Calculate the total amount to pay for talking.

        Args:
            minutes (int): Duration of the call in minutes.
            customer (Customer): The customer who made the call.

        Returns:
            float: Total cost of the call.
        """

        cost = self.talking_charge * minutes
        if self._check_if_customer_has_bill(customer_id=customer.id):
            customer_bill = self.customer_bills[customer.id]
            customer_bill.add(amount=cost)
        else:
            bill = Bill(limiting_amount=100)
            self.customer_bills[customer.id] = bill
            bill.add(amount=cost)
            print(f"New bill for customer {customer.name} is created")

        return cost

    def calculate_message_cost(self, quantity: int, customer: 'Customer', other: 'Customer') -> float:
        """
        Calculate the total amount to pay for messages.

        Args:
            quantity (int): Number of messages sent.
            customer (Customer): The customer who sent the messages.
            other (Customer): The customer who received the messages.

        Returns:
            float: Total cost of the messages.
        """

        cost = self.message_cost * quantity
        if self._check_if_customer_has_bill(customer_id=customer.id):
            customer_bill = self.customer_bills[customer.id]
            customer_bill.add(amount=cost)
        else:
            bill = Bill(limiting_amount=100)
            self.customer_bills[customer.id] = bill
            bill.add(amount=cost)
            print(f"New bill for customer {customer.name} is created")

        return cost

    def calculate_network_cost(self, amount: float) -> float:
        """
        Calculate the total amount to pay for internet data usage.

        Args:
            amount (float): Amount of data used in MB.

        Returns:
            float: Total cost of the data usage.
        """
        cost = self.network_charge * amount

        for customer_id in self.customer_bills:
            customer_bill = self.customer_bills[customer_id]
            customer_bill.add(amount=cost)
        return cost

    def get_bill(self, customer_id: int):
        return self.customer_bills[customer_id]


    def get_talking_charge(self) -> float:
        return self.talking_charge

    def set_talking_charge(self, talking_charge: float) -> None:
        self.talking_charge = talking_charge

    def get_message_cost(self) -> float:
        return self.message_cost

    def set_message_cost(self, message_cost: float) -> None:
        self.message_cost = message_cost

    def get_network_charge(self) -> float:
        return self.network_charge

    def set_network_charge(self, network_charge: float) -> None:
        self.network_charge = network_charge

    def get_discount_rate(self) -> int:
        return self.discount_rate

    def set_discount_rate(self, discount_rate: int) -> None:
        self.discount_rate = discount_rate
