"""
Concrete repository for saved vocabulary using Django ORM.
"""
from typing import List, Optional
from uuid import UUID
from django.db.models import Q
from ...domain.entities import VocabularyEntry
from ...domain.interfaces import VocabularyRepository
from ..models import VocabularyEntryModel
from words.infrastructure.models import WordModel

class VocabularyRepositoryImpl(VocabularyRepository):
    """Implements vocabulary persistence with Django ORM."""

    def _to_entity(self, model: VocabularyEntryModel) -> VocabularyEntry:
        """Convert ORM model to domain entity."""
        return VocabularyEntry(
            id=model.id,
            user_id=model.user_id,
            word_id=model.word_id,
            meaning=model.meaning,
            saved_at=model.saved_at,
            review_count=model.review_count,
            last_reviewed_at=model.last_reviewed_at,
        )

    def add(self, entry: VocabularyEntry) -> VocabularyEntry:
        """Save a new vocabulary entry."""
        model = VocabularyEntryModel.objects.create(
            user_id=entry.user_id,
            word_id=entry.word_id,
            meaning=entry.meaning,
            review_count=entry.review_count,
            last_reviewed_at=entry.last_reviewed_at,
        )
        entry.id = model.id
        entry.saved_at = model.saved_at
        return entry

    def get_by_user(self, user_id: UUID) -> List[VocabularyEntry]:
        """Retrieve all saved words for a user, ordered newest first."""
        models = VocabularyEntryModel.objects.filter(user_id=user_id).select_related('word')
        return [self._to_entity(m) for m in models]

    def remove(self, entry_id: UUID) -> None:
        """Delete a vocabulary entry by ID."""
        VocabularyEntryModel.objects.filter(id=entry_id).delete()

    def find_by_user_and_word(self, user_id: UUID, word_id: UUID) -> Optional[VocabularyEntry]:
        """Check if a specific word is already saved by the user."""
        try:
            model = VocabularyEntryModel.objects.get(user_id=user_id, word_id=word_id)
            return self._to_entity(model)
        except VocabularyEntryModel.DoesNotExist:
            return None

    def search(self, user_id: UUID, query: str) -> List[VocabularyEntry]:
        """Search saved vocabulary by word text (case‑insensitive)."""
        models = VocabularyEntryModel.objects.filter(
            user_id=user_id,
            word__text__icontains=query
        ).select_related('word')
        return [self._to_entity(m) for m in models]