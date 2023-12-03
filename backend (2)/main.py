from typing import List, Optional, Set
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import UserCreate, UserInDB, hash_password, User, Session, Participant
from jose import JWTError, jwt
from datetime import datetime, timedelta
import json
from auth import create_access_token, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import Depends
from passlib.context import CryptContext
from security import pwd_context


app = FastAPI()
# Utility function to load participants from the JSON file
def load_participants():
    try:
        with open("participants.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Return an empty list if the file does not exist

# Utility function to save participants to the JSON file
def save_participants(participants):
    with open("participants.json", "w") as file:
        json.dump(participants, file, indent=4)  # Indent for pretty printing

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Collaborative Jamming Scheduler API"}

# # Password hashing context
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT secret and algorithm
SECRET_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Function to read user data from the JSON file
def read_users_from_json():
    with open('users.json', 'r') as f:
        try:
            users = json.load(f)
        except FileNotFoundError:
            return {}  # Return an empty dict if the file doesn't exist
        except json.JSONDecodeError:
            return {}  # Return an empty dict if the file is empty or invalid
    return users

def save_users_db(users_db):
    with open('users.json', 'w') as file:
        json.dump(users_db, file, indent=4)

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(email: str, password: str):
    users_db = read_users_from_json()  # Load the user database
    user_dict = users_db.get(email)
    if not user_dict:
        return False
    user = UserInDB(**user_dict)
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/register/")
def register(user: UserCreate):
    users_db = read_users_from_json()  # Load the users database from JSON file
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user.password)
    users_db[user.email] = {"email": user.email, "hashed_password": hashed_password}
    save_users_db(users_db)  # Save the updated users database back to JSON file
    return {"email": user.email, "message": "Successfully registered."}

@app.post("/token/")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},  # Use dot notation here
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def get_user_from_json_db(email: str):
    users = read_users_from_json()
    user_dict = users.get(email)
    if user_dict:
        return UserInDB(**user_dict)
    return None

# Dependencies
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        user = get_user_from_json_db(email)
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception


@app.post("/protected-route/")
def protected_route(current_user: UserInDB = Depends(get_current_user)):
    # Now 'current_user' is the authenticated user
    # My protected logic goes here
    return {"message": "You are accessing a protected route", "user": current_user}

@app.get("/users/me/")
def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    return current_user

def get_next_session_id():
    sessions = load_sessions()
    if sessions:
        max_id = max(session['id'] for session in sessions)
    else:
        max_id = 0
    return max_id + 1

# Let's assume that `load_sessions` returns a list of sessions
def load_sessions():
    # Load the sessions from a JSON file and return them
    with open("sessions.json", "r") as file:
        sessions_data = json.load(file)
        # Convert any lists back to sets for the `participants` field
        for session in sessions_data:
            if 'participants' in session:
                session['participants'] = set(session['participants'])
        return sessions_data

def save_sessions(sessions):
    # Convert any sets to lists before serialization
    for session in sessions:
        if 'participants' in session:
            session['participants'] = list(session['participants'])
            
    with open("sessions.json", "w") as file:
        json.dump(sessions, file, indent=4)

@app.post("/sessions/")
async def create_session(session_details: Session, current_user: UserInDB = Depends(get_current_user)):
    sessions = load_sessions()

    # Creating a new session object
    new_session = Session(
        id=get_next_session_id(),  # Assuming this function generates a unique ID
        host_name=current_user.email,  # or another field from UserInDB, if appropriate
        # ...populate other fields from session_details...
        studio_name=session_details.studio_name,
        session_time=session_details.session_time,
        genre=session_details.genre,
        instruments=session_details.instruments,
        theme=session_details.theme,
        max_participants=session_details.max_participants,
        current_participants=session_details.current_participants,
        downpayment=session_details.downpayment,
        session_status=session_details.session_status,
        participants=session_details.participants
    )
    
    sessions.append(new_session.dict())
    save_sessions(sessions)
    return {"id": new_session.id}


@app.get("/sessions/", response_model=List[Session])
async def read_sessions():
    return load_sessions()

