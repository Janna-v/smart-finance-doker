from fastapi import APIRouter, HTTPException, Depends, status
from database import get_db
import mysql.connector
from mysql.connector import Error
from schemas import UserCreate 
from passlib.context import CryptContext
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordRequestForm
import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

router = APIRouter()

# Carichiamo le variabili d'ambiente dal file .env
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = HTTPBearer()

@router.post("/register")
def register(user: UserCreate, db: mysql.connector.MySQLConnection = Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_password = pwd_context.hash(user.password[:72])

        sql = """
            INSERT INTO users (first_name, last_name, email, password_hash) 
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (user.first_name, user.last_name, user.email, hashed_password))
        db.commit()
    except Error as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        cursor.close()
    return {"status": "success", "message": "User registered successfully"}


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: mysql.connector.MySQLConnection = Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (form_data.username,))
    user = cursor.fetchone()

    if user is None:
        cursor.close()
        raise HTTPException(status_code=401, detail="Invalid credentials")
   
    if not pwd_context.verify(form_data.password, user['password_hash']):
        cursor.close()
        raise HTTPException(status_code=401, detail="Invalid credentials")

    cursor.close()
    
    payload = {
        "sub": str(user['id']), 
        "exp": datetime.utcnow() + timedelta(hours=8)
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    return {"access_token": token, "token_type": "bearer"}


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    token = credentials.credentials
    try:
        # Decodifichiamo il token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Estraiamo l'id utente
        user_id = payload.get("sub") 
        
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalido")
            
        return user_id
        
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalido o scaduto")