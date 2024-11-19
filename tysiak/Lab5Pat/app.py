from flask import Flask, jsonify
from credit_card import CreditCard, GoldenCreditCard, CorporateCreditCard
from bank_info import BankInfo
from bank_customer import PersonalInfo, BankCustomer, IndividualCustomer, VIPCustomer

app = Flask(__name__)

credit_card = CreditCard("Sara Maas", "1234567890", 5000.0, 30, "123")
golden_card = GoldenCreditCard("Sara Maas", "0987654321", 7000.0, 45, "456")
corporate_card = CorporateCreditCard("Company ABC", "1122334455", 20000.0, 60, "789")

personal_info = PersonalInfo("Lily Smith", 30)
bank_info = BankInfo("Bank of World", "Lily Smith", ["1234567890"], {"1234567890": "Good"})
customer = BankCustomer(personal_info, bank_info)
individual_customer = IndividualCustomer(personal_info, bank_info)
vip_customer = VIPCustomer(personal_info, bank_info)

@app.route('/', methods=['GET'])
def index():
    return "API is working!"

@app.route('/credit_card', methods=['GET'])
def get_credit_card():
    return jsonify(credit_card.give_details())

@app.route('/golden_card', methods=['GET'])
def get_golden_card():
    return jsonify(golden_card.give_details())

@app.route('/corporate_card', methods=['GET'])
def get_corporate_card():
    return jsonify(corporate_card.give_details())

@app.route('/customer', methods=['GET'])
def get_customer():
    return jsonify(customer.give_details())

@app.route('/individual_customer', methods=['GET'])
def get_individual_customer():
    return jsonify(individual_customer.give_details())

@app.route('/vip_customer', methods=['GET'])
def get_vip_customer():
    return jsonify(vip_customer.give_details())

if __name__ == '__main__':
    app.run(debug=True)
