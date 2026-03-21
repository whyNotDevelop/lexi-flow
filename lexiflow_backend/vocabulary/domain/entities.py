"""
Domain entities for saved vocabulary.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

@dataclass
class VocabularyEntry:
    """
    Represents a word saved by a user to their personal vocabulary list.
    
    Attributes:
        id: Unique identifier (UUID)
        user_id: Reference to the User
        word_id: Reference to the Word
        meaning: Cached primary meaning (for quick display)
        saved_at: When the word was saved
        review_count: Number of times reviewed (for future spaced repetition)
        last_reviewed_at: Last review timestamp
    """
    id: Optional[UUID]
    user_id: UUID
    word_id: UUID
    meaning: str
    saved_at: datetime
    review_count: int = 0
    last_reviewed_at: Optional[datetime] = None