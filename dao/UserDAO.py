import logging
from util.DatabaseConnection import DBConnector

class UserDAO:
    @staticmethod
    def get_user_by_username(username):
        connection = None
        try:
            # get database connection
            connection = DBConnector.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            return result

        except Exception as e:
            print(f"Database query failed: {e}")
            print(f"When trying to query the username: {username}")
            return None

        finally:
            if connection:
                connection.close()  # ensure to claose the connection