
from cryptography.fernet import Fernet

class CreditCardAdapter:
    def __init__(self, credit_card):
        self.credit_card = credit_card

    def get_account_number(self):
        return self.credit_card.account_number

    def get_credit_info(self):
        details = self.credit_card.give_details()
        return {
            'credit_limit': details['credit_limit'],
            'grace_period': details['grace_period']
        }
        

    @property
    def cvv(self):
        return self.decrypt(self._cvv, self.encryption_key)

    @cvv.setter
    def cvv(self, value):
        self._cvv = self.encrypt(value, self.encryption_key)

    def give_details(self) -> dict:
        return {
            "client": self.client,
            "account_number": self.account_number,
            "credit_limit": self.credit_limit,
            "grace_period": self.grace_period,
            "cvv": self.cvv,
        }

    def encrypt(self, value: str, encryption_key: bytes) -> bytes:
        cipher = Fernet(encryption_key)
        encrypted_value = cipher.encrypt(value.encode())
        return encrypted_value

    def decrypt(self, encrypted_value: bytes, encryption_key: bytes) -> str:
        cipher = Fernet(encryption_key)
        decrypted_value = cipher.decrypt(encrypted_value)
        return decrypted_value.decode()
    
"""
    Encrypts a string value using the specified encryption key.
    
    Args:
        value (str): The string value to be encrypted.
        encryption_key (bytes): The encryption key to use for encryption, 
                                which should be a valid Fernet key.

    Returns:
        bytes: The encrypted value in bytes.
"""

class GoldenCreditCardDecorator(CreditCard):
    def give_details(self) -> dict:
        details = super().give_details()
        details['card_type'] = 'Golden'
        return details

class CorporateCreditCardDecorator(CreditCard):
    def give_details(self) -> dict:
        details = super().give_details()
        details['card_type'] = 'Corporate'
        return details
