from flask import Flask, jsonify, request
from pymongo import MongoClient
from typing import List
from dataclasses import dataclass
import hashlib

# Підключення до MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["banking_system"]
credit_cards_collection = db["credit_cards"]
bank_customers_collection = db["bank_customers"]

# CreditCard class with MongoDB integration
class CreditCard:
    def __init__(self, client: str, account_number: str, credit_limit: float, grace_period: int, cvv: str):
        self.client = client
        self.account_number = account_number
        self.credit_limit = credit_limit
        self.grace_period = grace_period
        self._cvv = self.encrypt(cvv)

    @property
    def cvv(self):
        return self.decrypt(self._cvv)

    @cvv.setter
    def cvv(self, value: str):
        self._cvv = self.encrypt(value)

    def encrypt(self, value: str) -> str:
        return hashlib.sha256(value.encode()).hexdigest()

    def decrypt(self, value: str) -> str:
        return value  # Хешовані дані не можна розшифрувати.

    def save_to_db(self):
        credit_cards_collection.insert_one(self.give_details())

    def give_details(self) -> dict:
        return {
            "client": self.client,
            "account_number": self.account_number,
            "credit_limit": self.credit_limit,
            "grace_period": self.grace_period,
            "cvv": self._cvv,
        }

# BankInfo class
class BankInfo:
    def __init__(self, bank_name: str, holder_name: str, accounts_number: List[str]):
        self.bank_name = bank_name
        self.holder_name = holder_name
        self.accounts_number = accounts_number
        self.credit_history = {}

    def transaction_list(self, account_number: str) -> List[str]:
        return ["Transaction1", "Transaction2", "Transaction3"]

    def give_details(self) -> dict:
        return {
            "bank_name": self.bank_name,
            "holder_name": self.holder_name,
            "accounts_number": self.accounts_number,
            "credit_history": self.credit_history,
        }

# BankCustomer class with MongoDB integration
@dataclass
class PersonalInfo:
    name: str
    email: str

class BankCustomer:
    def __init__(self, personal_info: PersonalInfo, bank_details: BankInfo):
        self.personal_info = personal_info
        self.bank_details = bank_details

    def save_to_db(self):
        bank_customers_collection.insert_one(self.give_details())

    def give_details(self) -> dict:
        return {
            "personal_info": {
                "name": self.personal_info.name,
                "email": self.personal_info.email,
            },
            "bank_details": self.bank_details.give_details(),
        }

# Flask REST API
app = Flask(__name__)

@app.route('/credit_card', methods=['POST'])
def create_credit_card():
    data = request.json
    card = CreditCard(
        client=data['client'],
        account_number=data['account_number'],
        credit_limit=data['credit_limit'],
        grace_period=data['grace_period'],
        cvv=data['cvv'],
    )
    card.save_to_db()
    return jsonify({"message": "Credit card saved successfully!", "details": card.give_details()}), 201

@app.route('/bank_customer', methods=['POST'])
def create_bank_customer():
    data = request.json
    personal_info = PersonalInfo(name=data['name'], email=data['email'])
    bank_details = BankInfo(
        bank_name=data['bank_name'],
        holder_name=data['holder_name'],
        accounts_number=data['accounts_number'],
    )
    customer = BankCustomer(personal_info=personal_info, bank_details=bank_details)
    customer.save_to_db()
    return jsonify({"message": "Bank customer saved successfully!", "details": customer.give_details()}), 201

@app.route('/credit_cards', methods=['GET'])
def get_credit_cards():
    cards = list(credit_cards_collection.find({}, {"_id": 0}))  # Витягуємо всі картки без ObjectId
    return jsonify(cards), 200

@app.route('/bank_customers', methods=['GET'])
def get_bank_customers():
    customers = list(bank_customers_collection.find({}, {"_id": 0}))  # Витягуємо всіх клієнтів без ObjectId
    return jsonify(customers), 200

if __name__ == '__main__':
    app.run(debug=True)
