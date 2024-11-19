from customer import Customer
from operators import Operator
from bill import Bill



class Main:
    """Main class to test customer interactions with the operator."""

    def __init__(self) -> None:
        """
        Initialize the simulation with predefined operators and customers.
        """
    
        self.operator = Operator(id=1, message_cost=0.4, talking_charge=1, network_charge=0.7, discount_rate=0.3)
        self.customer1 = Customer(1, "John", "Doe", 25, [self.operator], 100)
        self.customer2 = Customer(2, "Jane", "Smith", 5, [self.operator], 150)
        self.customer3 = Customer(3, "Mary", "Gray", 67, [self.operator], 100)

    def test_talks(self):
        """
        Test the talk functionality between two customers.
        """
        print("Testing calls...")
        self.customer1.talk(10, self.customer2, self.operator.id)
        self.customer3.talk(17, self.customer2, self.operator.id)

    def test_chat(self):
        """
        Test the message functionality between two customers.
        """
        print("Testing messages...")
        self.customer1.message(8, self.customer3, self.operator.id)
        self.customer2.message(14, self.customer3, self.operator.id)

    def test_networking(self):
        """
        Test the internet connection functionality.
        """
        print("Testing internet connection...")
        self.customer1.connection(1000, self.operator.id)
        self.customer3.connection(20, self.operator.id)



if __name__ == "__main__":
    main = Main()
    main.test_chat()
    main.test_talks()
    main.test_networking()
