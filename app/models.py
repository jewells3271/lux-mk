from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    memories = relationship("ExperienceMemory", back_populates="user")
    streams = relationship("StreamLog", back_populates="user")

class ExperienceMemory(Base):
    """Long-term synthesized memories (The 'Experience' from mk3.txt)"""
    __tablename__ = "experience_memories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)  # The summarized fact/pattern
    category = Column(String) # e.g., 'preference', 'fact', 'pattern'
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="memories")

class StreamLog(Base):
    """The raw conversation stream (The 'Stream' from mk3.txt)"""
    __tablename__ = "stream_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String) # 'user' or 'lux'
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="streams")

class DomainMemory(Base):
    """Structured data for Lux's job (Leads, State, User Profile from mk3.txt)"""
    __tablename__ = "domain_memories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    key = Column(String)    # e.g., 'name', 'token_id', 'status'
    value = Column(String)  # The structured value
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User")
