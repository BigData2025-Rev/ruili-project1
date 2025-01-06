import logging
from util.DatabaseConnection import DBConnector
from log.log import get_logger
from model.User import User
from model.Product import Product
from model.Order import Order
import mysql.connector

logger = get_logger(__name__)

class OrderDAO:
    """
    Table orders
    +------------+----------+------+-----+-------------------+-------------------+
    | Field      | Type     | Null | Key | Default           | Extra             |
    +------------+----------+------+-----+-------------------+-------------------+
    | id         | int      | NO   | PRI | NULL              | auto_increment    |
    | user_id    | int      | NO   | MUL | NULL              |                   |
    | product_id | int      | NO   | MUL | NULL              |                   |
    | quantity   | int      | NO   |     | NULL              |                   |
    | order_date | datetime | YES  |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
    +------------+----------+------+-----+-------------------+-------------------+

    reference integrity constraints:
    +----------------------+------------+-------------+-----------------------+------------------------+-------------+-------------+
    | CONSTRAINT_NAME      | TABLE_NAME | COLUMN_NAME | REFERENCED_TABLE_NAME | REFERENCED_COLUMN_NAME | DELETE_RULE | UPDATE_RULE |
    +----------------------+------------+-------------+-----------------------+------------------------+-------------+-------------+
    | fk_orders_user_id    | orders     | user_id     | users                 | id                     | CASCADE     | CASCADE     |
    | fk_orders_product_id | orders     | product_id  | products              | id                     | CASCADE     | CASCADE     |
    +----------------------+------------+-------------+-----------------------+------------------------+-------------+-------------+

    """
    @staticmethod
    def create_order(user_id, product_id, quantity):
        connection = None
        try:
            connection = DBConnector.get_connection()
            cursor = connection.cursor()

            query = """
                INSERT INTO orders (user_id, product_id, quantity)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (user_id, product_id, quantity))
            connection.commit()

            logger.info(f"Order created: user_id={user_id}, product_id={product_id}, quantity={quantity}.")
            return cursor.lastrowid

        except mysql.connector.Error as e:
            logger.warning(f"Failed to create order: {e}")
            return None

        finally:
            if connection and connection.is_connected():
                connection.close()

    @staticmethod
    def get_all_orders():
        connection = None
        try:
            connection = DBConnector.get_connection()
            cursor = connection.cursor(dictionary=True)

            query = "SELECT * FROM orders"
            cursor.execute(query)
            results = cursor.fetchall()
            return [Order.from_dict(row) for row in results]

        except mysql.connector.Error as e:
            logger.warning(f"Failed to get orders: {e}")
            return []

        finally:
            if connection and connection.is_connected():
                connection.close()

    @staticmethod
    def get_order_by_id(order_id):
        connection = None
        try:
            connection = DBConnector.get_connection()
            cursor = connection.cursor(dictionary=True)

            query = "SELECT * FROM orders WHERE id = %s"
            cursor.execute(query, (order_id,))
            result = cursor.fetchone()
            return Order.from_dict(result) if result else None

        except mysql.connector.Error as e:
            logger.warning(f"Failed to get order: {e}")
            return None

        finally:
            if connection and connection.is_connected():
                connection.close()

    @staticmethod
    def get_orders_by_user_id(user_id):
        connection = None
        try:
            connection = DBConnector.get_connection()
            cursor = connection.cursor(dictionary=True)

            query = "SELECT * FROM orders WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            results = cursor.fetchall()
            return [Order.from_dict(row) for row in results]

        except mysql.connector.Error as e:
            logger.warning(f"Failed to get orders for user_id={user_id}: {e}")
            return []

        finally:
            if connection and connection.is_connected():
                connection.close()

    @staticmethod
    def update_inventory_deposit_and_create_order(product_id, new_inventory, user_id, new_deposit, quantity):
        # in transaction, update both product inventory and user deposit, and create the order
        # in case database error happened during the process
        connection = None
        try:
            connection = DBConnector.get_connection()
            cursor = connection.cursor()
            connection.start_transaction()

            # update inventory
            inventory_query = "UPDATE products SET inventory = %s WHERE id = %s"
            cursor.execute(inventory_query, (new_inventory, product_id))

            # update user deposit
            deposit_query = "UPDATE users SET deposit = %s WHERE id = %s"
            cursor.execute(deposit_query, (new_deposit, user_id))

            # create order
            order_query = """
                INSERT INTO orders (user_id, product_id, quantity)
                VALUES (%s, %s, %s)
            """
            cursor.execute(order_query, (user_id, product_id, quantity))

            # commit
            connection.commit()
            logger.info(f"Order created: user_id={user_id}, product_id={product_id}, quantity={quantity}.")
            return cursor.lastrowid 

        except mysql.connector.Error as e:
            if connection:
                connection.rollback()  # here, exception happened, rollback
            logger.warning(f"Failed to process transaction: {e}")
            return None

        finally:
            if connection and connection.is_connected():
                connection.close()

    @staticmethod
    def delete_order_by_id(order_id):
        connection = None
        try:
            connection = DBConnector.get_connection()
            cursor = connection.cursor()

            query = "DELETE FROM orders WHERE id = %s"
            cursor.execute(query, (order_id,))
            connection.commit()

            logger.info(f"Order with ID {order_id} deleted successfully.")
            return cursor.rowcount

        except mysql.connector.Error as e:
            logger.warning(f"Failed to delete order: {e}")
            return 0

        finally:
            if connection and connection.is_connected():
                connection.close()
