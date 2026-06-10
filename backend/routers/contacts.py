from fastapi import APIRouter, Depends, HTTPException, status
import mysql.connector
from typing import List
from database import get_db
from routers.auth import get_current_user
from models.contact_model import ContactCreate, ContactResponse

from controllers.contact_controller import (
    create_contact_in_db, 
    get_contacts_by_user, 
    update_contact_in_db, 
    delete_contact_from_db
)

router = APIRouter(prefix="/contacts", tags=["Contacts"])

@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def create_contact(
    contact: ContactCreate,
    db: mysql.connector.MySQLConnection = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return create_contact_in_db(db, user_id, contact)

@router.get("/", response_model=List[ContactResponse])
def get_contacts(
    db: mysql.connector.MySQLConnection = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return get_contacts_by_user(db, user_id)


@router.put("/{contact_id}")
def update_contact(
    contact_id: int,
    contact: ContactCreate,
    db: mysql.connector.MySQLConnection = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    success = update_contact_in_db(db, user_id, contact_id, contact)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contatto non trovato o non posseduto dall'utente")
    return {"status": "success", "message": "Contatto aggiornato con successo"}

@router.delete("/{contact_id}")
def delete_contact(
    contact_id: int,
    db: mysql.connector.MySQLConnection = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    success = delete_contact_from_db(db, user_id, contact_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contatto non trovato o non posseduto dall'utente")
    return {"status": "success", "message": "Contatto eliminato con successo"}    