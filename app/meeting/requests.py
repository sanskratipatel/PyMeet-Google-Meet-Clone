from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class CreateMeetingRequest(BaseModel):
    title: str
    scheduled_time: Optional[datetime] = None
    password: Optional[str] = None

class JoinMeetingRequest(BaseModel):
    code: str
    password: Optional[str] = None

class InviteParticipantsRequest(BaseModel):
    emails: List[EmailStr]


from pydantic import BaseModel

class CreateMeetingRequest(BaseModel):
    title: str | None = None

class JoinMeetingRequest(BaseModel):
    code: str

class SendMessageRequest(BaseModel):
    message: str
