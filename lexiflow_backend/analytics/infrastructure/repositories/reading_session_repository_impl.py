"""
Concrete repository for reading sessions using Django ORM.
"""
from datetime import datetime
from typing import List, Dict, Any
from uuid import UUID
from django.db.models import Sum, Count
from ...domain.entities import ReadingSession
from ...domain.interfaces import ReadingSessionRepository
from ..models import ReadingSessionModel

class ReadingSessionRepositoryImpl(ReadingSessionRepository):
    """Implements reading session persistence with Django ORM."""

    def _to_entity(self, model: ReadingSessionModel) -> ReadingSession:
        return ReadingSession(
            id=model.id,
            user_id=model.user_id,
            book_id=model.book_id,
            book_title=model.book_title,
            started_at=model.started_at,
            ended_at=model.ended_at,
            duration_seconds=model.duration_seconds,
            words_looked_up=model.words_looked_up,
        )

    def create(self, session: ReadingSession) -> ReadingSession:
        """Create a new reading session."""
        model = ReadingSessionModel.objects.create(
            user_id=session.user_id,
            book_id=session.book_id,
            book_title=session.book_title,
        )
        session.id = model.id
        session.started_at = model.started_at
        return session

    def update(self, session: ReadingSession) -> ReadingSession:
        """Update an existing session (e.g., end it)."""
        model = ReadingSessionModel.objects.get(id=session.id)
        model.ended_at = session.ended_at
        model.duration_seconds = session.duration_seconds
        model.words_looked_up = session.words_looked_up
        model.save()
        return self._to_entity(model)

    def get_by_user(self, user_id: UUID, limit: int = 10) -> List[ReadingSession]:
        """Retrieve recent sessions for a user."""
        models = ReadingSessionModel.objects.filter(user_id=user_id).order_by('-started_at')[:limit]
        return [self._to_entity(m) for m in models]

    def get_stats(self, user_id: UUID) -> Dict[str, Any]:
        """Return aggregated statistics for a user."""
        # Basic stats: total lookups, total reading time
        # We'll implement a simple version; can be extended later.
        lookups_count = HistoryRepositoryImpl().get_by_user(user_id).count()  # type: ignore – we'll import properly later
        reading_time = ReadingSessionModel.objects.filter(user_id=user_id).aggregate(total=Sum('duration_seconds'))['total'] or 0
        return {
            "lookups_total": lookups_count,
            "reading_time_seconds": reading_time,
            # Additional stats can be added later
        }