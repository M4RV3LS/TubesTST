from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import json
from typing import List, Optional, Set


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


# def load_sessions():
#     try:
#         with open('sessions.json', 'r') as file:
#             return json.load(file)
#     except json.JSONDecodeError as e:
#         # Log error details
#         print(f"JSONDecodeError: {e.msg}")
#         print(f"Error at line {e.lineno}, column {e.colno}")
        
#         # Read the problematic line
#         file.seek(0)
#         lines = file.readlines()
#         error_line = lines[e.lineno - 1]  # Adjust for zero-based index
#         print(f"Error line: {error_line}")

#         raise

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Collaborative Jamming Scheduler API"}

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
async def create_session(session: Session):
    sessions = load_sessions()
    session.id = get_next_session_id()
    sessions.append(session.dict())
    save_sessions(sessions)
    return {"id": session.id}

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
async def update_session(session_id: int, updated_session: Session):
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
async def delete_session(session_id: int):
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
@app.post("/participants/", response_model=Participant)
async def create_participant(participant: Participant):
    participants = load_participants()
    # Generate the next ID based on the maximum ID present in the system
    participant.id = max([p["id"] for p in participants], default=0) + 1
    participants.append(participant.dict())
    save_participants(participants)
    return participant


# Update a participant
@app.put("/participants/{participant_id}")
async def update_participant(participant_id: int, updated_participant: Participant):
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
async def delete_participant(participant_id: int):
    try:
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
    except HTTPException as http_exc:
        # Re-raise the HTTP exception to be handled by FastAPI
        raise http_exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")



@app.put("/sessions/{session_id}/participants/{participant_id}")
async def add_participant_to_session(session_id: int, participant_id: int):
    try:
        sessions = load_sessions()
        participants = load_participants()
        session = next((sess for sess in sessions if sess['id'] == session_id), None)
        participant = next((part for part in participants if part['id'] == participant_id), None)

        if session is None or participant is None:
            raise HTTPException(status_code=404, detail="Session or Participant not found")

        if 'participants' not in session:
            session['participants'] = set()
        session['participants'].add(participant_id)

        if 'sessions' not in participant:
            participant['sessions'] = []
        if session_id not in participant['sessions']:
            participant['sessions'].append(session_id)

        save_sessions(sessions)
        save_participants(participants)
        return {"message": "Participant added to session successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/sessions/{session_id}/participants/{participant_id}")
async def remove_participant_from_session(session_id: int, participant_id: int):
    try:
        sessions = load_sessions()
        participants = load_participants()
        session = next((sess for sess in sessions if sess['id'] == session_id), None)
        participant = next((part for part in participants if part['id'] == participant_id), None)

        if session and participant and participant_id in session.get('participants', []):
            session['participants'].remove(participant_id)
            participant['sessions'].remove(session_id)
            save_sessions(sessions)
            save_participants(participants)
            return {"message": "Participant removed from session successfully"}
        else:
            raise HTTPException(status_code=404, detail="Session or Participant not found or not associated")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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

