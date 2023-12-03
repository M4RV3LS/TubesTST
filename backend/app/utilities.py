import json
from typing import Optional
from models import UserInDB  # Importing models from models.py


def get_user_db() -> dict:
    with open('db/users.json', 'r') as file:
        return json.load(file)

def write_user_db(db: dict) -> None:
    try:
        with open('db/users.json', 'w') as file:
            json.dump(db, file, indent=4)
    except Exception as e:
        print(f"An error occurred while writing to the users.json file: {e}")
        # Depending on your setup, you might want to raise the exception or handle it differently


def get_user(username: str) -> Optional[UserInDB]:
    db = get_user_db()
    user_data = db.get(username)
    if user_data:
        return UserInDB(**user_data)
    return None



def register_user(username: str, user_data: UserInDB) -> bool:
    db = get_user_db()
    if username in db:
        return False  # User already exists
    db[username] = user_data.dict()
    write_user_db(db)
    return True



def get_sessions_db() -> list:
    try:
        with open('db/sessions.json', 'r') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"JSON decode error in sessions.json: {e}")
        return []  # Return an empty list if there's a decode error
    except FileNotFoundError:
        print("sessions.json not found, creating a new one")
        write_sessions_db([])  # Create a new file with an empty list
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise


def write_sessions_db(sessions: list) -> None:
    # Convert sets to lists before writing JSON
    for session in sessions:
        if isinstance(session.get('participants', None), set):
            session['participants'] = list(session['participants'])
    try:
        with open('db/sessions.json', 'w') as file:
            json.dump(sessions, file, indent=4)
    except Exception as e:
        print(f"An error occurred while writing to the sessions.json file: {e}")
        raise

