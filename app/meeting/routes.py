from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from db.database import get_db
from models.meeting_models import Meeting, Participant, Message, MeetingLog
from models.usermodels import User
from schemas.meeting_schemas import CreateMeetingRequest, JoinMeetingRequest, SendMessageRequest
from app.utils.jwt import get_current_user
from datetime import datetime
import random, string
from middleware.jwt_middleware import verify_jwt
api = APIRouter(prefix="/meetings", tags=["Meetings"])

def generate_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


@api.post("/create")
def create_meeting(data: CreateMeetingRequest, db: Session = Depends(get_db), request: Request = Depends(verify_jwt)):
    user_id = request.state.user.get("sub")
    code = generate_code()
    meeting = Meeting(title=data.title, host_id=user_id, code=code)
    db.add(meeting)
    db.commit()
    db.refresh(meeting)
    return {"message": "Meeting created", "code": meeting.code}


@api.post("/{code}/join")
def join_meeting(code: str, db: Session = Depends(get_db), request: Request = Depends(verify_jwt)):
    user_id = request.state.user.get("sub")
    meeting = db.query(Meeting).filter_by(code=code, is_active=True).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found or ended")

    already_joined = db.query(Participant).filter_by(meeting_id=meeting.id, user_id=user_id).first()
    if not already_joined:
        participant = Participant(user_id=user_id, meeting_id=meeting.id)
        db.add(participant)
        db.add(MeetingLog(meeting_id=meeting.id, user_id=user_id, action="joined"))
        db.commit()

    return {"message": "Joined meeting", "meeting_id": meeting.id}


@api.post("/{meeting_id}/end")
def end_meeting(meeting_id: int, db: Session = Depends(get_db), request: Request = Depends(verify_jwt)):
    user_id = request.state.user.get("sub")
    meeting = db.query(Meeting).filter_by(id=meeting_id, host_id=user_id).first()
    if not meeting:
        raise HTTPException(status_code=403, detail="Not authorized")
    meeting.is_active = False
    meeting.end_time = datetime.utcnow()
    db.commit()
    return {"message": "Meeting ended"}


@api.get("/my")
def get_user_meetings(db: Session = Depends(get_db), request: Request = Depends(verify_jwt)):
    user_id = request.state.user.get("sub")
    hosted = db.query(Meeting).filter_by(host_id=user_id).all()
    joined = db.query(Participant).filter_by(user_id=user_id).all()
    return {
        "hosted": [m.id for m in hosted],
        "joined": [p.meeting_id for p in joined]
    }


@api.get("/{meeting_id}/participants")
def get_participants(meeting_id: int, db: Session = Depends(get_db), request: Request = Depends(verify_jwt)):
    participants = db.query(Participant).filter_by(meeting_id=meeting_id).all()
    return [{"user_id": p.user_id, "muted": p.is_muted} for p in participants]


@api.post("/{meeting_id}/participants/mute/{user_id}")
def mute_user(meeting_id: int, user_id: int, db: Session = Depends(get_db), request: Request = Depends(verify_jwt)):
    requester_id = request.state.user.get("sub")
    meeting = db.query(Meeting).filter_by(id=meeting_id, host_id=requester_id).first()
    if not meeting:
        raise HTTPException(status_code=403, detail="Not authorized")
    participant = db.query(Participant).filter_by(meeting_id=meeting_id, user_id=user_id).first()
    if participant:
        participant.is_muted = True
        db.commit()
        return {"message": "User muted"}
    raise HTTPException(status_code=404, detail="Participant not found")


@api.post("/{meeting_id}/chat/send")
def send_chat(meeting_id: int, data: SendMessageRequest, db: Session = Depends(get_db), request: Request = Depends(verify_jwt)):
    user_id = request.state.user.get("sub")
    message = Message(sender_id=user_id, meeting_id=meeting_id, content=data.message)
    db.add(message)
    db.commit()
    return {"message": "Sent"}


@api.get("/{meeting_id}/chat")
def get_chat(meeting_id: int, db: Session = Depends(get_db), request: Request = Depends(verify_jwt)):
    messages = db.query(Message).filter_by(meeting_id=meeting_id).all()
    return [{"sender": m.sender_id, "content": m.content, "timestamp": m.timestamp} for m in messages]


@api.get("/{meeting_id}/logs")
def get_logs(meeting_id: int, db: Session = Depends(get_db), request: Request = Depends(verify_jwt)):
    logs = db.query(MeetingLog).filter_by(meeting_id=meeting_id).all()
    return [{"user_id": log.user_id, "action": log.action, "time": log.timestamp} for log in logs]
