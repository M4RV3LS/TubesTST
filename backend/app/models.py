from pydantic import BaseModel, EmailStr
from typing import Optional, Set
from uuid import uuid4
import random


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

class Session(BaseModel):
    id: str
    host_name: str
    studio_name: str
    session_date: str
    session_time: str
    genre: Optional[str] = None
    theme: Optional[str] = None
    max_participants: int
    downpayment: int
    participants: list[str] = []
    total_fee : int

    @classmethod
    def create(cls, host_name: str, studio_name: str, session_date: str,  session_time: str, 
               genre: Optional[str], theme: Optional[str], max_participants: int, total_fee : int):
        return cls(
            id=str(uuid4()),
            host_name=host_name,
            studio_name=studio_name,
            session_date=session_date,
            session_time=session_time,
            genre=genre,
            theme=theme,
            max_participants=max_participants,
            downpayment=random.randint(50, 500),  # Random downpayment between 50 and 500
            participants=[],  # Initialize as an empty list
            total_fee = total_fee
        )
        
class CreateSessionModel(BaseModel):  # Define a model for the request body
    studio_name: str
    session_date: str
    session_time: str
    genre: Optional[str] = None
    theme: Optional[str] = None
    max_participants: int
    total_fee: int

#model for register User
class UserRegister(BaseModel):
    username: str
    password: str
    email: EmailStr = None
    full_name: Optional[str] = None
    

#model for post menu item
class Order_Item(BaseModel):
    order_id: int
    customer_id: int
    menu_id: int
    menu_quantity: int

    
    

