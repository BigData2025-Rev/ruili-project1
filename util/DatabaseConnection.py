import os
import json
import mysql.connector
from mysql.connector import pooling

class DBConnector:
    _pool = None
    _config_filepath = "../config/db_connection.json"

    @staticmethod
    def load_db_config(file_path):
        # Get the connection host, username, and password from the file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        absolute_path = os.path.join(base_dir, file_path)
        with open(absolute_path, 'r') as file:
            return json.load(file)

    @classmethod
    def initialize_pool(cls):
        # Initialize the connection pool only once
        db_config = cls.load_db_config(cls._config_filepath)
        cls._pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **db_config)

    @staticmethod
    def get_connection():
        # Ensure the pool is initialized
        if DBConnector._pool is None:
            DBConnector.initialize_pool()
        return DBConnector._pool.get_connection()
