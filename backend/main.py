from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
# Importiamo il router dal pacchetto locale
from routers.transazioni import router as transazioni_router
from database import get_db
from models.transazioni import init_db 

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
    

app.include_router(transazioni_router)

@app.get("/")
def read_root():
    return {"message": "Il backend è online!"}