from abc import ABC, abstractmethod
from typing import List, Dict, Any
from uuid import UUID
from .entities import ReadingSession

class ReadingSessionRepository(ABC):
    """
    Interface for reading session persistence.
    """
    @abstractmethod
    def create(self, session: ReadingSession) -> ReadingSession:
        """Start a new reading session."""
        pass

    @abstractmethod
    def update(self, session: ReadingSession) -> ReadingSession:
        """Update an existing session (e.g., end it)."""
        pass

    @abstractmethod
    def get_by_user(self, user_id: UUID, limit: int = 10) -> List[ReadingSession]:
        """Retrieve recent reading sessions for a user."""
        pass

    @abstractmethod
    def get_stats(self, user_id: UUID) -> Dict[str, Any]:
        """
        Return aggregated statistics for a user:
        - total lookups
        - lookups today/this week
        - total reading time
        - etc.
        """
        pass