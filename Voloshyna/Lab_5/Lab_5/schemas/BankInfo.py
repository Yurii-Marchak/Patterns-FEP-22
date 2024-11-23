class BankInfo:
    def __init__(self, bank_name: str, holder_name: str, accounts_number: list, credit_history: dict):
        self.bank_name = bank_name
        self.holder_name = holder_name
        self.accounts_number = accounts_number
        self.credit_history = credit_history

    def add_account(self, credit_card_adapter):
        account_number = credit_card_adapter.get_account_number()
        credit_info = credit_card_adapter.get_credit_info()
        self.accounts_number.append(account_number)
        self.credit_history[account_number] = credit_info
