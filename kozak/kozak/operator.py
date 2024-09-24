from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from src.customer import Customer

from src.bill import Bill


class Operator:
    """
    The Operator class represents a mobile service operator that manages billing for customers
    based on their usage of messages, calls, and internet services. Each operator tracks customer
    bills and applies specific costs for various services, including discounts where applicable.
    """

    def __init__(self, id: int, message_cost: float,
                 talking_charge: float, network_charge: float,
                 discount_rate: float) -> None:
        """
        Initializes an Operator instance with specific pricing details for services.

        Args:
            id (int): The unique identifier for the operator.
            message_cost (float): The cost per message sent by a customer.
            talking_charge (float): The cost per minute of a phone call.
            network_charge (float): The cost per unit of data usage (e.g., MB).
            discount_rate (float): The discount rate applied to certain services (e.g., self-messaging).
        """
        self.id: int = id
        self.message_cost: float = message_cost
        self.talking_charge: float = talking_charge
        self.network_charge: float = network_charge
        self.discount_rate: float = discount_rate
        self.customer_bills: Dict[int, Bill] = {}  # A dictionary storing bills for each customer by their ID

    def _check_if_customer_has_bill(self, customer_id: int) -> bool:
        """
        Checks whether a customer already has a bill in the system.

        Args:
            customer_id (int): The unique ID of the customer.

        Returns:
            bool: True if the customer has a bill, False otherwise.
        """
        return customer_id in self.customer_bills

    def calculate_talking_cost(self, duration: float, customer: 'Customer') -> None:
        """
        Calculates the cost of a phone call for a customer and adds it to their bill.
        If the customer does not have an existing bill, a new one is created.

        Args:
            duration (float): The duration of the call in minutes.
            customer (Customer): The customer who made the call.
        """
        cost = self.talking_charge * duration
        if self._check_if_customer_has_bill(customer_id=customer.id):
            customer_bill = self.customer_bills[customer.id]
            customer_bill.add(amount=cost)
        else:
            bill = Bill(customer_id=customer.id)
            self.customer_bills[customer.id] = bill
            print(f"Створено новий рахунок для клієнта {customer.first_name}")

    def calculate_message_cost(self, quantity: int, customer: 'Customer', other: 'Customer') -> None:
        """
        Calculates the cost of sending messages from one customer to another and adds it to the sender's bill.
        If the customer is sending messages to themselves, a discount is applied. If the customer does not have an
        existing bill, a new one is created.

        Args:
            quantity (int): The number of messages sent.
            customer (Customer): The customer sending the messages.
            other (Customer): The recipient of the messages.
        """
        cost = self.message_cost * quantity
        if customer.id == other.id:
            cost *= (1 - self.discount_rate)

        if self._check_if_customer_has_bill(customer_id=customer.id):
            customer_bill = self.customer_bills[customer.id]
            customer_bill.add(amount=cost)
        else:
            bill = Bill(customer_id=customer.id)
            self.customer_bills[customer.id] = bill
            print(f"Створено новий рахунок для клієнта {customer.first_name}")

    def calculate_network_cost(self, customer: 'Customer') -> None:
        """
        Calculates the cost of data usage for a customer and adds it to their bill.
        If the customer does not have an existing bill, a new one is created.

        Args:
            customer (Customer): The customer using internet data.
        """
        cost = self.network_charge * 100  # Example: using 100 MB of data
        if self._check_if_customer_has_bill(customer_id=customer.id):
            customer_bill = self.customer_bills[customer.id]
            customer_bill.add(amount=cost)
        else:
            bill = Bill(customer_id=customer.id)
            self.customer_bills[customer.id] = bill
            print(f"Створено новий рахунок для клієнта {customer.first_name}")

    def get_bill(self, operator_id: int) -> Bill:
        """
        Retrieves the bill for a specific customer by their operator ID.

        Args:
            operator_id (int): The ID of the operator handling the bill for the customer.

        Returns:
            Bill: The bill associated with the customer.
        """
        return self.customer_bills[operator_id]
