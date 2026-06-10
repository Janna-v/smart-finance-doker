from fastapi import APIRouter, HTTPException, Depends
from database import get_db
import mysql.connector
from schemas import CategoryCreate, CategoryUpdate
from routers.auth import get_current_user
from pydantic import BaseModel

router = APIRouter()

@router.post("/categories")
def add_category(category: CategoryCreate, db: mysql.connector.MySQLConnection = Depends(get_db), user_id: int = Depends(get_current_user)):
    cursor = db.cursor()
    try:
        sql = "INSERT INTO categories (user_id, name, type) VALUES (%s, %s, %s)"
        cursor.execute(sql, (user_id, category.name, category.type))
        db.commit()
    except mysql.connector.Error as e:
        raise HTTPException(status_code=400, detail=f"Errore durante l'inserimento della categoria: {e}")
    finally:
        cursor.close()
    
    return {"status": "success", "message": "Categoria creata con successo"}


@router.get("/categories")
def get_categories(db: mysql.connector.MySQLConnection = Depends(get_db), user_id: int = Depends(get_current_user)):
    cursor = db.cursor(dictionary=True)
    # Seleziona solo le categorie che appartengono all'utente loggato
    cursor.execute("SELECT id, name, type FROM categories WHERE user_id = %s", (user_id,))
    result = cursor.fetchall()
    cursor.close()
    
    return result


@router.put("/categories/{category_id}")
def update_category(category_id: int, c: CategoryUpdate, db: mysql.connector.MySQLConnection = Depends(get_db), user_id: int = Depends(get_current_user)):
    cursor = db.cursor()
    try:
        # Aggiorna solo se la categoria appartiene all'utente loggato
        sql = "UPDATE categories SET name = %s WHERE id = %s AND user_id = %s"
        cursor.execute(sql, (c.name, category_id, user_id))
        db.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Categoria non trovata o non posseduta dall'utente")
            
    except mysql.connector.Error as e:
        raise HTTPException(status_code=400, detail="Errore durante l'aggiornamento o nome già esistente.")
    finally:
        cursor.close()
        
    return {"status": "success", "message": "Categoria aggiornata con successo"}

@router.delete("/categories/{category_id}")
def delete_category(category_id: int, db: mysql.connector.MySQLConnection = Depends(get_db), user_id: int = Depends(get_current_user)):
    cursor = db.cursor()
    
    sql = "DELETE FROM categories WHERE id = %s AND user_id = %s"
    cursor.execute(sql, (category_id, user_id))
    db.commit()
    
    count = cursor.rowcount
    cursor.close()
    
    if count == 0:
        raise HTTPException(status_code=404, detail="Categoria non trovata o non posseduta dall'utente")
        
    return {"status": "success", "message": "Categoria eliminata con successo"}