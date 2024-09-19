class Bill:
    """
    A class to represent a bill for a customer, with functionality to manage
    debt, payments, and limit changes.
    
    Attributes:
    ----------
    limitingAmount : float
        The maximum amount that the debt can reach.
    currentDebt : float
        The current debt amount.
    """
    def __init__(self, limitingAmount: float = 100) -> None:
        self.limitingAmount: float = limitingAmount
        self.currentDebt: float = 0.0
        
    def check(self, amount: float) -> bool:
        """
        Checks if adding a specific amount will exceed the limit.

        Parameters:
        ----------
        amount : float
            The amount to check against the current debt.
        
        Returns:
        -------
        bool
            True if the new debt exceeds the limit, False otherwise.
        """
        if self.currentDebt + amount > self.limitingAmount:
            return True
        return False
    
    def add(self, amount: float) -> None:
        """
        Adds an amount to the current debt if it doesn't exceed the limit.

        Parameters:
        ----------
        amount : float
            The amount to be added to the current debt.
        """
        if not self.check(amount):
            self.currentDebt += amount
            print(f'Added: {amount:.2f}. Current Debt: {self.currentDebt:.2f}')
        else:
            print(f"Unable to add {amount:.2f}. Limit exceeded!")
    
    def pay(self, amount: float) -> None:
        """
        Pays off a specified amount of the current debt.

        Parameters:
        ----------
        amount : float
            The amount to be paid off the current debt.
        """
        if amount >= self.currentDebt:
            difference = amount - self.currentDebt
            self.currentDebt = 0.0
            print(f'Current debt: {self.currentDebt}. Excess {difference:.2f}')
        else:
            self.currentDebt -= amount
            print(f'Current debt: {self.currentDebt:.2f}')
    
    def changeTheLimit(self, amount: float) -> None:
        """
        Adjusts the limiting amount for the bill.

        Parameters:
        ----------
        amount : float
            The amount to adjust the limit by. The limit cannot be negative.
        """
        if self.limitingAmount + amount > 0:
            self.limitingAmount += amount
            print(f'Limit Changed. Current limit: {self.limitingAmount}')
        else:
            print(f"The limit cannot be negative")
    
