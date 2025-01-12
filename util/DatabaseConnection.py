import os
import json
import mysql.connector
from mysql.connector import pooling
from log.log import get_logger

logger = get_logger(__name__)

class DBConnector:
    _pool = None
    _config_filepath = "../config/db_connection.json"

    @staticmethod
    def load_db_config(file_path):
        # Get the connection host, username, and password from the file
        # added tey except to handle exception and add loggers
        logger.info("Attempting to load database configuration from file: %s", file_path)
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            absolute_path = os.path.join(base_dir, file_path)
            with open(absolute_path, 'r') as file:
                config = json.load(file)
                logger.info("Database configuration successfully loaded.")
                return config
        except FileNotFoundError as e:
            logger.error("Database configuration file not found: %s", e)
            raise
        except json.JSONDecodeError as e:
            logger.error("Error decoding JSON from database configuration file: %s", e)
            raise
        except Exception as e:
            logger.error("Unexpected error while loading database configuration: %s", e)
            raise

    @classmethod
    def initialize_pool(cls):
        # Initialize the connection pool only once
        # I can take connection from pools instead of create new connectio nevery time or just play with one connection
        # this brings higher performance
        if cls._pool is not None:
            logger.info("Connection pool is already initialized.")
            return
        
        logger.info("Initializing connection pool.")
        try:
            db_config = cls.load_db_config(cls._config_filepath)
            cls._pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **db_config)
            logger.info("Connection pool initialized successfully with pool name: %s", cls._pool.pool_name)
        except Exception as e:
            logger.error("Failed to initialize connection pool: %s", e)
            raise

    @staticmethod
    def get_connection():
        # Ensure the pool is initialized
        if DBConnector._pool is None:
            logger.warning("Connection pool is not initialized. Initializing now.")
            try:
                DBConnector.initialize_pool()
            except Exception as e:
                logger.error("Failed to initialize connection pool during get_connection: %s", e)
                raise

        try:
            connection = DBConnector._pool.get_connection()
            logger.info("Successfully obtained a connection from the pool.")
            return connection
        except Exception as e:
            logger.error("Failed to obtain a connection from the pool: %s", e)
            raise
