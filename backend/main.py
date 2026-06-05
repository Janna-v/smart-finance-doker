from fastapi import FastAPI
import mysql.connector
import os
from pydantic import BaseModel

app = FastAPI()

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "db"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "root"),
        database=os.getenv("DB_NAME", "finanze_db") # Legge dal .env
    )

# Funzione per creare la tabella al primo avvio
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transazioni (
            id INT AUTO_INCREMENT PRIMARY KEY,
            descrizione VARCHAR(255),
            importo FLOAT,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    print("Tabella 'transazioni' verificata/creata con successo!")

# Eseguiamo l'inizializzazione all'avvio
init_db()

@app.get("/")
def read_root():
    return {"message": "Il backend è online e il DB è pronto!"}

@app.get("/transazioni")
def get_transazioni():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM transazioni")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# Definiamo come deve essere fatta una transazione
class Transazione(BaseModel):
    descrizione: str
    importo: float

@app.post("/transazioni")
def add_transazione(transazione: Transazione):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO transazioni (descrizione, importo) VALUES (%s, %s)"
    val = (transazione.descrizione, transazione.importo)
    cursor.execute(sql, val)
    conn.commit()
    cursor.close()
    conn.close()
    return {"status": "Transazione aggiunta con successo!"}