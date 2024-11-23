
class Shipment:
    def __init__(self):
        self.shipments = {}

    def create_shipment(self, order_id, address):
        self.shipments[order_id] = address

    def ship_order(self, order_id):
        if order_id in self.shipments:
            print(f"Order {order_id} shipped to {self.shipments[order_id]}")
