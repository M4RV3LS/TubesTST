from typing import Annotated, Optional
from fastapi import Depends, FastAPI, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import User, UserInDB, UserRegister  # Import models from models.py
from utilities import get_user, register_user  # Import utility functions
from typing import Annotated, Optional, Set
from fastapi import FastAPI
from sessions import router as sessions_router
from auth import get_current_active_user, fake_hash_password  # Import authentication utilities
from fastapi.middleware.cors import CORSMiddleware





app = FastAPI()

# CORS (Cross-Origin Resource Sharing) middleware untuk mengambil source cross origin darimana saja
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

#Routing Session
app.include_router(sessions_router, prefix="/sessions", tags=["sessions"])



@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)
    if not user or fake_hash_password(form_data.password) != user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

from fastapi import HTTPException

# @app.post("/register")
# async def register(username: str, password: str, email: Optional[str] = None, full_name: Optional[str] = None):
#     # Validate the input attributes before attempting to register the user
#     if not username or not username.strip():
#         raise HTTPException(status_code=400, detail="Username is required and cannot be blank.")
    
#     if not password or len(password) < 8:
#         raise HTTPException(status_code=400, detail="Password is required and must be at least 8 characters long.")
    
#     if email is not None and "@" not in email:
#         raise HTTPException(status_code=400, detail="Email must be a valid email address.")

#     # Proceed with user data creation and registration
#     user_data = UserInDB(
#         username=username,
#         hashed_password=fake_hash_password(password),
#         email=email,
#         full_name=full_name,
#         disabled=False
#     )

#     if register_user(username, user_data):
#         return {"message": "User registered successfully"}
#     else:
#         raise HTTPException(status_code=400, detail="Username already exists")



@app.post("/register")
async def register(user: UserRegister):  # Use the new model here
    # Now you can access the data as user.username, user.password, etc.
    if not user.username or not user.username.strip():
        raise HTTPException(status_code=400, detail="Username is required and cannot be blank.")
    
    if not user.password or len(user.password) < 8:
        raise HTTPException(status_code=400, detail="Password is required and must be at least 8 characters long.")
    
    if user.email and "@" not in user.email:
        raise HTTPException(status_code=400, detail="Email must be a valid email address.")

    # Proceed with user data creation and registration
    user_data = UserInDB(
        username=user.username,
        hashed_password=fake_hash_password(user.password),
        email=user.email,
        full_name=user.full_name,
        disabled=False
    )

    if register_user(user.username, user_data):
        return {"message": "User registered successfully"}
    else:
        raise HTTPException(status_code=400, detail="Username already exists")
