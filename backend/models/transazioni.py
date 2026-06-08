# models/transazioni.py
import mysql.connector

def init_db(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transazioni (
            id INT AUTO_INCREMENT PRIMARY KEY,
            data DATE NOT NULL,
            descrizione VARCHAR(255) NOT NULL,
            importo FLOAT NOT NULL,
            categoria VARCHAR(100),
            tipo VARCHAR(20) DEFAULT 'Uscita'
        )
    """)
    conn.commit()