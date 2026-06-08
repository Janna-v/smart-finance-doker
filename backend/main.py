from fastapi import FastAPI
import mysql.connector
import os
from typing import Optional
from pydantic import BaseModel
from schemas import Transazione, TransazioneUpdate, CategoriaEnum

app = FastAPI()

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=os.getenv("DB_PORT")
    )

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    # ATTENZIONE: La tabella deve avere anche 'categoria' per corrispondere allo schema!
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transazioni (
            id INT AUTO_INCREMENT PRIMARY KEY,
            data DATE,
            descrizione VARCHAR(255),
            importo FLOAT,
            categoria VARCHAR(100)
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

init_db()

@app.get("/")
def read_root():
    return {"message": "Il backend è online!"}

@app.post("/transazioni")
def add_transazione(t: Transazione):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # .strip() toglie gli spazi, .capitalize() rende la prima lettera maiuscola
    categoria_pulita = t.categoria.strip().capitalize() 
    
    sql = "INSERT INTO transazioni (data, descrizione, importo, categoria) VALUES (%s, %s, %s, %s)"
    val = (t.data, t.descrizione, t.importo, categoria_pulita)
    
    cursor.execute(sql, val)
    conn.commit()
    cursor.close()
    conn.close()
    return {"status": "Aggiunto con categoria: " + categoria_pulita}

@app.get("/transazioni")
def get_transazioni():
    conn = get_db_connection()
    # Usiamo 'dictionary=True' per avere i risultati come un dizionario leggibile
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM transazioni")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

@app.delete("/transazioni/{id_transazione}")
def delete_transazione(id_transazione: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Debug: stampiamo cosa stiamo cercando di cancellare
    print(f"Tentativo di cancellazione ID: {id_transazione}")
    
    sql = "DELETE FROM transazioni WHERE id = %s"
    cursor.execute(sql, (id_transazione,))
    conn.commit()
    
    if cursor.rowcount == 0:
        msg = {"error": f"Transazione con ID {id_transazione} non trovata!"}
    else:
        msg = {"status": f"Transazione {id_transazione} eliminata con successo!"}
        
    cursor.close()
    conn.close()
    return msg


@app.patch("/transazioni/{id_transazione}")
def patch_transazione(id_transazione: int, t: TransazioneUpdate):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # 1. Recupero record esistente
        cursor.execute("SELECT * FROM transazioni WHERE id = %s", (id_transazione,))
        record = cursor.fetchone()
        
        if not record:
            return {"error": "Non trovato"}

        # 2. Log dei dati in arrivo
        print(f"DEBUG: Dati ricevuti: {t.dict()}")

        # 3. Aggiornamento forzato
        data = t.data if (t.data and t.data != "string") else record['data']
        descrizione = t.descrizione if (t.descrizione and t.descrizione != "string") else record['descrizione']
        importo = t.importo if (t.importo is not None) else record['importo']
        categoria = t.categoria if (t.categoria and t.categoria != "string") else record['categoria']

        sql = "UPDATE transazioni SET data=%s, descrizione=%s, importo=%s, categoria=%s WHERE id=%s"
        cursor.execute(sql, (data, descrizione, importo, categoria, id_transazione))
        conn.commit()
        
        return {"status": "Aggiornato!"}
    
    except Exception as e:
        print(f"DEBUG CRITICO: {e}")
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()


@app.get("/report")
def get_report():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Query: raggruppa per categoria e somma gli importi
    sql = """
        SELECT categoria, SUM(importo) as totale 
        FROM transazioni 
        GROUP BY categoria
    """
    cursor.execute(sql)
    report = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return report