@app.get("/sessions/{session_id}", response_model=Session)
async def read_session(session_id: int):
    sessions = load_sessions()
    session = next((sess for sess in sessions if sess['id'] == session_id), None)
    if session is not None:
        return session
    raise HTTPException(status_code=404, detail="Session not found")

@app.put("/sessions/{session_id}")
async def update_session(session_id: int, updated_session: Session, current_user: UserInDB = Depends(get_current_user)):
    # Your logic to check if the current_user is authorized to update the session goes here

    sessions = load_sessions()
    session_index = next((index for (index, d) in enumerate(sessions) if d["id"] == session_id), None)

    if session_index is not None:
        updated_session_data = updated_session.dict(exclude_unset=True)
        for key, value in updated_session_data.items():
            sessions[session_index][key] = value
        save_sessions(sessions)
        return {"message": "Session updated successfully"}
    raise HTTPException(status_code=404, detail="Session not found")

@app.delete("/sessions/{session_id}")
async def delete_session(session_id: int, current_user: UserInDB = Depends(get_current_user)):
    # Your logic to check if the current_user is authorized to delete the session goes here

    sessions = load_sessions()
    session_index = next((index for (index, d) in enumerate(sessions) if d["id"] == session_id), None)

    if session_index is not None:
        sessions.pop(session_index)
        save_sessions(sessions)
        return {"message": "Session deleted successfully"}
    raise HTTPException(status_code=404, detail="Session not found")


# Read a single participant
@app.get("/participants/{participant_id}", response_model=Participant)
async def read_participant(participant_id: int):
    participants = load_participants()
    participant = next((part for part in participants if part['id'] == participant_id), None)
    if participant is not None:
        return participant
    raise HTTPException(status_code=404, detail="Participant not found")

# Write a single participant
@app.post("/participants/", response_model=Participant )
async def create_participant(participant: Participant = Depends(get_current_user)):
    participants = load_participants()
    participant.id = max([p["id"] for p in participants], default=0) + 1
    participants.append(participant.dict())
    save_participants(participants)
    return participant



# Update a participant
@app.put("/participants/{participant_id}")
async def update_participant(participant_id: int, updated_participant: Participant, current_user: UserInDB = Depends(get_current_user)):
    # Your logic to check if the current_user is authorized to update the participant goes here

    participants = load_participants()
    participant_index = next((index for (index, d) in enumerate(participants) if d["id"] == participant_id), None)

    if participant_index is not None:
        updated_participant_data = updated_participant.dict(exclude_unset=True)
        for key, value in updated_participant_data.items():
            participants[participant_index][key] = value
        save_participants(participants)
        return {"message": "Participant updated successfully"}
    raise HTTPException(status_code=404, detail="Participant not found")


@app.delete("/participants/{participant_id}")
async def delete_participant(participant_id: int, current_user: UserInDB = Depends(get_current_user)):
    # Your logic to check if the current_user is authorized to delete the participant goes here

    participants = load_participants()
    participant_index = next((index for (index, d) in enumerate(participants) if d["id"] == participant_id), None)

    if participant_index is None:
        raise HTTPException(status_code=404, detail="Participant not found")

    # Remove this participant from any sessions they're associated with
    sessions = load_sessions()
    for session in sessions:
        if participant_id in session.get('participants', []):
            session['participants'].remove(participant_id)
    save_sessions(sessions)

    # Now remove the participant
    participants.pop(participant_index)
    save_participants(participants)
    return {"message": "Participant deleted successfully"}




@app.put("/sessions/{session_id}/participants/{participant_id}")
async def add_participant_to_session(session_id: int, participant_id: int, current_user: UserInDB = Depends(get_current_user)):
    try:
        sessions = load_sessions()
        participants = load_participants()

        session = next((sess for sess in sessions if sess['id'] == session_id), None)
        participant = next((part for part in participants if part['id'] == participant_id), None)

        if session is None or participant is None:
            raise HTTPException(status_code=404, detail="Session or Participant not found")

        # Inside add_participant_to_session function
        if 'participants' not in session:
            session['participants'] = []
        if participant_id not in session['participants']:
            session['participants'].append(participant_id)


        if 'sessions' not in participant:
            participant['sessions'] = []
        if session_id not in participant['sessions']:
            participant['sessions'].append(session_id)

        save_sessions(sessions)
        save_participants(participants)
        return {"message": "Participant added to session successfully"}
    except Exception as e:
        # Log the full exception traceback for debugging
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="An internal server error occurred")

    except Exception as e:
        # Log unexpected exceptions for debugging
        print(f"Unexpected error: {e}")  # Consider using logging instead of print
        raise HTTPException(status_code=500, detail="An internal server error occurred")



