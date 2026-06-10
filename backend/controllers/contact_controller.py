import mysql.connector
from models.contact_model import ContactCreate, ContactType

def _extract_id(user_obj):
    """Estrae l'ID numerico da un int, stringa, dict o oggetto Pydantic."""
    if isinstance(user_obj, (int, str)):
        return user_obj
    if isinstance(user_obj, dict):
        # Cerca 'id', poi 'sub' (usato nei token JWT), poi 'user_id'
        return user_obj.get("id") or user_obj.get("sub") or user_obj.get("user_id")
    # Prova a leggere l'attributo se è un oggetto (es. Pydantic model)
    return getattr(user_obj, "id", getattr(user_obj, "sub", user_obj))

def _extract_val(obj):
    """Estrae il valore scalare da Enumi, dict o stringhe."""
    if isinstance(obj, (int, str)) or obj is None:
        return obj
    if isinstance(obj, dict):
        return obj.get("value") or obj.get("id") or str(obj)
    # Gestisce Enum (.value) o restituisce l'oggetto stesso
    return getattr(obj, "value", obj)

def create_contact_in_db(db: mysql.connector.MySQLConnection, user_id: int, contact: ContactCreate):
    cursor = db.cursor()
    try:
        sql = """
        INSERT INTO contacts (user_id, name, type, email) 
        VALUES (%s, %s, %s, %s)
        """
        
        is_dict_contact = isinstance(contact, dict)
        name = contact.get("name") if is_dict_contact else contact.name
        email = contact.get("email") if is_dict_contact else contact.email
        raw_type = contact.get("type") if is_dict_contact else contact.type
        
        type_val = _extract_val(raw_type)
        actual_user_id = _extract_id(user_id)

        cursor.execute(sql, (actual_user_id, name, type_val, email))
        db.commit()
        
        new_id = cursor.lastrowid
        return {
            "id": new_id,
            "user_id": actual_user_id,
            "name": name,
            "type": type_val,
            "email": email
        }
    finally:
        cursor.close()

def get_contacts_by_user(db: mysql.connector.MySQLConnection, user_id: int):
    cursor = db.cursor(dictionary=True)
    actual_user_id = _extract_id(user_id)
    try:
        sql = "SELECT id, user_id, name, type, email FROM contacts WHERE user_id = %s"
        cursor.execute(sql, (actual_user_id,))
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
        
        is_dict_contact = isinstance(contact, dict)
        name = contact.get("name") if is_dict_contact else contact.name
        email = contact.get("email") if is_dict_contact else contact.email
        raw_type = contact.get("type") if is_dict_contact else contact.type
        
        type_val = _extract_val(raw_type)
        actual_user_id = _extract_id(user_id)

        cursor.execute(sql, (name, type_val, email, contact_id, actual_user_id))
        db.commit()
        
        return cursor.rowcount > 0 # Restituisce True se la modifica è avvenuta con successo
    finally:
        cursor.close()

def delete_contact_from_db(db: mysql.connector.MySQLConnection, user_id: int, contact_id: int):
    cursor = db.cursor()
    actual_user_id = _extract_id(user_id)
    try:
        sql = "DELETE FROM contacts WHERE id = %s AND user_id = %s"
        cursor.execute(sql, (contact_id, actual_user_id))
        db.commit()
        
        return cursor.rowcount > 0 # Restituisce True se l'eliminazione è avvenuta con successo
    finally:
        cursor.close()