from backend.models import transazioni
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
# Importiamo il router dal pacchetto locale
# from routers.transazioni import router as transazioni_router
from routers.auth import router as auth_router
from database import get_db
from models.transazioni import init_db 
from routers import categories

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    db_gen = get_db()
    db = next(db_gen)  
    init_db(db)
    

app.include_router(transazioni.router)
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(categories.router)

@app.get("/")
def read_root():
    return {"message": "Il backend è online!"}