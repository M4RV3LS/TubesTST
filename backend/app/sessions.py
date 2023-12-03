from fastapi import APIRouter, HTTPException, Depends, Body
from models import User, Session
from utilities import get_sessions_db, write_sessions_db
from auth import get_current_active_user
from typing import Optional, Set


router = APIRouter()

#Membuat sebuah music jamming session
@router.post("/", response_model=Session)
async def create_session(
    studio_name: str,
    session_time: str,
    genre: Optional[str] = None,
    theme: Optional[str] = None,
    max_participants: int = Body(...),  # Removed gt=0 to accept user input
    current_user: User = Depends(get_current_active_user)
):
    # Assume Session.create is a method that initializes a Session instance
    new_session = Session.create(
        host_name=current_user.username,
        studio_name=studio_name,
        session_time=session_time,
        genre=genre,
        theme=theme,
        max_participants=max_participants
    )
    sessions = get_sessions_db()
    sessions.append(new_session.dict())
    write_sessions_db(sessions)
    return new_session

#mendapatkan data sebuah music jamming session berdasarkan id session nya
@router.get("/{session_id}")
async def get_session_by_id(session_id: str, current_user: User = Depends(get_current_active_user)):
    sessions = get_sessions_db()
    session = next((s for s in sessions if s["id"] == session_id), None)
    if session:
        return session
    raise HTTPException(status_code=404, detail="Session not found")

#mendapatkan music jamming session berdasarkan inputan nama
@router.get("/user/{username}")
async def get_sessions_by_username(username: str, current_user: User = Depends(get_current_active_user)):
    sessions = get_sessions_db()
    user_sessions = [s for s in sessions if s["host_name"] == username]
    return user_sessions

#Mendapatkan semua music jamming session
@router.get("/")
async def get_all_sessions(current_user: User = Depends(get_current_active_user)):
    return get_sessions_db()

#mendelete music jamming sessions 
@router.delete("/{session_id}")
async def delete_session(session_id: str, current_user: User = Depends(get_current_active_user)):
    sessions = get_sessions_db()
    session_index = next((i for i, s in enumerate(sessions) if s["id"] == session_id), None)
    
    if session_index is None:
        raise HTTPException(status_code=404, detail="Session not found")

    # Only allow deletion if the current user is the host of the session
    if sessions[session_index]["host_name"] != current_user.username:
        raise HTTPException(status_code=403, detail="Not authorized to delete this session")

    del sessions[session_index]
    write_sessions_db(sessions)
    return {"message": "Session deleted successfully"}

#menaruh user kedalam list of participant di suatu sesi , intinya kaya "join music jamming sessions" feature
@router.put("/{session_id}/participants")
async def add_participant_to_session(session_id: str, current_user: User = Depends(get_current_active_user)):
    sessions = get_sessions_db()
    session = next((s for s in sessions if s["id"] == session_id), None)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session["host_name"] == current_user.username:
        raise HTTPException(status_code=400, detail="Host cannot join as a participant")

    if current_user.username in session.get("participants", []):
        raise HTTPException(status_code=400, detail="User already a participant")

    session["participants"].append(current_user.username)
    write_sessions_db(sessions)
    return {"message": "Participant added successfully"}