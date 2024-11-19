from typing import Dict, TYPE_CHECKING
from bill import Bill

if TYPE_CHECKING:
    from customer import Customer

class Operator:
    """Operator class representing a mobile service provider."""

    def __init__(self, id: int, message_cost: float, talking_charge: float, network_charge: float, discount_rate: float) -> None:
        """
        Initialize the operator with its pricing details.

        Args:
            id (int): Operator ID.
            message_cost (float): Cost per message.
            talking_charge (float): Cost per minute of talk.
            network_charge (float): Cost per MB of data.
            discount_rate (float): Discount rate for certain customer groups.
        """
        self.id = id
        self.message_cost = message_cost
        self.talking_charge = talking_charge
        self.network_charge = network_charge
        self.discount_rate = discount_rate
        self.customer_bills: Dict[int, Bill] = {}

    def _check_if_customer_has_bill(self, customer_id: int) -> bool:
        """
        Check if the customer already has a bill.

        Args:
            customer_id (int): The ID of the customer.

        Returns:
            bool: True if the customer has a bill, False otherwise.
        """
        return customer_id in self.customer_bills

    def calculate_talking_cost(self, minute: int, customer: 'Customer') -> None:
        """
        Calculate and add the cost of talking for a customer.

        Args:
            minute (int): The duration of the call in minutes.
            customer (Customer): The customer making the call.
        """
        cost = self.talking_charge * minute
        if customer.age < 18 or customer.age > 65:
            cost *= (1 - self.discount_rate)
        self._add_to_bill(customer, cost)

    def calculate_message_cost(self, quantity: int, customer: 'Customer', other_customer: 'Customer') -> None:
        """
        Calculate and add the cost of sending messages.

        Args:
            quantity (int): Number of messages.
            customer (Customer): The sender.
            other_customer (Customer): The receiver.
        """
        cost = self.message_cost * quantity
        self._add_to_bill(customer, cost)

    def calculate_network_cost(self, customer: 'Customer', data_amount: float) -> None:
        """
        Calculate and add the cost of internet usage.

        Args:
            customer (Customer): The customer using data.
            data_amount (float): The amount of data in MB.
        """
        cost = self.network_charge * data_amount
        self._add_to_bill(customer, cost)

    def _add_to_bill(self, customer: 'Customer', amount: float) -> None:
        """
        Add the amount to the customer's bill.

        Args:
            customer (Customer): The customer whose bill is being updated.
            amount (float): The amount to add.
        """
        if not self._check_if_customer_has_bill(customer.id):
            self.customer_bills[customer.id] = Bill(limiting_amount=500)
            print(f"New bill created for customer {customer.first_name}")
        self.customer_bills[customer.id].add(amount)

    def get_bill(self, customer_id: int) -> Bill:
        """
        Get the bill associated with a customer.

        Args:
            customer_id (int): The customer ID.

        Returns:
            Bill: The customer's bill.
        """
        return self.customer_bills[customer_id]
