
class OrderFacade:
    def __init__(self, inventory_system, order_system, payment_system, shipment_system):
        self.inventory = inventory_system
        self.order = order_system
        self.payment = payment_system
        self.shipment = shipment_system

    def process_order(self, customer, order_details):
        # Check if the product is in stock
        if not self.inventory.select_stock_item(order_details['product_id']):
            raise Exception("Product out of stock")

        # Process the payment
        if not self.payment.process_payment(order_details['payment_info']):
            raise Exception("Payment failed")

        # Create an order
        self.order.create_order(customer, order_details)

        # Ship the order
        self.shipment.ship_order(order_details['order_id'])

        return "Order processed successfully"
