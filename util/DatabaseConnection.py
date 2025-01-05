import os
import json
import mysql.connector

def load_db_config(file_path):
    # Get the directory of the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the absolute path to the JSON file
    absolute_path = os.path.join(base_dir, file_path)
    with open(absolute_path, 'r') as file:
        return json.load(file)

db_config = load_db_config('../config/db_connection.json')

try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    print("Database connection succeeded.")

    cursor.execute("show tables;")
    for table in cursor.fetchall():
        print(table)

except mysql.connector.Error as err:
    print(f"Database connection failed: {err}")

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()


