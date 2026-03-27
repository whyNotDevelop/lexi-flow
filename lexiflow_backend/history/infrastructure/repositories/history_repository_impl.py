"""
Concrete repository for lookup history using Django ORM.
"""
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from ...domain.entities import LookupHistory
from ...domain.interfaces import HistoryRepository
from ..models import LookupHistoryModel

class HistoryRepositoryImpl(HistoryRepository):
    """Implements history persistence with Django ORM."""

    def _to_entity(self, model: LookupHistoryModel) -> LookupHistory:
        """Convert ORM model to domain entity."""
        return LookupHistory(
            id=model.id,
            user_id=model.user_id,
            word_id=model.word_id,
            looked_up_at=model.looked_up_at,
        )

    def add(self, entry: LookupHistory) -> LookupHistory:
        """Record a new lookup."""
        model = LookupHistoryModel.objects.create(
            user_id=entry.user_id,
            word_id=entry.word_id,
        )
        entry.id = model.id
        entry.looked_up_at = model.looked_up_at
        return entry

    def get_by_user(self, user_id: UUID, limit: int = 50, before: Optional[datetime] = None) -> List[LookupHistory]:
        """Retrieve most recent lookups for a user."""
        qs = LookupHistoryModel.objects.filter(user_id=user_id)
        if before:
            qs = qs.filter(looked_up_at__lt=before)
        qs = qs.order_by('-looked_up_at')[:limit]
        return [self._to_entity(m) for m in qs]

    def delete(self, history_id: UUID) -> None:
        """Delete a single history entry."""
        LookupHistoryModel.objects.filter(id=history_id).delete()

    def clear_for_user(self, user_id: UUID) -> int:
        """Delete all history for a user; return number deleted."""
        count, _ = LookupHistoryModel.objects.filter(user_id=user_id).delete()
        return count

    def count_by_user(self, user_id: UUID) -> int:
        """Count total lookup history entries for a user."""
        return LookupHistoryModel.objects.filter(user_id=user_id).count()

    def count_by_user_since(self, user_id: UUID, since: datetime) -> int:
        """Count lookup history entries for a user since the provided time."""
        return LookupHistoryModel.objects.filter(user_id=user_id, looked_up_at__gte=since).count()