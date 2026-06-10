from fastapi import APIRouter, HTTPException, Depends
from schemas import Transaction, TransactionUpdate
from database import get_db
import mysql.connector
from routers.auth import get_current_user  # 1. Importa la dipendenza per l'autenticazione

router = APIRouter()

@router.post("/transactions")
def add_transaction(t: Transaction, db: mysql.connector.MySQLConnection = Depends(get_db), user_id: int = Depends(get_current_user)):
    cursor = db.cursor()
    # Aggiunto user_id nella query
    sql = "INSERT INTO transactions (user_id, date, description, amount, category_id, type) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (user_id, t.date, t.description, t.amount, t.category_id.value, t.type.value))
    db.commit()
    cursor.close()
    return {"status": "ok"}

@router.get("/transactions")
def get_transactions(db: mysql.connector.MySQLConnection = Depends(get_db), user_id: int = Depends(get_current_user)):
    cursor = db.cursor(dictionary=True)
    # Filtro per mostrare solo le transazioni dell'utente loggato
    cursor.execute("SELECT * FROM transactions WHERE user_id = %s", (user_id,))
    result = cursor.fetchall()
    cursor.close()
    return result

@router.put("/transactions/{transaction_id}")
def update_transaction(transaction_id: int, t: TransactionUpdate, db: mysql.connector.MySQLConnection = Depends(get_db), user_id: int = Depends(get_current_user)):
    cursor = db.cursor(dictionary=True)
    
    update_data = t.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided for update")

   
    if "tipo" in update_data:
        update_data["tipo"] = update_data["tipo"].value

    sql = "UPDATE transactions SET "
    fields = [f"{k} = %s" for k in update_data.keys()]
    sql += ", ".join(fields)
    sql += " WHERE id = %s AND user_id = %s"  
    
    values = list(update_data.values())
    values.append(transaction_id)
    values.append(user_id)
    
    cursor.execute(sql, tuple(values))
    db.commit()
    
    count = cursor.rowcount
    cursor.close()
    
    if count == 0:
        raise HTTPException(status_code=404, detail="Transaction not found or not owned by user")
    return {"status": "updated"}

@router.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int, db: mysql.connector.MySQLConnection = Depends(get_db), user_id: int = Depends(get_current_user)):
    cursor = db.cursor()
    # Elimina solo se appartiene all'utente loggato
    cursor.execute("DELETE FROM transactions WHERE id = %s AND user_id = %s", (transaction_id, user_id))
    db.commit()
    count = cursor.rowcount
    cursor.close()
    
    if count == 0:
        raise HTTPException(status_code=404, detail="Transaction not found or not owned by user")
    return {"status": "deleted"}

@router.get("/report")
@router.get("/transactions/summary")
def get_transactions_summary(db: mysql.connector.MySQLConnection = Depends(get_db), user_id: int = Depends(get_current_user)):
    cursor = db.cursor(dictionary=True)
    
    # Filtra i totali in base all'utente
    cursor.execute("SELECT category, SUM(amount) as total FROM transactions WHERE user_id = %s GROUP BY category", (user_id,))
    category_totals = cursor.fetchall()
    
    cursor.execute("SELECT SUM(amount) as total_sum FROM transactions WHERE user_id = %s", (user_id,))
    total_sum_result = cursor.fetchone()
    total_sum = float(total_sum_result['total_sum']) if total_sum_result and total_sum_result['total_sum'] is not None else 0.0
    
    summary_data = []
    if total_sum > 0:
        for item in category_totals:
            category = item['category']
            total = float(item['total']) 
            percentage = (total / total_sum) * 100
            summary_data.append({
                "category": category,
                "total": total,
                "percentage": f"{percentage:.2f}%" 
            })
    
    cursor.close()
    return summary_data