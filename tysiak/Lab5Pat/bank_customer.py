from dataclasses import dataclass

@dataclass
class PersonalInfo:
    name: str
    age: int

class BankCustomer:
    def __init__(self, personal_info, bank_details):
        self.personal_info = personal_info
        self.bank_details = bank_details
    
    def give_details(self):
        details = {
            "personal_info": vars(self.personal_info),
            "bank_details": {
                "bank_name": self.bank_details.bank_name,
                "holder_name": self.bank_details.holder_name,
                "accounts_number": self.bank_details.accounts_number,
                "credit_history": self.bank_details.credit_history,
                "transactions": {
                    acc: self.bank_details.transaction_list(acc) for acc in self.bank_details.accounts_number
                }
            }
        }
        return details

class IndividualCustomer(BankCustomer):
    def __init__(self, personal_info, bank_details):
        super().__init__(personal_info, bank_details)
        self.individual_benefit = "Free ATM withdrawals"
    
    def give_details(self):
        details = super().give_details()
        details["individual_benefit"] = self.individual_benefit
        return details

class VIPCustomer(BankCustomer):
    def __init__(self, personal_info, bank_details):
        super().__init__(personal_info, bank_details)
        self.vip_support = "24/7 Personal Account Manager"
    
    def give_details(self):
        details = super().give_details()
        details["vip_support"] = self.vip_support
        return details
