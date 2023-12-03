from pydantic import BaseModel, EmailStr
from typing import List, Optional, Set
from security import pwd_context


class Session(BaseModel):
    id: Optional[int] = None
    host_name: str
    studio_name: str
    session_time: str
    genre: str
    instruments: List[str]
    theme: Optional[str] = None
    max_participants: int
    current_participants: int
    downpayment: float
    session_status: str
    participants: Set[int] = set()  # Set of participant IDs in this session
    
class Participant(BaseModel):
    id: int
    name: str
    email: EmailStr
    instrument: str
    sessions: List[int] = []  # List of session IDs the participant is part of
    

class User(BaseModel):
    email: EmailStr
    hashed_password: str

    class Config:
        from_attributes = True

class UserInDB(User):
    hashed_password: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str

def hash_password(password: str):
    return pwd_context.hash(password)

