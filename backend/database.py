import os
import mysql.connector
from mysql.connector import Error

def get_db():
    connection = mysql.connector.connect(
        host="mysql_db",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=3306
    )
    try:
        yield connection
    finally:
        connection.close()