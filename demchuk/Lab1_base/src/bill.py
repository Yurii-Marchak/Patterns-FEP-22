class Bill:
    """
    The Bill class represents a customer's billing information, including debt management
    and payment limits. It tracks the current debt and ensures that it does not exceed
    a specified limiting amount.
    """

    def __init__(self, customer_id: int, limiting_amount: float = 100) -> None:
        """
        Initializes a Bill instance for a specific customer.

        Args:
            customer_id (int): The unique identifier of the customer.
            limiting_amount (float, optional): The maximum allowed debt before restrictions apply. Default is 100.
        """
        self.limiting_amount: float = limiting_amount
        self.current_debt: float = 0.0
        self.customer_id: int = customer_id

    def check(self, amount: float) -> bool:
        """
        Checks if adding a specified amount to the current debt will exceed the limiting amount.

        Args:
            amount (float): The amount to be added to the current debt.

        Returns:
            bool: True if the new debt exceeds the limiting amount, False otherwise.
        """
        temp_value = self.current_debt + amount
        if temp_value >= self.limiting_amount:
            print(f"Limit {self.limiting_amount} reached, remaining {self.limiting_amount - temp_value}")
            return True
        return False

    def add(self, amount: float) -> None:
        """
        Adds a specified amount to the current debt if it does not exceed the limiting amount.

        Args:
            amount (float): The amount to be added to the current debt.
        """
        if not self.check(amount):
            self.current_debt += amount

    def pay(self, amount: float) -> None:
        """
        Pays off a portion or all of the current debt. If the payment exceeds the current debt,
        the limiting amount is adjusted accordingly.

        Args:
            amount (float): The amount to be paid off from the current debt.
        """
        temp_value = self.current_debt - amount
        if temp_value < 0:
            self.limiting_amount += temp_value
        self.current_debt = 0.0

    def change_limit(self, amount: float) -> None:
        """
        Changes the limiting amount to a new specified value.

        Args:
            amount (float): The new limiting amount to be set.
        """
        self.limiting_amount = amount
