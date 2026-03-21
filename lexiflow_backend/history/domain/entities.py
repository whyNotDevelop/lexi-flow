"""
Domain entities for lookup history.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

@dataclass
class LookupHistory:
    """
    Records every time a user looks up a word.
    
    Attributes:
        id: Unique identifier (UUID)
        user_id: Reference to the User
        word_id: Reference to the Word
        looked_up_at: Timestamp of the lookup
    """
    id: Optional[UUID]
    user_id: UUID
    word_id: UUID
    looked_up_at: datetime