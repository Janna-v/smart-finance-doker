from datetime import date
from typing import Optional
from enum import Enum
from pydantic import BaseModel, EmailStr

class Category(str, Enum):
    food = "Food"
    leisure = "Leisure"
    home = "Home"

class TransactionType(str, Enum):
    expense = "Expense"
    income = "Income"

class TransactionBase(BaseModel):
    date: date
    description: str
    amount: float
    category: Category
    type: TransactionType

class Transaction(TransactionBase):
    id: Optional[int] = None

    class Config:
        from_attributes = True

class TransactionUpdate(BaseModel):
    date: Optional[date] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    category: Optional[Category] = None
    type: Optional[TransactionType] = None

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str