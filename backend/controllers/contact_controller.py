import mysql.connector
from models.contact_model import ContactCreate, ContactType

def create_contact_in_db(db: mysql.connector.MySQLConnection, user_id: int, contact: ContactCreate):
    cursor = db.cursor()
    try:
        sql = """
        INSERT INTO contacts (user_id, name, type, email) 
        VALUES (%s, %s, %s, %s)
        """
        
        # Estrazione sicura dei dati gestendo sia Pydantic object che dict
        is_dict = isinstance(contact, dict)
        name = contact.get("name") if is_dict else contact.name
        email = contact.get("email") if is_dict else contact.email
        raw_type = contact.get("type") if is_dict else contact.type
        type_val = getattr(raw_type, 'value', raw_type)
        actual_user_id = user_id.get("id") if isinstance(user_id, dict) else user_id

        cursor.execute(sql, (actual_user_id, name, type_val, email))
        db.commit()
        
        new_id = cursor.lastrowid
        return {
            "id": new_id,
            "user_id": user_id,
            "name": name,
            "type": type_val,
            "email": email
        }
    finally:
        cursor.close()

def get_contacts_by_user(db: mysql.connector.MySQLConnection, user_id: int):
    cursor = db.cursor(dictionary=True)
    try:
        sql = "SELECT id, user_id, name, type, email FROM contacts WHERE user_id = %s"
        cursor.execute(sql, (user_id,))
        return cursor.fetchall()
    finally:
        cursor.close()

def update_contact_in_db(db: mysql.connector.MySQLConnection, user_id: int, contact_id: int, contact: ContactCreate):
    cursor = db.cursor()
    try:
        sql = """
        UPDATE contacts 
        SET name = %s, type = %s, email = %s 
        WHERE id = %s AND user_id = %s
        """
        
        # Estrazione sicura dei dati gestendo sia Pydantic object che dict
        is_dict = isinstance(contact, dict)
        name = contact.get("name") if is_dict else contact.name
        email = contact.get("email") if is_dict else contact.email
        raw_type = contact.get("type") if is_dict else contact.type
        type_val = getattr(raw_type, 'value', raw_type)
        actual_user_id = user_id.get("id") if isinstance(user_id, dict) else user_id

        cursor.execute(sql, (name, type_val, email, contact_id, actual_user_id))
        db.commit()
        
        return cursor.rowcount > 0 # Restituisce True se la modifica è avvenuta con successo
    finally:
        cursor.close()

def delete_contact_from_db(db: mysql.connector.MySQLConnection, user_id: int, contact_id: int):
    cursor = db.cursor()
    try:
        sql = "DELETE FROM contacts WHERE id = %s AND user_id = %s"
        cursor.execute(sql, (contact_id, user_id))
        db.commit()
        
        return cursor.rowcount > 0 # Restituisce True se l'eliminazione è avvenuta con successo
    finally:
        cursor.close()