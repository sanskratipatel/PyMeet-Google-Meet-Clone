from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class MessageResponse(BaseModel):
    message: str

class MeetingResponse(BaseModel):
    id: int
    title: str
    code: str
    scheduled_time: Optional[datetime]
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True
