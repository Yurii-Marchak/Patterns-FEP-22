from cryptography.fernet import Fernet

class CreditCard:
    def __init__(self, client, account_number, credit_limit, grace_period, cvv):
        self.client = client
        self.account_number = account_number
        self.credit_limit = credit_limit
        self.grace_period = grace_period
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
        self._cvv = self.encrypt(cvv)
    
    @property
    def cvv(self):
        return self.decrypt(self._cvv)
    
    @cvv.setter
    def cvv(self, value):
        self._cvv = self.encrypt(value)
    
    def encrypt(self, value):
        encrypted_value = self.cipher_suite.encrypt(value.encode())
        return encrypted_value
    
    def decrypt(self, value):
        decrypted_value = self.cipher_suite.decrypt(value).decode()
        return decrypted_value
    
    def give_details(self):
        return {
            "client": self.client,
            "account_number": self.account_number,
            "credit_limit": self.credit_limit,
            "grace_period": self.grace_period,
            "cvv": self.cvv
        }

class GoldenCreditCard(CreditCard):
    def __init__(self, client, account_number, credit_limit, grace_period, cvv):
        super().__init__(client, account_number, credit_limit, grace_period, cvv)
        self.additional_limit = 10000
    
    def give_details(self):
        details = super().give_details()
        details["additional_limit"] = self.additional_limit
        return details

class CorporateCreditCard(CreditCard):
    def __init__(self, client, account_number, credit_limit, grace_period, cvv):
        super().__init__(client, account_number, credit_limit, grace_period, cvv)
        self.corporate_discount = 5  # 5%
    
    def give_details(self):
        details = super().give_details()
        details["corporate_discount"] = self.corporate_discount
        return details
