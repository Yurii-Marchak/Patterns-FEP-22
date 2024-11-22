
class Stock:
    def __init__(self):
        self.stock_items = {}

    def select_stock_item(self, product_id):
        return product_id in self.stock_items

    def update_stock(self, product_id, quantity : int):
        self.stock_items[product_id] = quantity
