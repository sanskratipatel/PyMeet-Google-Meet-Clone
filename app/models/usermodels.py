from xmlrpc.client import DateTime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship 
from pydantic import datetime
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)

    role = relationship("Role", back_populates="users")


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    users = relationship("User", back_populates="role")



class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True)
    meeting_id = Column(Integer, ForeignKey("meeting_rooms.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    is_host = Column(Boolean, default=False)
    is_muted = Column(Boolean, default=False)
    is_video_on = Column(Boolean, default=True)
    hand_raised = Column(Boolean, default=False)
    joined_at = Column(DateTime, default=datetime.utcnow)
    left_at = Column(DateTime, nullable=True)

    meeting = relationship("MeetingRoom", back_populates="participants")
    user = relationship("User")

class Invite(Base):
    __tablename__ = "invites"

    id = Column(Integer, primary_key=True)
    meeting_id = Column(Integer, ForeignKey("meeting_rooms.id"))
    email = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending, accepted
    invited_at = Column(DateTime, default=datetime.utcnow)
