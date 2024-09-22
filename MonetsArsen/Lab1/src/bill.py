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
    """
    Represents a customer's bill with methods for debt management.

    This class provides functionality to track and manage a customer's debt,
    including adding charges, making payments, and checking against a debt limit.
    """

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
        self._is_reached_limit: bool = False
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
            print(f"Current limit {self.limiting_amount} has been exceeded by {temp_value - self.limiting_amount}")
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
        if not self.check(amount):
            self._is_reached_limit = False
            self.current_debt += amount
        else:
            self._is_reached_limit = True

    def pay(self, amount: float) -> None:
        """
        Process a payment to reduce the current debt.

        If the payment amount is greater than the current debt,
        the debt is set to zero.

        Args:
            amount (float): The payment amount to be subtracted from the current debt.

        Returns:
            None
        """
        self.current_debt = max(0.0, self.current_debt - amount)

    def change_limit(self, amount: float) -> None:
        """
        Change the limiting amount for the bill.

        Args:
            amount (float): The new limiting amount.

        Returns:
            None

        Prints:
            A message confirming the new limit.
        """
        self.limiting_amount = amount
        print(f"Limit has changed to {self.limiting_amount}")

    def is_reached_limit(self) -> bool:
        """
        Check if the debt limit has been reached.

        Returns:
            bool: True if the limit has been reached, False otherwise.
        """
        return self._is_reached_limit