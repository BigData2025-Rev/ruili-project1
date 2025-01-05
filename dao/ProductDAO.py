import logging
from util.DatabaseConnection import DBConnector
from log.log import get_logger
from model.User import User
from model.Product import Product
from model.Order import Order
import mysql.connector

logger = get_logger(__name__)

class ProductDAO:
    
    """
    Table products
    +-------------+---------------+------+-----+-------------------+-----------------------------------------------+
    | Field       | Type          | Null | Key | Default           | Extra                                         |
    +-------------+---------------+------+-----+-------------------+-----------------------------------------------+
    | id          | int           | NO   | PRI | NULL              | auto_increment                                |
    | name        | varchar(255)  | NO   |     | NULL              |                                               |
    | description | text          | YES  |     | NULL              |                                               |
    | price       | decimal(10,2) | NO   |     | NULL              |                                               |
    | tags        | varchar(255)  | YES  |     | NULL              |                                               |
    | category    | varchar(255)  | YES  |     | NULL              |                                               |
    | inventory   | int           | NO   |     | NULL              |                                               |
    | created_at  | datetime      | YES  |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED                             |
    | updated_at  | datetime      | YES  |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED on update CURRENT_TIMESTAMP |
    +-------------+---------------+------+-----+-------------------+-----------------------------------------------+
    """
    
    @staticmethod
    def create_product(name, price, inventory, category=None, description=None):
        connection = None
        try:
            connection = DBConnector.get_connection()
            cursor = connection.cursor()

            query = """
                INSERT INTO products (name, price, inventory, category, description)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, price, inventory, category, description))
            connection.commit()

            logger.info(f"Product created: {name}, price={price}, inventory={inventory}.")
            return cursor.lastrowid

        except mysql.connector.Error as e:
            logger.warning(f"Failed to create product: {e}")
            return None

        finally:
            if connection and connection.is_connected():
                connection.close()

    @staticmethod
    def get_product_by_id(product_id):
        connection = None
        try:
            connection = DBConnector.get_connection()
            cursor = connection.cursor(dictionary=True)

            query = "SELECT * FROM products WHERE id = %s"
            cursor.execute(query, (product_id,))
            result = cursor.fetchone()
            return Product.from_dict(result) if result else None

        except mysql.connector.Error as e:
            logger.warning(f"Failed to get product: {e}")
            return None

        finally:
            if connection and connection.is_connected():
                connection.close()

    @staticmethod
    def get_product_by_name(product_name):
        connection = None
        try:
            connection = DBConnector.get_connection()
            cursor = connection.cursor(dictionary=True)

            query = "SELECT * FROM products WHERE name = %s"
            cursor.execute(query, (product_name,))
            result = cursor.fetchone()
            return Product.from_dict(result) if result else None

        except mysql.connector.Error as e:
            logger.warning(f"Failed to get product: {e}")
            return None

        finally:
            if connection and connection.is_connected():
                connection.close()

    @staticmethod
    def update_inventory_by_id(product_id, new_inventory):
        connection = None
        try:
            connection = DBConnector.get_connection()
            cursor = connection.cursor()

            query = "UPDATE products SET inventory = %s WHERE id = %s"
            cursor.execute(query, (new_inventory, product_id))
            connection.commit()

            logger.info(f"Updated inventory for product_id={product_id} to {new_inventory}.")
            return cursor.rowcount

        except mysql.connector.Error as e:
            logger.warning(f"Failed to update inventory: {e}")
            return 0

        finally:
            if connection and connection.is_connected():
                connection.close()

    @staticmethod
    def update_price_by_id(product_id, new_price):
        connection = None
        try:
            connection = DBConnector.get_connection()
            cursor = connection.cursor()

            query = "UPDATE products SET price = %s WHERE id = %s"
            cursor.execute(query, (new_price, product_id))
            connection.commit()

            logger.info(f"Updated price for product_id={product_id} to {new_price}.")
            return cursor.rowcount

        except mysql.connector.Error as e:
            logger.warning(f"Failed to update price: {e}")
            return 0

        finally:
            if connection and connection.is_connected():
                connection.close()

    @staticmethod
    def delete_product_by_id(product_id):
        connection = None
        try:
            connection = DBConnector.get_connection()
            cursor = connection.cursor()

            query = "DELETE FROM products WHERE id = %s"
            cursor.execute(query, (product_id,))
            connection.commit()

            logger.info(f"Deleted product with product_id={product_id}.")
            return cursor.rowcount

        except mysql.connector.Error as e:
            logger.warning(f"Failed to delete product: {e}")
            return 0

        finally:
            if connection and connection.is_connected():
                connection.close()