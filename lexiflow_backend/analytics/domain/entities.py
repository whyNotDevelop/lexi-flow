"""
Domain entities for reading sessions.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

@dataclass
class ReadingSession:
    """
    Tracks a continuous reading session.
    
    Attributes:
        id: Unique identifier (UUID)
        user_id: Reference to the User
        book_id: Optional external book identifier (e.g., ISBN)
        book_title: Book title for display
        started_at: Session start time
        ended_at: Session end time (null if still active)
        duration_seconds: Total session length in seconds
        words_looked_up: Number of word lookups during the session
    """
    id: Optional[UUID]
    user_id: UUID
    book_id: Optional[str] = None
    book_title: Optional[str] = None
    started_at: datetime = None
    ended_at: Optional[datetime] = None
    duration_seconds: int = 0
    words_looked_up: int = 0