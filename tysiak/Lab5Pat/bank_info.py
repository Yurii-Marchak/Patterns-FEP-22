class BankInfo:
    def __init__(self, bank_name, holder_name, accounts_number, credit_history):
        self.bank_name = bank_name
        self.holder_name = holder_name
        self.accounts_number = accounts_number
        self.credit_history = credit_history
    
    def transaction_list(self, account_number):
        return ["Transaction1", "Transaction2", "Transaction3"]
