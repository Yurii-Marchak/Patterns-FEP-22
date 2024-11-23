class BankCustomer:
    def __init__(self, name: str, bank_info: BankInfo):
        self.name = name
        self.bank_info = bank_info

    def give_details(self):
        return {
            'name': self.name,
            'bank_info': self.bank_info.give_details()  
        }

