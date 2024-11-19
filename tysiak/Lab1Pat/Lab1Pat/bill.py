class Bill:
    """Bill class to track customer spending."""

    def __init__(self, limiting_amount: float) -> None:
        """
        Initialize a Bill object with a limiting amount and a current debt of zero.
        
        Args:
            limiting_amount (float): The maximum debt allowed for the customer.
        """
        self.limiting_amount = limiting_amount
        self.current_debt = 0.0

    def check(self, amount: float) -> bool:
        """
        Check if the current debt after adding the specified amount exceeds the limit.

        Args:
            amount (float): The amount to be checked.

        Returns:
            bool: True if the amount can be added without exceeding the limit.
        """
        return (self.current_debt + amount) <= self.limiting_amount

    def add(self, amount: float) -> None:
        """
        Add an amount to the current debt if the limit is not exceeded.

        Args:
            amount (float): The amount to add.
        """
        if self.check(amount):
            self.current_debt += round(amount, 2) 
            print(f"Amount {round(amount, 2)} added. New debt: {round(self.current_debt, 2)}")
        else:
            print(f"Cannot add amount {round(amount, 2)}. Limit exceeded.")

    def pay(self, amount: float) -> None:
        """
        Pay off an amount from the current debt.

        Args:
            amount (float): The amount to be paid.
        """
        self.current_debt -= round(amount, 2)  
        if self.current_debt < 0:
            self.current_debt = 0.0
        print(f"Paid {round(amount, 2)}. Remaining debt: {round(self.current_debt, 2)}")

    def change_limit(self, amount: float) -> None:
        """
        Change the debt limit.

        Args:
            amount (float): The new limit amount.
        """
        self.limiting_amount = round(amount, 2)
        print(f"New limit set: {self.limiting_amount}")