@app.delete("/sessions/{session_id}/participants/{participant_id}")
async def remove_participant_from_session(session_id: int, participant_id: int, current_user: UserInDB = Depends(get_current_user)):
    sessions = load_sessions()
    participants = load_participants()

    session = next((sess for sess in sessions if sess['id'] == session_id), None)
    participant = next((part for part in participants if part['id'] == participant_id), None)

    if session is None or participant is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session or Participant not found")

    if participant_id not in session.get('participants', []):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Participant not associated with the session")

    # Remove the participant from the session
    session['participants'].remove(participant_id)
    participant['sessions'].remove(session_id)

    save_sessions(sessions)
    save_participants(participants)

    return {"message": "Participant removed from session successfully"}


# List all participants
@app.get("/participants/", response_model=List[Participant])
async def list_participants():
    participants = load_participants()
    return participants

@app.get("/participants/{participant_id}/sessions", response_model=List[Session])
async def read_participant_sessions(participant_id: int):
    try:
        sessions = load_sessions()
        participants = load_participants()

        participant = next((part for part in participants if part['id'] == participant_id), None)
        if participant is None:
            raise HTTPException(status_code=404, detail="Participant not found")

        participant_sessions = [sess for sess in sessions if participant_id in sess.get('participants', [])]
        return participant_sessions
    except HTTPException as he:  # This is to re-raise the 404 error without changing it to 500
        raise he
    except Exception as e:
        # Log the exception here
        raise HTTPException(status_code=500, detail="Failed to load participant sessions")








# # Password hashing context
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT secret and algorithm
# SECRET_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")




# # Function to read user data from the JSON file
# def read_users_from_json():
#     with open('users.json', 'r') as f:
#         try:
#             users = json.load(f)
#         except FileNotFoundError:
#             return {}  # Return an empty dict if the file doesn't exist
#         except json.JSONDecodeError:
#             return {}  # Return an empty dict if the file is empty or invalid
#     return users


# def save_users_db(users_db):
#     with open('users.json', 'w') as file:
#         json.dump(users_db, file, indent=4)

# # def verify_password(plain_password, hashed_password):
# #     return pwd_context.verify(plain_password, hashed_password)

# def authenticate_user(email: str, password: str):
#     users_db = read_users_from_json()  # Load the user database
#     user_dict = users_db.get(email)
#     if not user_dict:
#         return False
#     user = UserInDB(**user_dict)
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user

# def create_access_token(data: dict, expires_delta: timedelta = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# @app.post("/register/")
# def register(user: UserCreate):
#     users_db = read_users_from_json()  # Load the users database from JSON file
#     if user.email in users_db:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     hashed_password = hash_password(user.password)
#     users_db[user.email] = {"email": user.email, "hashed_password": hashed_password}
#     save_users_db(users_db)  # Save the updated users database back to JSON file
#     return {"email": user.email, "message": "Successfully registered."}

# @app.post("/token/")
# def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.email},  # Use dot notation here
#         expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}


# def get_user_from_json_db(email: str):
#     users = read_users_from_json()
#     user_dict = users.get(email)
#     if user_dict:
#         return UserInDB(**user_dict)
#     return None




# # Dependencies
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"}
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise credentials_exception
#         user = get_user_from_json_db(email)
#         if user is None:
#             raise credentials_exception
#         return user
#     except JWTError:
#         raise credentials_exception


# @app.post("/protected-route/")
# def protected_route(current_user: UserInDB = Depends(get_current_user)):
#     # Now 'current_user' is the authenticated user
#     # Your protected logic goes here
#     return {"message": "You are accessing a protected route", "user": current_user}

# @app.get("/users/me/")
# def read_users_me(current_user: UserInDB = Depends(get_current_user)):
#     # Convert UserInDB to User if necessary, or just return the current_user if UserInDB is suitable
#     return current_user