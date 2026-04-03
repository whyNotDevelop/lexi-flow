# vocabulary/application/dtos.py
from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class VocabularyEntryDTO:
    """Data Transfer Object for vocabulary entries with word text."""
    id: UUID
    user_id: UUID
    word_id: UUID
    word_text: str
    meaning: str
    saved_at: datetime
    review_count: int
    last_reviewed_at: datetime = None