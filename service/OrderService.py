from dao.UserDAO import UserDAO
from dao.OrderDAO import OrderDAO
from dao.ProductDAO import ProductDAO
from model.Order import Order
from model.Product import Product
from model.User import User
from log.log import get_logger

logger = get_logger(__name__)

class OrderService:

    @staticmethod
    def create_order(user_id, product_id, quantity):
        logger.info(f"Attempting to create order: user_id={user_id}, product_id={product_id}, quantity={quantity}")

        # bunch of data check to make sure it is legal to create an order
        if quantity < 1:
            logger.warning(f"Invalid quantity: {quantity}. Quantity must be at least 1.")
            return {"success": False, "message": "Quantity must be at least 1."}

        user = UserDAO.get_user_by_id(user_id)
        if not user:
            logger.warning(f"User not found: user_id={user_id}")
            return {"success": False, "message": "User not found."}

        product = ProductDAO.get_product_by_id(product_id)
        if not product:
            logger.warning(f"Product not found: product_id={product_id}")
            return {"success": False, "message": "Product not found."}

        if product.inventory < quantity:
            logger.warning(f"Insufficient inventory: product_id={product_id}, requested={quantity}, available={product.inventory}")
            return {"success": False, "message": f"Insufficient inventory (Available: {product.inventory})."}

        total_cost = product.price * quantity
        if user.deposit < total_cost:
            logger.warning(f"Insufficient deposit: user_id={user_id}, deposit={user.deposit}, total_cost={total_cost}")
            return {"success": False, "message": "Insufficient deposit."}

        # Update product inventory and user deposit
        logger.info(f"Updating inventory and deposit for transaction: product_id={product_id}, user_id={user_id}")
        ProductDAO.update_inventory_by_id(product_id, product.inventory - quantity)
        UserDAO.update_user_deposit_by_id(user_id, user.deposit - total_cost)

        # Call the transaction method
        # In transaction, update both product inventory and user deposit, and create the order
        # In case database error happened during the process
        logger.info(f"Creating order in transaction: user_id={user_id}, product_id={product_id}, quantity={quantity}")
        order_id = OrderDAO.update_inventory_deposit_and_create_order(
            product_id=product_id,
            new_inventory=product.inventory - quantity,
            user_id=user_id,
            new_deposit=user.deposit - total_cost,
            quantity=quantity
        )
        if not order_id:
            logger.error(f"Transaction failed for order creation: user_id={user_id}, product_id={product_id}")
            return {"success": False, "message": "Failed to process purchase. Transaction rolled back."}

        logger.info(f"Order created successfully: order_id={order_id}")
        return {"success": True, "message": "Purchase successful.", "order_id": order_id}

    @staticmethod
    def get_all_orders():
        logger.info("Fetching all orders from database")
        orders = OrderDAO.get_all_orders()
        orders_dict = []

        for order in orders:
            order_dict = order.to_dict()
            product = ProductDAO.get_product_by_id(order.product_id)  # Get product name
            order_dict["product_name"] = product.name if product else "Unknown"
            orders_dict.append(order_dict)

        if not orders:
            logger.warning("No orders found or database query failed.")
            return {"success": False, "orders": orders_dict, "message": "Database query orders failed."}

        logger.info(f"Fetched {len(orders)} orders successfully.")
        return {"success": True, "orders": orders_dict}

    @staticmethod
    def get_order_by_user_id(user_id):
        logger.info(f"Fetching orders for user_id={user_id}")
        user = UserDAO.get_user_by_id(user_id)
        if not user:
            logger.warning(f"User not found while fetching orders: user_id={user_id}")
            return {"success": False, "message": "Order query failed. User id not exist."}

        orders = OrderDAO.get_orders_by_user_id(user_id)
        orders_dict = []

        for order in orders:
            order_dict = order.to_dict()
            product = ProductDAO.get_product_by_id(order.product_id)  # Get product name
            order_dict["product_name"] = product.name if product else "Unknown"
            orders_dict.append(order_dict)

        logger.info(f"Fetched {len(orders)} orders for user_id={user_id}.")
        return {"success": True, "orders": orders_dict}
