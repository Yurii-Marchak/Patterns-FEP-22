from src.customer import Customer
from src.operator import Operator

class Main:
    """
    The Main class serves as the entry point for testing various customer interactions
    with operators, such as making calls, sending messages, and connecting to the internet.
    It initializes a set of customers and operators and provides methods to test different
    functionalities.
    """

    def __init__(self) -> None:
        """
        Initializes the Main class by creating arrays of customers and operators.
        Each customer is associated with one or more operators, which define the cost
        structure for their communications.
        """
        self.operators = [
            Operator(id=1, message_cost=0.05, talking_charge=0.10, network_charge=0.01, discount_rate=0.1),
            Operator(id=2, message_cost=0.08, talking_charge=0.12, network_charge=0.015, discount_rate=0.15)
        ]

        self.customers = [
            Customer(id=1, first_name="Alice", last_name="Johnson", age=25, operators=self.operators),
            Customer(id=2, first_name="Bob", last_name="Smith", age=30, operators=[self.operators[0]]),
        ]

    def test_talks(self):
        """
        Simulates a phone call between two customers and tests the call functionality.
        This method prints a message indicating that calls are being tested.
        """
        print("Тестуємо дзвінки:")
        self.customers[0].talk(duration=10, other_customer=self.customers[1], operator_id=1)

    def test_chat(self):
        """
        Simulates sending messages between two customers and tests the messaging functionality.
        This method prints a message indicating that messaging is being tested.
        """
        print("Тестуємо повідомлення:")
        self.customers[0].message(quantity=5, other_customer=self.customers[1], operator_id=1)

    def test_networking(self):
        """
        Simulates an internet connection by a customer and tests the data usage functionality.
        This method prints a message indicating that internet connection is being tested.
        """
        print("Тестуємо інтернет-з'єднання:")
        self.customers[0].connection(amount=100, operator_id=1)

# Initialize and run tests
main = Main()
main.test_chat()
main.test_talks()
main.test_networking()
