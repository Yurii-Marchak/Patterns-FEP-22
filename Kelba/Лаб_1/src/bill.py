class Bill:
    """Represents a customer's bill with methods for debt management."""

    def __init__(self, limiting_amount: float) -> None:
        """
        Initialize a Bill object.

        Args:
            limiting_amount (float): The maximum allowable debt.

        Returns:
            None
        """
        self.limiting_amount: float = limiting_amount
        self.current_debt: float = 0.0

    def check(self, amount: float) -> bool:
        """
        Check if adding the given amount would exceed the limiting amount.

        Args:
            amount (float): The amount to be added to the current debt.

        Returns:
            bool: True if the limit would be exceeded, False otherwise.
        """
        temp_value = self.current_debt + amount
        if temp_value >= self.limiting_amount:
            print(f"Current limit {self.limiting_amount} has been reached by {self.limiting_amount - temp_value}")
            return True
        return False

    def add(self, amount: float) -> None:
        """
        Add the given amount to the current debt if it doesn't exceed the limit.

        Args:
            amount (float): The amount to be added to the current debt.

        Returns:
            None
        """
        if not self.check(amount):
            self.current_debt += amount

    def pay(self, amount: float) -> None:
        """
        Pay a portion of the debt.

        Args:
            amount (float): The amount to be paid.

        Returns:
            None
        """
        temp_value = self.current_debt - amount
        if temp_value < 0:
            self.limiting_amount += temp_value
        self.current_debt = max(0.0, self.current_debt - amount)

    def change_limit(self, amount: float) -> None:
        """
        Change the limit of the bill.

        Args:
            amount (float): The new limit value.

        Returns:
            None
        """
        self.limiting_amount = amount

    def get_limiting_amount(self) -> float:
        """Get the current limiting amount."""
        return self.limiting_amount

    def get_current_debt(self) -> float:
        """Get the current debt."""
        return self.current_debt
