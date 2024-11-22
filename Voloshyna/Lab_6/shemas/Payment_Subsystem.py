
class Payment:
    def __init__(self):
        self.card_details = {}

    def add_card_details(self, card_info):
        self.card_details = card_info

    def process_payment(self, payment_info):
        # Dummy implementation for payment processing
        return True
