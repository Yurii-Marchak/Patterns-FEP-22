from bill import Bill
from typing import TYPE_CHECKING, Dict, Self
if TYPE_CHECKING:   
    from customer import Customer

class Operator:
    """
    A class to represent an operator, responsible for calculating costs for 
    talking, messaging, and network services based on customer usage.

    Attributes:
    ----------
    id : int
        The unique identifier for the operator.
    talkingCharge : float
        The cost per minute for talking.
    messageCost : float
        The cost per message.
    networkCharge : float
        The cost per megabyte of network usage.
    discountRate : float
        The discount rate applied for certain customers (e.g., children or seniors).
    customers_bills : Dict[int, Bill]
        A dictionary storing customer bills, mapping customer IDs to Bill objects.
    """
    def __init__(self, id: int, talkingCharge: float, messageCost: float,
                networkCharge: float, discountRate: float) -> None:
        self.id: int = id
        self.talkingCharge: float = talkingCharge
        self.messageCost: float = messageCost
        self.networkCharge: float = networkCharge
        self.discountRate: float = discountRate
        self.customers_bills: Dict[int, Bill] = {}
        
    def _check_if_customer_have_bill(self, customer_id = int) -> bool:
        """
        Checks if a customer already has a bill with the operator.

        Parameters:
        ----------
        customer_id : int
            The unique identifier of the customer.
        
        Returns:
        -------
        bool
            True if the customer has a bill, False otherwise.
        """
        if self.customers_bills.get(customer_id):
            return True
        else:
            return False

    def calculateTalkingCost(self, minute: int, customer: 'Customer') -> None:
        """
        Calculates the cost for talking services based on the duration and applies 
        discounts based on the customer's age.

        Parameters:
        ----------
        minute : int
            The number of minutes the customer talks.
        customer : Customer
            The customer using the talking service.
        """
        if customer.age < 18 or customer.age > 65:
            total_cost = minute * (self.talkingCharge * (1 - self.discountRate / 100))
        else:
            total_cost = minute * self.talkingCharge
            
        if not self._check_if_customer_have_bill(customer.id):
            customer_bill = Bill(limitingAmount=customer.limitingAmount)
            self.customers_bills[customer.id] = customer_bill
            print(f'New Bill for {customer.name} is created.')
        else:
            customer_bill = self.customers_bills[customer.id]
        
        if customer_bill.check(total_cost):
            affordable_minute = (customer.limitingAmount - customer_bill.currentDebt) / self.talkingCharge
            affordable_cost = affordable_minute * self.talkingCharge
            customer_bill.add(amount=affordable_cost)
            print(f"{customer.name}'s call is cut off after {affordable_minute} minutes due to reaching the limit.")
        else:
            customer_bill.add(amount=total_cost)
            print(f'{customer.name} has talked for {minute} minutes')
    
    def calculateMessageCost(self, quantity: int, customer: 'Customer', other_customer: 'Customer', operator2: Self) -> None:
        """
        Calculates the cost for messaging services based on the quantity of messages sent.
        Discounts are applied if both customers use the same operator.

        Parameters:
        ----------
        quantity : int
            The number of messages sent.
        customer : Customer
            The customer sending the messages.
        other_customer : Customer
            The customer receiving the messages.
        operator2 : Operator
            The operator used by the receiving customer.
        """
        if self.id == operator2.id:
            total_cost = quantity * (self.messageCost * (1 - self.discountRate / 100))
        else:
            total_cost = quantity * self.messageCost
            
        if not self._check_if_customer_have_bill(customer.id):
            customer_bill = Bill(limitingAmount=customer.limitingAmount)
            self.customers_bills[customer.id] = customer_bill
            print(f'New Bill for {customer.name} is created')
        else:
            customer_bill = self.customers_bills[customer.id]
        
        if customer_bill.check(total_cost):
            affordable_messages = (customer.limitingAmount - customer_bill.currentDebt) // self.messageCost
            affordable_cost = affordable_messages * self.messageCost
            customer_bill.add(amount=affordable_cost)
            print(f'Only {affordable_messages:.2f} messages can be sent. Added {affordable_cost:.2f} to the bill.')
        else:
            customer_bill.add(amount=total_cost)
            print(f'{customer.name} has sent {quantity} messages to {other_customer.name}')

    def calculateNetworkCost(self, amount: float, customer='Customer'):
        """
        Calculates the cost for network usage based on the amount of data consumed in megabytes.

        Parameters:
        ----------
        amount : float
            The amount of data used in megabytes.
        customer : Customer
            The customer using the network service.
        """
        total_cost = amount * self.networkCharge
        if not self._check_if_customer_have_bill(customer.id):
            customer_bill = Bill(limitingAmount=customer.limitingAmount)
            self.customers_bills[customer.id] = customer_bill
            print(f'New Bill for {customer.name} is created')
        else:
            customer_bill = self.customers_bills[customer.id]
        
        if customer_bill.check(total_cost):
            affordable_MB = (customer.limitingAmount - customer_bill.currentDebt) / self.networkCharge
            affordable_cost = affordable_MB * self.networkCharge
            customer_bill.add(amount=affordable_cost)
            print(f'Only {affordable_MB:.2f} MB can be used. Added {affordable_cost:.2f} to the bill.')
        else:
            customer_bill.add(amount=total_cost)
            print(f'{customer.name} has used {amount:.2f} MB of network services.')

        

    