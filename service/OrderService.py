from dao.UserDAO import UserDAO
from dao.OrderDAO import OrderDAO
from dao.ProductDAO import ProductDAO
from model.Order import Order
from model.Product import Product
from model.User import User
from log.log import get_logger

class OrderService:
    
    @staticmethod
    def create_order(user_id, product_id, quantity):
        # bunch of data check to make sure it is legal to create an order
        if quantity < 1:
            return {"success": False, "message": "Quantity must be at least 1."}
        user = UserDAO.get_user_by_id(user_id)
        if not user:
            return {"success": False, "message": "User not found."}
        product = ProductDAO.get_product_by_id(product_id)
        if not product:
            return {"success": False, "message": "Product not found."}
        if product.inventory < quantity:
            return {"success": False, "message": f"Insufficient inventory (Available: {product.inventory})."}
        total_cost = product.price * quantity
        if user.deposit < total_cost:
            return {"success": False, "message": "Insufficient deposit."}
        
        # update product inventory and user despoist
        ProductDAO.update_inventory_by_id(product_id, product.inventory - quantity)
        UserDAO.update_user_deposit_by_id(user_id, user.deposit - total_cost)

        # call the transaction method
        # in transaction, update both product inventory and user deposit, and create the order
        # in case database error happened during the process
        order_id = OrderDAO.update_inventory_deposit_and_create_order(
            product_id=product_id,
            new_inventory=product.inventory - quantity,
            user_id=user_id,
            new_deposit=user.deposit - total_cost,
            quantity=quantity
        )
        if not order_id:
            return {"success": False, "message": "Failed to process purchase. Transaction rolled back."}

        return {"success": True, "message": "Purchase successful.", "order_id": order_id}


    @staticmethod
    def get_all_orders():
        orders = OrderDAO.get_all_orders()
        orders_dict = []
        for order in orders:
            order_dict = order.to_dict()
            product = ProductDAO.get_product_by_id(order.product_id)  # get product name
            order_dict["product_name"] = product.name if product else "Unknown"
            orders_dict.append(order_dict)

        if not orders:
            return {"success": False, "orders": orders_dict, "message": "Database query orders failed."}
        return {"success": True, "orders": orders_dict}

    @staticmethod
    def get_order_by_user_id(user_id):
        user = UserDAO.get_user_by_id(user_id)
        if not user:
            return {"success": False, "message": "Order query failed. User id not exist."}

        orders = OrderDAO.get_orders_by_user_id(user_id)
        orders_dict = []
        for order in orders:
            order_dict = order.to_dict()
            product = ProductDAO.get_product_by_id(order.product_id)  # get product name
            order_dict["product_name"] = product.name if product else "Unknown"
            orders_dict.append(order_dict)

        return {"success": True, "orders": orders_dict}

