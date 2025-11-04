from typing import List, Optional
from sqlalchemy.orm import Session
import uuid
from datetime import datetime
from ..models import Recording, RecordingDB, RecordingChunkDB, RecordingStatus

class MySQLRecordingRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def create_recording(self, user_id: str) -> Recording:
        """Create a new recording entry in the database"""
        recording_id = str(uuid.uuid4())
        now = datetime.now()
        
        recording_db = RecordingDB(
            id=recording_id,
            user_id=user_id,
            status=RecordingStatus.ACTIVE.value,
            created_at=now,
            updated_at=now,
            llm_provider="requestyai"
        )
        
        self.db_session.add(recording_db)
        self.db_session.commit()
        self.db_session.refresh(recording_db)
        
        # Convert to dataclass for application logic
        recording = Recording(
            id=recording_id,
            user_id=user_id,
            status=RecordingStatus.ACTIVE,
            created_at=now,
            updated_at=now,
            audio_file_path=None,
            transcription_text=None,
            llm_provider="requestyai"
        )
        return recording
    
    def get_recording(self, recording_id: str) -> Recording:
        """Retrieve a recording by its ID"""
        recording_db = self.db_session.query(RecordingDB).filter(RecordingDB.id == recording_id).first()
        if not recording_db:
            raise ValueError(f"Recording with id {recording_id} not found")
        
        # Convert to dataclass for application logic
        recording = Recording(
            id=str(recording_db.id),
            user_id=str(recording_db.user_id),
            status=RecordingStatus(str(recording_db.status)),
            created_at=recording_db.created_at,
            updated_at=recording_db.updated_at,
            audio_file_path=str(recording_db.audio_file_path) if recording_db.audio_file_path else None,
            transcription_text=str(recording_db.transcription_text) if recording_db.transcription_text else None,
            llm_provider=str(recording_db.llm_provider)
        )
        return recording
    
    def list_recordings(self, user_id: str) -> List[Recording]:
        """List all recordings for a user"""
        recordings_db = self.db_session.query(RecordingDB).filter(RecordingDB.user_id == user_id).all()
        
        # Convert to dataclasses for application logic
        recordings = [
            Recording(
                id=str(r.id),
                user_id=str(r.user_id),
                status=RecordingStatus(str(r.status)),
                created_at=r.created_at,
                updated_at=r.updated_at,
                audio_file_path=str(r.audio_file_path) if r.audio_file_path else None,
                transcription_text=str(r.transcription_text) if r.transcription_text else None,
                llm_provider=str(r.llm_provider)
            )
            for r in recordings_db
        ]
        return recordings
    
    def add_chunk(self, recording_id: str, chunk_path: str, index: int) -> None:
        """Add a chunk to a recording"""
        chunk_db = RecordingChunkDB(
            id=str(uuid.uuid4()),
            recording_id=recording_id,
            chunk_index=index,
            audio_blob_path=chunk_path
        )
        
        self.db_session.add(chunk_db)
        self.db_session.commit()
    
    def mark_paused(self, recording_id: str) -> None:
        """Mark a recording as paused"""
        recording_db = self.db_session.query(RecordingDB).filter(RecordingDB.id == recording_id).first()
        if recording_db:
            recording_db.status = RecordingStatus.PAUSED.value
            recording_db.updated_at = datetime.now()
            self.db_session.commit()
    
    def mark_ended(self, recording_id: str, full_audio_path: str, transcription: str) -> None:
        """Mark a recording as ended and store the transcription"""
        recording_db = self.db_session.query(RecordingDB).filter(RecordingDB.id == recording_id).first()
        if recording_db:
            recording_db.status = RecordingStatus.ENDED.value
            recording_db.audio_file_path = full_audio_path
            recording_db.transcription_text = transcription
            recording_db.updated_at = datetime.now()
            self.db_session.commit()