
class ShoppingCart:
    def __init__(self):
        self.cart_items = {}

    def add_item(self, product_id, quantity):
        self.cart_items[product_id] = quantity

    def update_quantity(self, product_id, new_quantity):
        if product_id in self.cart_items:
            self.cart_items[product_id] = new_quantity

    def checkout(self, stock_items: dict):
        for product_id, quantity in self.cart_items.items():
            if product_id not in stock_items or stock_items[product_id] < quantity:
                return False
        return True

class Order:
    def __init__(self):
        self.orders = {}
        self.next_order_id = 1

    def create_order(self, cart, customer_info):
        order_id = self.next_order_id
        self.next_order_id += 1
        self.orders[order_id] = {
            "cart": cart,
            "customer_info": customer_info
        }
        return order_id
