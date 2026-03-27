"""
HistoryService: lookup history management and querying.

This service manages the user's lookup history, providing methods to:
- Record new lookups
- Retrieve lookup history (with pagination)
- Clear history
- Query lookups within time ranges

Clean Architecture principles:
- Service depends only on HistoryRepository interface.
- Business logic for history operations is centralized.
- Repository handles persistence; service enforces business rules.
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from history.domain.entities import LookupHistory
from history.domain.interfaces import HistoryRepository


class HistoryService:
    """
    Manages user lookup history operations.

    Dependencies:
        - history_repo: HistoryRepository for history persistence and retrieval.
    """

    def __init__(self, history_repo: HistoryRepository):
        """
        Initialize the HistoryService.

        Args:
            history_repo: Repository for history management.
        """
        self.history_repo = history_repo

    def record_lookup(self, user_id: UUID, word_id: UUID) -> LookupHistory:
        """
        Record a new word lookup.

        Args:
            user_id: UUID of the user performing the lookup.
            word_id: UUID of the word being looked up.

        Returns:
            The created LookupHistory entry (with ID assigned).
        """
        history = LookupHistory(
            id=None,  # Let repository assign ID
            user_id=user_id,
            word_id=word_id,
            looked_up_at=datetime.now(),
        )
        return self.history_repo.add(history)

    def get_user_history(
        self, user_id: UUID, limit: int = 50, before: Optional[datetime] = None
    ) -> List[LookupHistory]:
        """
        Retrieve lookup history for a user.

        Args:
            user_id: UUID of the user.
            limit: Maximum number of entries to return (default 50).
            before: Optional timestamp; return entries older than this time.

        Returns:
            List of LookupHistory entries (most recent first).
        """
        return self.history_repo.get_by_user(user_id, limit, before)

    def delete_lookup(self, history_id: UUID) -> None:
        """
        Delete a single lookup history entry.

        Args:
            history_id: UUID of the history entry to delete.
        """
        self.history_repo.delete(history_id)

    def clear_user_history(self, user_id: UUID) -> int:
        """
        Delete all lookup history for a user.

        Args:
            user_id: UUID of the user.

        Returns:
            Number of history entries deleted.
        """
        return self.history_repo.clear_for_user(user_id)

    def get_lookup_count(self, user_id: UUID) -> int:
        """
        Get total number of lookups for a user.

        Args:
            user_id: UUID of the user.

        Returns:
            Total count of lookups.
        """
        return self.history_repo.count_by_user(user_id)

    def get_lookup_count_since(self, user_id: UUID, since: datetime) -> int:
        """
        Get number of lookups for a user since a specific time.

        Args:
            user_id: UUID of the user.
            since: Start time for counting.

        Returns:
            Count of lookups after the given time.
        """
        return self.history_repo.count_by_user_since(user_id, since)
