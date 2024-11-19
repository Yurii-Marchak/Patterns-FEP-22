from typing import List, Dict
from bill import Bill
from operators import Operator

class Customer:
    """Customer class representing a mobile service user."""

    def __init__(self, id: int, first_name: str, last_name: str, age: int, operators: List[Operator], limiting_amount: float) -> None:
        """
        Initialize the customer with personal details and available operators.

        Args:
            id (int): Customer ID.
            first_name (str): First name of the customer.
            last_name (str): Last name of the customer.
            age (int): Age of the customer.
            operators (List[Operator]): List of available operators for the customer.
            limiting_amount (float): Initial limit for the customer's bill.
        """
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.operators: Dict[int, Operator] = {operator.id: operator for operator in operators}
        self.bills: List[Bill] = [Bill(limiting_amount)]  

    def talk(self, minute: int, other_customer: 'Customer', operator_id: int) -> None:
        """
        Make a call to another customer.

        Args:
            minute (int): Duration of the call in minutes.
            other_customer (Customer): The customer being called.
            operator_id (int): ID of the operator handling the call.
        """
        operator = self.operators[operator_id]
        operator.calculate_talking_cost(minute, self)
        print(f"{self.first_name} talked to {other_customer.first_name} for {minute} minutes.")

    def message(self, quantity: int, other_customer: 'Customer', operator_id: int) -> None:
        """
        Send messages to another customer.

        Args:
            quantity (int): Number of messages to send.
            other_customer (Customer): The customer receiving the messages.
            operator_id (int): ID of the operator handling the messages.
        """
        operator = self.operators[operator_id]
        operator.calculate_message_cost(quantity, self, other_customer)
        print(f"{self.first_name} sent {quantity} messages to {other_customer.first_name}.")

    def connection(self, data_amount: float, operator_id: int) -> None:
        """
        Connect to the internet.

        Args:
            data_amount (float): Amount of data used in MB.
            operator_id (int): ID of the operator handling the internet connection.
        """
        operator = self.operators[operator_id]
        operator.calculate_network_cost(self, data_amount)
        print(f"{self.first_name} used {data_amount} MB of internet.")
