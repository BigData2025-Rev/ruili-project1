class Order:
    def __init__(self, order_id, user_id, product_id, quantity, order_date=None):
        self.id = order_id
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        self.order_date = order_date

    def __repr__(self):
        return (f"Order(id={self.id}, user_id={self.user_id}, product_id={self.product_id}, "
                f"quantity={self.quantity}, order_date={self.order_date})")

    def total_price(self, product_price):
        # count the total price of the order
        return self.quantity * product_price

    def to_dict(self):
        # transfer the object to dict format
        return {
            "id": self.id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "order_date": self.order_date
        }

    @staticmethod
    def from_dict(data):
        # create an order object from the dict
        return Order(
            order_id=data.get('id'),
            user_id=data.get('user_id'),
            product_id=data.get('product_id'),
            quantity=data.get('quantity'),
            order_date=data.get('order_date')
        )
