from typing import List, Dict, TYPE_CHECKING
if TYPE_CHECKING:
    from src.c_operator import Operator
    from src.bill import Bill


class Customer:
    """Represents a customer with details for managing bills and interactions."""

    def __init__(self, id: int, name: str, age: int, operators: List['Operator'],
                 bills: List['Bill'], limitingAmount: float) -> None:
        self.id: int = id
        self.name: str = name
        self.age: int = age
        self.operators: Dict[int, Operator] = {operator.id: operator for operator in operators}
        self.bills: List[Bill] = bills
        self.limitingAmount: float = limitingAmount

    def talk(self, minutes: int, other: 'Customer') -> None:
        """Allow customers to talk via the operator."""
        if self.operators:
            operator = self.operators[0]
            operator.calculate_talking_cost(minutes=minutes, customer=self)

            my_bill = operator.get_bill(customer_id=self.id)
            self.bills.append(my_bill)

            print(f"{self.name} has talked to {other.name}")

    def message(self, quantity: int, other: 'Customer') -> None:
        """Allow customers to send messages to another customer."""
        if self.operators:
            operator = self.operators[0]  # Or choose the appropriate operator
            operator.calculate_message_cost(quantity=quantity, customer=self, other=other)

            my_bill = operator.get_bill(customer_id=self.id)
            self.bills.append(my_bill)

            print(f"{self.name} has sent {quantity} messages to {other.name}")

    def connection(self, amount: float) -> None:
        """Allow customers to connect to the internet."""
        if self.operators:
            operator = self.operators[0]
            operator.calculate_network_cost(amount=amount)

            my_bill = operator.get_bill(customer_id=self.id)
            self.bills.append(my_bill)

            print(f"{self.name} has used {amount} MB of internet")

    # Getter and setter methods
    def get_age(self) -> int:
        return self.age

    def set_age(self, age: int) -> None:
        self.age = age

    def get_operators(self) -> List['Operator']:
        return list(self.operators.values())

    def set_operators(self, operators: List['Operator']) -> None:
        self.operators = {operator.id: operator for operator in operators}

    def get_bills(self) -> List['Bill']:
        return self.bills

    def set_bills(self, bills: List['Bill']) -> None:
        self.bills = bills