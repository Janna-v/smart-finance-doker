from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class ContactType(str, Enum):
    client = 'Client'
    supplier = 'Supplier'

class ContactCreate(BaseModel):
    name: str
    type: ContactType
    email: Optional[EmailStr] = None

class ContactResponse(BaseModel):
    id: int
    user_id: int
    name: str
    type: ContactType
    email: Optional[str] = None

    class Config:
        from_attributes = True