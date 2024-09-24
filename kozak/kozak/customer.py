from typing import List, Dict, Self, TYPE_CHECKING
if TYPE_CHECKING:
    from src.operator import Operator
    from src.bill import Bill


class Customer:
    """
    The Customer class represents a mobile service customer. Each customer has a unique
    ID, personal details (first name, last name, and age), and a list of available operators.
    The customer can make calls, send messages, and use internet services through the associated operators.
    """

    def __init__(self, id: int, first_name: str, last_name: str,
                 age: float, operators: List['Operator']) -> None:
        """
        Initializes a Customer instance with personal details and available operators.

        Args:
            id (int): The unique identifier of the customer.
            first_name (str): The customer's first name.
            last_name (str): The customer's last name.
            age (float): The customer's age.
            operators (List[Operator]): A list of operators the customer can interact with.
        """
        self.id: int = id
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.age: float = age
        self.operators: Dict[int, Operator] = {operator.id: operator for operator in operators}
        self.bills: List[Bill] = []  # A list of bills associated with the customer

    def talk(self, duration: float, other_customer: Self, operator_id: int) -> None:
        """
        Simulates a phone conversation between the customer and another customer. The cost of the call is
        calculated based on the operator's pricing, and a bill is generated.

        Args:
            duration (float): The duration of the call in minutes.
            other_customer (Customer): The customer on the other end of the call.
            operator_id (int): The ID of the operator facilitating the call.
        """
        operator = self.operators[operator_id]
        operator.calculate_talking_cost(duration=duration, customer=self)

        my_bill = operator.get_bill(operator_id=self.id)
        self.bills.append(my_bill)

        print(f"{self.first_name} розмовляв з {other_customer.first_name}")

    def message(self, quantity: int, other_customer: Self, operator_id: int) -> None:
        """
        Simulates sending messages to another customer. The cost is calculated based on the operator's message rate,
        and a bill is generated.

        Args:
            quantity (int): The number of messages sent.
            other_customer (Customer): The recipient customer.
            operator_id (int): The ID of the operator handling the message service.
        """
        operator = self.operators[operator_id]
        operator.calculate_message_cost(quantity=quantity, customer=self, other=other_customer)

        my_bill = operator.get_bill(operator_id=self.id)
        self.bills.append(my_bill)

        print(f"{self.first_name} надіслав {quantity} повідомлень {other_customer.first_name}")

    def connection(self, amount: float, operator_id: int) -> None:
        """
        Simulates the usage of internet data by the customer. The cost of the data usage is calculated by the operator,
        and a bill is generated.

        Args:
            amount (float): The amount of data used in MB.
            operator_id (int): The ID of the operator providing the internet connection.
        """
        operator = self.operators[operator_id]
        operator.calculate_network_cost(customer=self)

        my_bill = operator.get_bill(operator_id=self.id)
        self.bills.append(my_bill)

        print(f"{self.first_name} використав {amount} МБ даних")
