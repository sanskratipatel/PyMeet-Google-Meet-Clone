# models/meeting_models.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime

class Meeting(Base):
    __tablename__ = "meetings"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=True)
    host_id = Column(Integer, ForeignKey("users.id"))
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    host = relationship("User")
    participants = relationship("Participant", back_populates="meeting")
    messages = relationship("Message", back_populates="meeting")


class Participant(Base):
    __tablename__ = "participants"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    meeting_id = Column(Integer, ForeignKey("meetings.id"))
    is_muted = Column(Boolean, default=False)
    is_video_on = Column(Boolean, default=True)

    meeting = relationship("Meeting", back_populates="participants")
    user = relationship("User")


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    meeting_id = Column(Integer, ForeignKey("meetings.id"))
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    sender = relationship("User")
    meeting = relationship("Meeting", back_populates="messages")


class MeetingLog(Base):
    __tablename__ = "meeting_logs"
    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    meeting = relationship("Meeting")
