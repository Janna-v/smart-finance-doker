from pydantic import BaseModel
from datetime import date

class Transazione(BaseModel):
    data: date
    descrizione: str
    importo: float
    categoria: str