from fastapi import FastAPI
from typing import List
import hashlib
from dataclasses import dataclass

app = FastAPI()


# Клас CreditCard
class CreditCard:
    def __init__(self, client: str, account_number: str, credit_limit: float, grace_period: int, cvv: str):
        self.client = client
        self.account_number = account_number
        self.credit_limit = credit_limit
        self.grace_period = grace_period
        self._cvv = None
        self.encrypt(cvv)

    @property
    def cvv(self):
        return self._cvv

    @cvv.setter
    def cvv(self, value: str):
        self.encrypt(value)

    def encrypt(self, value: str):
        self._cvv = hashlib.sha256(value.encode()).hexdigest()

    def decrypt(self, hashed_value: str) -> str:
        return hashed_value

    def give_details(self):
        return {
            "client": self.client,
            "account_number": self.account_number,
            "credit_limit": self.credit_limit,
            "grace_period": self.grace_period,
            "cvv": self._cvv
        }


# Клас BankInfo
class BankInfo:
    def __init__(self, bank_name: str, holder_name: str, account_number: str, credit_history: dict):
        self.bank_name = bank_name
        self.holder_name = holder_name
        self.account_number = account_number
        self.credit_history = credit_history

    def transaction_list(self, account_number: str) -> List[str]:
        return self.credit_history.get(account_number, [])


# Клас BankCustomer
@dataclass
class PersonalInfo:
    first_name: str
    last_name: str
    dob: str


class BankCustomer:
    def __init__(self, personal_info: PersonalInfo, bank_details: BankInfo):
        self.personal_info = personal_info
        self.bank_details = bank_details

    def give_details(self):
        details = self.bank_details.transaction_list(self.bank_details.account_number)
        return {
            "personal_info": {
                "first_name": self.personal_info.first_name,
                "last_name": self.personal_info.last_name,
                "dob": self.personal_info.dob
            },
            "bank_details": {
                "bank_name": self.bank_details.bank_name,
                "holder_name": self.bank_details.holder_name,
                "account_number": self.bank_details.account_number,
                "credit_history": self.bank_details.credit_history,
                "transactions": details
            }
        }


# Декоратори для CreditCard
class GoldenCreditCard:
    def __init__(self, credit_card: CreditCard):
        self.credit_card = credit_card

    def give_details(self):
        details = self.credit_card.give_details()
        details["extra_benefits"] = "Golden privileges: Free airport lounge access"
        return details


class CorporateCreditCard:
    def __init__(self, credit_card: CreditCard):
        self.credit_card = credit_card

    def give_details(self):
        details = self.credit_card.give_details()
        details["extra_benefits"] = "Corporate privileges: Business travel discounts"
        return details


# Декоратори для BankCustomer
class VIPCustomer:
    def __init__(self, bank_customer: BankCustomer):
        self.bank_customer = bank_customer

    def give_details(self):
        details = self.bank_customer.give_details()
        details["customer_status"] = "VIP"
        return details


class CorporateCustomer:
    def __init__(self, bank_customer: BankCustomer):
        self.bank_customer = bank_customer

    def give_details(self):
        details = self.bank_customer.give_details()
        details["customer_status"] = "Corporate"
        return details


# Створення великої бази даних для тестування

credit_cards = [
    CreditCard("John Doe", "1234567890123456", 5000.0, 30, "123"),
    CreditCard("Jane Smith", "2345678901234567", 8000.0, 30, "456"),
    CreditCard("Alice Johnson", "3456789012345678", 10000.0, 45, "789"),
    CreditCard("Bob Brown", "4567890123456789", 12000.0, 60, "101"),
    CreditCard("Charlie Davis", "5678901234567890", 15000.0, 90, "202")
]

bank_info = [
    BankInfo("Big Bank", "John Doe", "1234567890123456", {"1234567890123456": ["Payment of $100", "Payment of $50"]}),
    BankInfo("Small Bank", "Jane Smith", "2345678901234567",
             {"2345678901234567": ["Payment of $200", "Payment of $150"]}),
    BankInfo("International Bank", "Alice Johnson", "3456789012345678",
             {"3456789012345678": ["Payment of $300", "Payment of $250"]}),
    BankInfo("Super Bank", "Bob Brown", "4567890123456789",
             {"4567890123456789": ["Payment of $500", "Payment of $100"]}),
    BankInfo("Mega Bank", "Charlie Davis", "5678901234567890",
             {"5678901234567890": ["Payment of $600", "Payment of $400"]})
]

personal_infos = [
    PersonalInfo("John", "Doe", "1980-01-01"),
    PersonalInfo("Jane", "Smith", "1990-02-02"),
    PersonalInfo("Alice", "Johnson", "1992-03-03"),
    PersonalInfo("Bob", "Brown", "1985-04-04"),
    PersonalInfo("Charlie", "Davis", "1978-05-05")
]

bank_customers = [
    BankCustomer(personal_infos[0], bank_info[0]),
    BankCustomer(personal_infos[1], bank_info[1]),
    BankCustomer(personal_infos[2], bank_info[2]),
    BankCustomer(personal_infos[3], bank_info[3]),
    BankCustomer(personal_infos[4], bank_info[4])
]

# Створення екземплярів декораторів для тестування
golden_cards = [GoldenCreditCard(card) for card in credit_cards]
corporate_cards = [CorporateCreditCard(card) for card in credit_cards]
vip_customers = [VIPCustomer(customer) for customer in bank_customers]
corporate_customers = [CorporateCustomer(customer) for customer in bank_customers]


# Тестування через FastAPI ендпоінти
@app.get("/credit_cards")
def get_credit_cards():
    return [card.give_details() for card in credit_cards]


@app.get("/bank_customers")
def get_bank_customers():
    return [customer.give_details() for customer in bank_customers]


@app.get("/golden_credit_cards")
def get_golden_credit_cards():
    return [card.give_details() for card in golden_cards]


@app.get("/corporate_credit_cards")
def get_corporate_credit_cards():
    return [card.give_details() for card in corporate_cards]


@app.get("/vip_customers")
def get_vip_customers():
    return [customer.give_details() for customer in vip_customers]


@app.get("/corporate_customers")
def get_corporate_customers():
    return [customer.give_details() for customer in corporate_customers]
