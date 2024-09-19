"""Docstring"""
from typing import List, Self, Dict
from typing import TYPE_CHECKING
from my_operator import Operator

if TYPE_CHECKING:

    from bill import Bill

class Customer:
    """
    Represents a customer using the services of a telecom operator.

    Attributes:
        id (int): The customer's unique identifier.
        first_name (str): The customer's first name.
        last_name (str): The customer's last name.
        age (float): The customer's age.
        limiting_amount (float): The maximum amount the customer can spend.
        operators (Dict[int, Operator]): A dictionary mapping operator IDs to Operator objects.
        bills (Dict[int, Bill]): A dictionary mapping customer IDs to Bill objects.
    """
    def __init__(self, id: int, first_name: str, last_name: str,
                 age: float, limiting_amount: float, operators: List[Operator]) -> None:
        self.id: int = id
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.age: float = age
        self.limiting_amount = limiting_amount
        self.operators: Dict[int, 'Operator'] = {operator.id: operator for operator in operators}
        self.bills: Dict[int, Bill] = {}

    def talk(self, duration: float, customer: Self, operator_id: int) -> None:
        """
        Allows the customer to make a call.

        Args:
            duration (float): The duration of the call in minutes.
            customer (Self): The customer being called.
            operator_id (int): The ID of the operator providing the service.

        Effect:
            The call cost is calculated and added to the customer's bill.
        """
        operator = self.operators[operator_id]
        operator.calculate_talking_cost(duration=duration, customer = self)
        
 


    def connection(self,  data_usage_mb: float, operator_id: int ) -> None:
        """
        Allows the customer to use mobile data.

        Args:
            data_usage_mb (float): The amount of data used in megabytes.
            operator_id (int): The ID of the operator providing the service.

        Effect:
            The data usage cost is calculated and added to the customer's bill.
        """
        operator = self.operators[operator_id]
        result = operator.calculate_network_cost(mbs = data_usage_mb,
                                                 customer = self)
 

    def message(self, quantity: int, operator_id: int, other_customer: 'Customer' ) -> None:
        """
        Allows the customer to send messages to another customer.

        Args:
            quantity (int): The number of messages sent.
            operator_id (int): The ID of the operator providing the service.
            other_customer (Customer): The customer receiving the messages.

        Effect:
            The messaging cost is calculated and added to the customer's bill.
        """
        operator = self.operators[operator_id]
        result = operator.calculate_message_cost(quantity = quantity, another_customer = other_customer, customer = self, operator_id=operator_id)
