from typing import Dict
from bill import Bill
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from my_customer import Customer

class Operator:
    """TODO: Docstring to fill"""

    def __init__(self, id: int,
                name: str,
                message_cost: float,
                talking_charge: float, 
                network_charge: float,
                discount_rate: float) -> None:
        self.id: int = id
        self.name: str = name
        self.message_cost: float = message_cost
        self.talking_charge: float = talking_charge
        self.network_charge: float = network_charge
        self.discount_rate: float = discount_rate
        self.customer_bills: Dict[int, Bill] = {}

    def _check_if_customer_has_bill(self, customer_id: int) -> bool:
        """
        Checks if a bill exists for a given customer.

        Args:
            customer_id (int): The ID of the customer to check.

        Returns:
            bool: True if the customer has a bill, False otherwise.
        """
        if self.customer_bills.get(customer_id):
            return True
        return False

    def calculate_talking_cost(self, duration: float, customer: 'Customer') -> None:
        """
        Calculates the cost of a phone call and updates the customer's bill.

        Args:
            duration (float): The duration of the call in minutes.
            customer (Customer): The customer making the call.

        Effect:
            Adds the cost of the call to the customer's bill, applying discounts if applicable.
        """
        cost = self.talking_charge * duration
        
        if customer.age < 18 or customer.age > 65:
            discount = self.discount_rate / 100
            cost *= (1 - discount)
            
        customer_bill = self.customer_bills.get(customer.id)

        if customer_bill is None:
            # Customer doesn't have a bill, create a new one
            customer_bill = Bill(customer_id=customer.id)
            self.customer_bills[customer.id] = customer_bill
            print(f"New bill for customer {customer.first_name} is created")
            print(f"{customer.first_name} has been talking for {duration} minutes")
        else:
            customer_bill = self.customer_bills[customer.id]
            print(f"{customer.first_name} has been talking for {duration} minutes") 
            
            
            
        if customer_bill.check(amount=cost):
            allowed_amount = (customer.limiting_amount - customer_bill.current_debt) / self.talking_charge
            allowed_cost = allowed_amount * self.talking_charge
            customer_bill.add(allowed_cost)
            print(f"But you reached the limit. Operation was interrapted, only {allowed_amount:.2f} minutes was available")
        else:
            customer_bill.add(amount=cost)
            

    def calculate_network_cost(self, mbs: float, customer: 'Customer') -> None:
        """
        Calculates the cost of data usage and updates the customer's bill.

        Args:
            mbs (float): The amount of data used in megabytes.
            customer (Customer): The customer using the data.

        Effect:
            Adds the cost of the data usage to the customer's bill, applying discounts if applicable.
        """
        cost =  self.network_charge * mbs
        customer_bill = self.customer_bills.get(customer.id)
        
        
        if customer_bill is None:
            # Customer doesn't have a bill, create a new one
            customer_bill = Bill(customer_id=customer.id)
            self.customer_bills[customer.id] = customer_bill
            print(f"New bill for customer {customer.first_name} is created")
            print(f"{customer.first_name} has been using {mbs} MBs")
        else:
            customer_bill = self.customer_bills[customer.id]
            print(f"{customer.first_name} has been using {mbs} MBs")
            
            
            
        if customer_bill.check(amount=cost):
            allowed_amount = (customer.limiting_amount - customer_bill.current_debt) / self.network_charge
            allowed_cost = allowed_amount * self.network_charge
            customer_bill.add(amount=allowed_cost)
            print(f"But you reached the limit. Operation was interrapted, only {allowed_amount:.2f} MBs were available")
        else:
            customer_bill.add(amount=cost)


    def calculate_message_cost(self, quantity: int, customer: 'Customer', another_customer: 'Customer', operator_id: int) -> None:
        """
        Calculates the cost of sending messages and updates the customer's bill.

        Args:
            quantity (int): The number of messages sent.
            customer (Customer): The customer sending the messages.
            another_customer (Customer): The recipient of the messages.
            operator_id (int): The ID of the operator providing the service.

        Effect:
            Adds the cost of the messages to the customer's bill, applying discounts if applicable.
        """
        
        
        cost = self.message_cost * quantity
        if customer.operators[operator_id] == another_customer.operators[operator_id]:
            discount = self.discount_rate / 100
            cost *= (1 - discount)
            
        customer_bill = self.customer_bills.get(customer.id)
            
        if customer_bill is None:
            # Customer doesn't have a bill, create a new one
            customer_bill = Bill(customer_id=customer.id)
            self.customer_bills[customer.id] = customer_bill
            print(f"New bill for customer {customer.first_name} is created")
            print(f"{customer.first_name} sent {quantity} messages to {another_customer.first_name}.")
        else:
            customer_bill = self.customer_bills[customer.id]
            print(f"{customer.first_name} sent {quantity} messages to {another_customer.first_name}.")  
            
            
        if customer_bill.check(amount=cost):
            allowed_amount = (customer.limiting_amount - customer_bill.current_debt) / self.network_charge
            allowed_cost = allowed_amount * self.network_charge
            customer_bill.add(amount=allowed_cost)
            print(f"But you reached the limit. Operation was interrapted, only {allowed_amount:.2f} messages were available")
        else:
            customer_bill.add(amount=cost)  
            
            
            
            
        