from sqlalchemy import Column, String, Text, DateTime, Enum, Float, ForeignKey, Integer
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional
from enum import Enum as PyEnum
from dataclasses import dataclass

# Create Base for SQLAlchemy models
Base = declarative_base()

# Define RecordingStatus enum for both SQLAlchemy and dataclasses
class RecordingStatus(PyEnum):
    ACTIVE = "active"
    PAUSED = "paused"
    ENDED = "ended"

# Database models
class UserDB(Base):
    __tablename__ = "users"
    
    id = Column(CHAR(36), primary_key=True)  # UUID
    google_id = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    display_name = Column(String(255), nullable=False)
    avatar_url = Column(String(512), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class RecordingDB(Base):
    __tablename__ = "recordings"
    
    id = Column(CHAR(36), primary_key=True)  # UUID
    user_id = Column(CHAR(36), ForeignKey("users.id"), nullable=False)
    status = Column(Enum(RecordingStatus), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    audio_file_path = Column(String(512), nullable=True)
    transcription_text = Column(Text, nullable=True)
    llm_provider = Column(String(255), nullable=False, default="requestyai")

class RecordingChunkDB(Base):
    __tablename__ = "recording_chunks"
    
    id = Column(CHAR(36), primary_key=True)  # UUID
    recording_id = Column(CHAR(36), ForeignKey("recordings.id"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    audio_blob_path = Column(String(512), nullable=False)
    duration_seconds = Column(Float, nullable=True)
    uploaded_at = Column(DateTime, server_default=func.now())

# Dataclasses for application logic
@dataclass
class User:
    id: str  # UUID
    google_id: str
    email: str
    display_name: str
    avatar_url: Optional[str]
    created_at: datetime
    updated_at: datetime

@dataclass
class Recording:
    id: str  # UUID
    user_id: str  # FK to User.id
    status: RecordingStatus
    created_at: datetime
    updated_at: datetime
    audio_file_path: Optional[str]
    transcription_text: Optional[str]
    llm_provider: str = "requestyai"

@dataclass
class RecordingChunk:
    id: str  # UUID
    recording_id: str  # FK to Recording.id
    chunk_index: int
    audio_blob_path: str
    duration_seconds: Optional[float]
    uploaded_at: datetime