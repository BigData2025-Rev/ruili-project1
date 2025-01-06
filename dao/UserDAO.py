import logging
from util.DatabaseConnection import DBConnector
from log.log import get_logger
from model.User import User
import mysql.connector

logger = get_logger(__name__)

class UserDAO:

    """
    Table users:
    +----------+----------------------+------+-----+---------+----------------+
    | Field    | Type                 | Null | Key | Default | Extra          |
    +----------+----------------------+------+-----+---------+----------------+
    | id       | int                  | NO   | PRI | NULL    | auto_increment |
    | username | varchar(255)         | NO   | UNI | NULL    |                |
    | password | varchar(255)         | NO   |     | NULL    |                |
    | role     | enum('user','admin') | NO   |     | NULL    |                |
    | deposit  | decimal(10,2)        | NO   |     | 0.00    |                |
    +----------+----------------------+------+-----+---------+----------------+
    """

    @staticmethod
    def get_all_users():
        """获取所有用户"""
        connection = None
        try:
            connection = DBConnector.get_connection()
            cursor = connection.cursor(dictionary=True)

            query = "SELECT * FROM users"
            cursor.execute(query)
            results = cursor.fetchall()
            logger.info(f"Returned all users.")
            return [User.from_dict(row) for row in results]

        except mysql.connector.Error as e:
            logger.warning(f"Database query failed: {e}")
            return []

        finally:
            if connection and connection.is_connected():
                connection.close()

    @staticmethod
    def get_user_by_username(username):
        connection = None
        try:
            connection = DBConnector.get_connection()
            cursor = connection.cursor(dictionary=True)

            query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()

            if result:
                user = User.from_dict(result)
                logger.info(f"Queried a user {user.username} and returned.")
                return user
            else:
                logger.info(f"Didn't find user with username : {username}")
                return None

        except mysql.connector.Error as e:
            logger.warning(f"Database query failed: {e} when querying {username}")
            return None

        finally:
            if connection and connection.is_connected():
                connection.close()

    @staticmethod
    def get_user_by_id(user_id):
        connection = None
        try:
            connection = DBConnector.get_connection()
            cursor = connection.cursor(dictionary=True)

            query = "SELECT * FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()

            if result:
                user = User.from_dict(result)
                logger.info(f"Queried a user with user id {user_id} and returned.")
                return user
            else:
                logger.info(f"Didn't find user with user id : {user_id}")
                return None

        except mysql.connector.Error as e:
            logger.warning(f"Database query failed: {e} when querying {user_id}")
            return None

        finally:
            if connection and connection.is_connected():
                connection.close()

    @staticmethod
    def update_user_deposit_by_id(user_id, new_deposit):
        connection = None
        try:
            connection = DBConnector.get_connection()
            cursor = connection.cursor()

            query = "UPDATE users SET deposit = %s WHERE id = %s" 
            cursor.execute(query, (new_deposit, user_id))
            connection.commit()

            logger.info(f"Updated deposit for user_id={user_id} to {new_deposit}.")
            return cursor.rowcount 

        except mysql.connector.Error as e:
            logger.warning(f"Failed to update deposit: {e} for user_id={user_id}.")
            return 0

        finally:
            if connection and connection.is_connected():
                connection.close()

    @staticmethod
    def create_user(username, password, role):
        connection = None
        try:
            # Get database connection
            connection = DBConnector.get_connection()
            cursor = connection.cursor()

            query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, password, role))
            connection.commit()

            logger.info(f"New user inserted into database: {username}, role={role}.")
            return cursor.lastrowid

        except mysql.connector.Error as e:
            logger.warning(f"Database insert failed: {e} when inserting {username}.")
            return None

        finally:
            if connection and connection.is_connected():
                connection.close()

    @staticmethod
    def update_username(user_id, new_username):
        connection = None
        try:
            connection = DBConnector.get_connection()
            cursor = connection.cursor()

            query = "UPDATE users SET username = %s WHERE id = %s"
            cursor.execute(query, (new_username, user_id))
            connection.commit()

            logger.info(f"Updated username for user_id={user_id} to {new_username}.")
            return cursor.rowcount 

        except mysql.connector.Error as e:
            logger.warning(f"Failed to update username: {e} for user_id={user_id}.")
            return 0

        finally:
            if connection and connection.is_connected():
                connection.close()

    @staticmethod
    def update_password(user_id, new_password):
        connection = None
        try:
            connection = DBConnector.get_connection()
            cursor = connection.cursor()

            query = "UPDATE users SET password = %s WHERE id = %s"
            cursor.execute(query, (new_password, user_id))
            connection.commit()

            logger.info(f"Updated password for user_id={user_id}.")
            return cursor.rowcount

        except mysql.connector.Error as e:
            logger.warning(f"Failed to update password: {e} for user_id={user_id}.")
            return 0

        finally:
            if connection and connection.is_connected():
                connection.close()

    @staticmethod
    def update_role_by_id(user_id, new_role):
        connection = None
        try:
            connection = DBConnector.get_connection()
            cursor = connection.cursor()

            query = "UPDATE users SET role = %s WHERE id = %s"
            cursor.execute(query, (new_role, user_id))
            connection.commit()

            logger.info(f"Updated role for user_id={user_id} to {new_role}.")
            return cursor.rowcount

        except mysql.connector.Error as e:
            logger.warning(f"Failed to update role: {e} for user_id={user_id}.")
            return 0

        finally:
            if connection and connection.is_connected():
                connection.close()

    @staticmethod
    def delete_user_by_id(user_id):
        connection = None
        try:
            connection = DBConnector.get_connection()
            cursor = connection.cursor()

            query = "DELETE FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            connection.commit()

            logger.info(f"Deleted user with user_id={user_id}.")
            return cursor.rowcount

        except mysql.connector.Error as e:
            logger.warning(f"Failed to delete user: {e} for user_id={user_id}.")
            return 0

        finally:
            if connection and connection.is_connected():
                connection.close()
    
    @staticmethod
    def delete_user_by_username(user_name):
        connection = None
        try:
            connection = DBConnector.get_connection()
            cursor = connection.cursor()

            query = "DELETE FROM users WHERE username = %s"
            cursor.execute(query, (user_name,))
            connection.commit()

            logger.info(f"Deleted user with user_name={user_name}.")
            return cursor.rowcount

        except mysql.connector.Error as e:
            logger.warning(f"Failed to delete user: {e} for user_name={user_name}.")
            return 0

        finally:
            if connection and connection.is_connected():
                connection.close()