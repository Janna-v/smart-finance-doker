from fastapi import APIRouter, HTTPException, Depends
from schemas import Transazione, TransazioneUpdate
from database import get_db
import mysql.connector

router = APIRouter()

@router.post("/transazioni")
def add_transazione(t: Transazione, db: mysql.connector.MySQLConnection = Depends(get_db)):
    cursor = db.cursor()
    sql = "INSERT INTO transazioni (data, descrizione, importo, categoria, tipo) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (t.data, t.descrizione, t.importo, t.categoria.value, t.tipo.value))
    db.commit()
    cursor.close()
    return {"status": "ok"}

@router.get("/transazioni")
def get_transazioni(db: mysql.connector.MySQLConnection = Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM transazioni")
    result = cursor.fetchall()
    cursor.close()
    return result

@router.put("/transazioni/{id_transazione}")
def update_transazione(id_transazione: int, t: TransazioneUpdate, db: mysql.connector.MySQLConnection = Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    
   
    update_data = t.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Nessun dato fornito per l'aggiornamento")

    
    if "categoria" in update_data:
        update_data["categoria"] = update_data["categoria"].value
    if "tipo" in update_data:
        update_data["tipo"] = update_data["tipo"].value

    sql = "UPDATE transazioni SET "
    fields = [f"{k} = %s" for k in update_data.keys()]
    sql += ", ".join(fields)
    sql += " WHERE id = %s"
    
    values = list(update_data.values())
    values.append(id_transazione)
    
    cursor.execute(sql, tuple(values))
    db.commit()
    
    count = cursor.rowcount
    cursor.close()
    
    if count == 0:
        raise HTTPException(status_code=404, detail="Transazione non trovata")
    return {"status": "updated"}

@router.delete("/transazioni/{id_transazione}")
def delete_transazione(id_transazione: int, db: mysql.connector.MySQLConnection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM transazioni WHERE id = %s", (id_transazione,))
    db.commit()
    cursor.close()
    return {"status": "deleted"}

@router.get("/report")
@router.get("/transazioni/summary")
def get_transazioni_summary(db: mysql.connector.MySQLConnection = Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    
   
    cursor.execute("SELECT categoria, SUM(importo) as totale FROM transazioni GROUP BY categoria")
    category_totals = cursor.fetchall()
    
    
    cursor.execute("SELECT SUM(importo) as total_sum FROM transazioni")
    total_sum_result = cursor.fetchone()
    total_sum = float(total_sum_result['total_sum']) if total_sum_result and total_sum_result['total_sum'] is not None else 0.0
    
    summary_data = []
    if total_sum > 0:
        for item in category_totals:
            categoria = item['categoria']
            totale = float(item['totale']) 
            percentuale = (totale / total_sum) * 100
            summary_data.append({
                "categoria": categoria,
                "totale": totale,
                "percentuale": f"{percentuale:.2f}%" 
            })
    
    cursor.close()
    return summary_data