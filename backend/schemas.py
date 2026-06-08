from typing import Optional

from pydantic import BaseModel
from datetime import date
from enum import Enum


# Definiamo le categorie permesse
class CategoriaEnum(str, Enum):
    CIBO = "Cibo"
    SVAGO = "Svago"
    CASA = "Casa"
    TRASPORTI = "Trasporti"
    ALTRO = "Altro"

class Transazione(BaseModel):
    data: date
    descrizione: str
    importo: float
    categoria: CategoriaEnum  

class TransazioneUpdate(BaseModel):
    data: Optional[date] = None
    descrizione: Optional[str] = None
    importo: Optional[float] = None
    categoria: Optional[CategoriaEnum] = None