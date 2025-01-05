class Product:
    def __init__(self, product_id, name, price, inventory, category=None, description=None):
        self.id = product_id
        self.name = name
        self.price = price
        self.inventory = inventory
        self.category = category
        self.description = description

    def __repr__(self):
        # string format of the product
        return (f"Product(id={self.id}, name={self.name}, price={self.price}, "
                f"inventory={self.inventory}, category={self.category})")

    def is_in_stock(self):
        # check if inventory greater than 0
        return self.inventory > 0

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "inventory": self.inventory,
            "category": self.category,
            "description": self.description
        }

    @staticmethod
    def from_dict(data):
        return Product(
            product_id=data.get('id'),
            name=data.get('name'),
            price=data.get('price'),
            inventory=data.get('inventory'),
            category=data.get('category'),
            description=data.get('description')
        )
