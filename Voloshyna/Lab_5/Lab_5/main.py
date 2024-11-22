
from fastapi import FastAPI
from Modified_Credit_Cart import GoldenCreditCardDecorator, CorporateCreditCardDecorator
from Modified_BankInfo import BankInfo
from Modified_BankCustomer import BankCustomer
from Modified_fernet import Fernet

app = FastAPI()


encryption_key = Fernet.generate_key()

golden_card = GoldenCreditCardDecorator(
    client="John Doe",
    account_number="1234567890123456",
    credit_limit=5000.0,
    grace_period=30,
    cvv="123",
    encryption_key=encryption_key
)

corporate_card = CorporateCreditCardDecorator(
    client="Jane Doe",
    account_number="9876543210987654",
    credit_limit=7000.0,
    grace_period=45,
    cvv="456",
    encryption_key=encryption_key
)

# Creating a BankInfo instance
bank_info = BankInfo(
    bank_name="My Bank",
    holder_name="John Doe",
    accounts_number=[],
    credit_history={}
)


# golden_adapter (CreditCardAdapter): Adapter that transforms the GoldenCreditCardDecorator interface 
# to work with the BankInfo class, providing access to the main card data in a format compatible with BankInfo.

# corporate_adapter (CreditCardAdapter): Adapter that transforms the CorporateCreditCardDecorator interface 
# to work with the BankInfo class, providing access to the main card data in a format compatible with BankInfo.


golden_adapter = CreditCardAdapter(golden_card)
corporate_adapter = CreditCardAdapter(corporate_card)

bank_info.add_account(golden_adapter)
bank_info.add_account(corporate_adapter)


bank_customer = BankCustomer("John Doe", bank_info)

@app.get("/")
async def read_root():
    return {"message": "Hello, welcome to the FastAPI application!"}

@app.get("/bank_customer")
async def get_bank_customer():
    return {"bank_customer_details": bank_customer.give_details()}
