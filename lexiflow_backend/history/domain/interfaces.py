from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from .entities import LookupHistory

class HistoryRepository(ABC):
    """
    Interface for lookup history persistence.
    """
    @abstractmethod
    def add(self, entry: LookupHistory) -> LookupHistory:
        """
        Record a new lookup.
        Returns the saved entry (with ID).
        """
        pass

    @abstractmethod
    def get_by_user(self, user_id: UUID, limit: int = 50, before: Optional[datetime] = None) -> List[LookupHistory]:
        """
        Retrieve the most recent lookups for a user.
        If `before` is given, return entries older than that timestamp.
        """
        pass

    @abstractmethod
    def delete(self, history_id: UUID) -> None:
        """Delete a single history entry by its ID."""
        pass

    @abstractmethod
    def clear_for_user(self, user_id: UUID) -> int:
        """
        Delete all history entries for a user.
        Returns the number of deleted entries.
        """
        pass