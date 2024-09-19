"""
Bill Management Module

This module provides functionality for managing customer bills, including
debt tracking, limit checking, and payment processing.

Classes:
    Bill: Represents a customer's bill with methods for debt management.

Example:
    bill = Bill(customer_id=123, limiting_amount=500)
    bill.add(100)
    bill.pay(50)
"""

class Bill:
    """Docstring"""

    def __init__(self, customer_id: int, limiting_amount: float = 100) -> None:
        """
        Initialize a Bill object.

        Args:
            customer_id (int): The unique identifier for the customer.
            limiting_amount (float, optional): The maximum allowable debt. Defaults to 100.

        Returns:
            None
        """
        self.limiting_amount: float = limiting_amount
        self.current_debt: float = 0.0
        self.customer_id: int = customer_id

    def check(self, amount: float) -> bool:
        """
        Check if adding the given amount would exceed the limiting amount.

        Args:
            amount (float): The amount to be added to the current debt.

        Returns:
            bool: True if the limit would be exceeded, False otherwise.

        Prints:
            A message indicating by how much the limit has been exceeded, if applicable.
        """
        temp_value = self.current_debt + amount
        if temp_value > self.limiting_amount:
            return True
        return False

    def add(self, amount: float) -> None:
        """
        Add the given amount to the current debt if it doesn't exceed the limit.

        This method first checks if adding the amount would exceed the limiting amount.
        If not, it adds the amount to the current debt.

        Args:
            amount (float): The amount to be added to the current debt.

        Returns:
            None

        Note:
            This method does not return any value, but it may modify the `current_debt`
            attribute of the object if the check passes.
        """
     
        if self.check(amount):
            allowed_amount = self.limiting_amount - self.current_debt
            self.current_debt += allowed_amount
            
        else:
            self.current_debt += amount
            print(f"Added {amount:.2f} to the current debt.")
            
    
    
    def pay(self, amount: float) -> None:
        if amount >= self.current_debt:
            difference = amount - self.current_debt
            self.current_debt = 0.0
            if difference > 0:
                print(f"Debt is paid off. Change returned: {difference:.2f}")
            else:
                print("Debt is paid off.")
        else:
        
            self.current_debt -= amount
            print(f"Remaining debt: {self.current_debt:.2f}")


    def change_limit(self, amount: float) -> None:
        """    
        Changes the spending limit on the customer's bill.

        Args:
            amount (float): The new spending limit for the customer.

        Returns:
            None
        """
        self.limiting_amount = amount
        print(f"New limit for customer {self.customer_id} is set to {self.limiting_amount}")