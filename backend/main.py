from fastapi import FastAPI
import mysql.connector
import os
from pydantic import BaseModel
from schemas import Transazione

app = FastAPI()

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=os.getenv("DB_PORT")
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
    # Usiamo i 4 campi definiti nel tuo file schemas.py
    sql = "INSERT INTO transazioni (data, descrizione, importo, categoria) VALUES (%s, %s, %s, %s)"
    val = (transazione.data, transazione.descrizione, transazione.importo, transazione.categoria)
    cursor.execute(sql, val)
    conn.commit()
    cursor.close()
    conn.close()
    return {"status": "Transazione aggiunta con successo!"}

# ... (tutto il tuo codice precedente) ...

# AGGIUNGI QUESTO ALLA FINE DEL FILE
if __name__ == "__main__":
    import uvicorn
    # 'main:app' significa: cerca l'oggetto 'app' dentro il file 'main.py'
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


@app.post("/transazioni/")
def crea_transazione(t: Transazione):
    # Qui dentro scriveremo la logica per salvare nel database
    # Per ora, facciamo solo una prova:
    return {"messaggio": "Ho ricevuto la transazione!", "dati": t}