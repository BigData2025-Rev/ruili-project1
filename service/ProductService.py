import bcrypt
import jwt
from dao.UserDAO import UserDAO
from model.Product import Product
from dao.ProductDAO import ProductDAO
from datetime import datetime, timedelta, timezone
from config.config import Config
from log.log import get_logger

logger = get_logger(__name__)

class ProductService:

    @staticmethod
    def get_all_products():
        logger.info("Fetching all products from database.")
        products = [product.to_dict() for product in ProductDAO.get_all_products()]
        if not products:
            logger.warning("No products found or database query failed.")
        else:
            logger.info(f"Fetched {len(products)} products successfully.")
        return {"success": True, "products": products}

    @staticmethod
    def add_product(product):
        logger.info(f"Attempting to add new product: {product.get('name', 'Unknown Name')}")
        product = Product(
            product_id=None,  # id generated by database
            name=product['name'],
            price=product['price'],
            inventory=product['inventory'],
            category=product['category'],  # can be empty
            description=product['description']  # can be empty
        )
        product_id = ProductDAO.create_product(product)
        if product_id is None:
            logger.error(f"Failed to add product: {product.name}")
            return {"success": False, "message": "Product insert failed."}
        logger.info(f"Product added successfully with ID: {product_id}")
        return {"success": True, "product_id": product_id}

    @staticmethod
    def update_inventory_by_id(product_id, change_amount):
        logger.info(f"Updating inventory for product_id={product_id}, change_amount={change_amount}")
        product = ProductDAO.get_product_by_id(product_id)
        if product is None:
            logger.warning(f"Product not found: product_id={product_id}")
            return {"success": False, "message": "Product does not exist."}
        new_inventory = product.inventory + change_amount
        if new_inventory < 0:
            logger.warning(f"Attempt to set negative inventory: product_id={product_id}, current_inventory={product.inventory}, attempted_change={change_amount}")
            return {"success": False, "message": "Inventory cannot be negative."}
        success = ProductDAO.update_inventory_by_id(product_id, new_inventory) > 0
        if success:
            logger.info(f"Inventory updated successfully for product_id={product_id}, new_inventory={new_inventory}")
        else:
            logger.error(f"Failed to update inventory for product_id={product_id}")
        return {"success": success, "message": "Inventory updated successfully." if success else "Failed to update inventory."}

    @staticmethod
    def update_price_by_id(product_id, new_price):
        logger.info(f"Updating price for product_id={product_id}, new_price={new_price}")
        product = ProductDAO.get_product_by_id(product_id)
        if product is None:
            logger.warning(f"Product not found: product_id={product_id}")
            return {"success": False, "message": "Product does not exist."}
        affected_line = ProductDAO.update_price_by_id(product_id, new_price) > 0
        if affected_line:
            logger.info(f"Price updated successfully for product_id={product_id}, new_price={new_price}")
        else:
            logger.error(f"Failed to update price for product_id={product_id}")
        return {"success": True, "message": f"Line affected by price change: {affected_line}"}

    @staticmethod
    def delete_product_by_id(product_id):
        logger.info(f"Attempting to delete product: product_id={product_id}")
        deleted_rows = ProductDAO.delete_product_by_id(product_id)
        if deleted_rows > 0:
            logger.info(f"Product deleted successfully: product_id={product_id}, rows_affected={deleted_rows}")
        else:
            logger.warning(f"Product deletion failed or no rows affected: product_id={product_id}")
        return {"success": True, "message": f"Deleted rows: {deleted_rows}"}
