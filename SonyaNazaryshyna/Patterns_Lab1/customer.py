from typing import List, TYPE_CHECKING, Self, Dict
from operator_1 import Operator
if TYPE_CHECKING:
    from bill import Bill
    
class Customer:
    """
    A class to represent a customer, who interacts with operators and manages services 
    such as talking, messaging, and network connection.
    
    Attributes:
    ----------
    id : int
        The unique identifier for the customer.
    name : str
        The customer's name.
    age : int
        The customer's age.
    limitingAmount : float
        The financial limit for the customer's bills.
    operators : Dict[int, Operator]
        A dictionary mapping operator IDs to Operator objects.
    bills : Dict[int, Bill]
        A dictionary mapping operator IDs to Bill objects for tracking usage.
    """
    def __init__(self, id: int, name: str, age: int, 
                operators: List[Operator], limitingAmount: float) -> None:
        self.id: int = id
        self.name: str = name
        self.age: int = age
        self.limitingAmount: float = limitingAmount
        self.op_name = None
        self.operators: Dict[int, 'Operator'] = {operator.id: operator for operator in operators}
        self.bills: Dict[int, Bill] = {}
    
    def talk(self, minute: float, other_customer: Self, operator_id: int) -> None:
        """
        Allows the customer to make a call through a specified operator and calculates 
        the cost of the call based on the operator's rates.

        Parameters:
        ----------
        minute : float
            The duration of the call in minutes.
        other_customer : Customer
            The customer receiving the call.
        operator_id : int
            The ID of the operator used for the call.
        """
        operator = self.operators[operator_id]
        operator.calculateTalkingCost(minute=minute, customer=self)
    
    def message(self, quantity: int, operator_id: int, other_customer: 'Customer', other_operator_id: int):
        """
        Sends messages to another customer and calculates the cost based on both 
        customers' operators.

        Parameters:
        ----------
        quantity : int
            The number of messages sent.
        operator_id : int
            The ID of the operator for the sending customer.
        other_customer : Customer
            The receiving customer of the messages.
        other_operator_id : int
            The ID of the operator for the receiving customer.    
        """
        operator1 = self.operators[operator_id]
        operator2 = other_customer.operators[other_operator_id]
        operator1.calculateMessageCost(quantity=quantity, customer=self, other_customer=other_customer, operator2=operator2)
    
    def connection(self, amount: int, operator_id: int):
        """
        Uses network data and calculates the cost of the connection through the specified operator.

        Parameters:
        ----------
        amount : int
            The amount of network data used in megabytes.
        operator_id : int
            The ID of the operator providing the network service.
        """
        operator = self.operators[operator_id]
        operator.calculateNetworkCost(amount=amount, customer=self)
