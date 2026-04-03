"""
VocabularyService: user vocabulary management (save, remove, search).

This service orchestrates saving words to a user's personal vocabulary list,
removing saved words, and searching the vocabulary.

Clean Architecture principles:
- Service depends only on repository interfaces (VocabularyRepository, WordRepository).
- All business logic for vocabulary operations is centralized here.
- Repositories handle persistence; the service enforces business rules.
"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from vocabulary.domain.entities import VocabularyEntry
from vocabulary.domain.interfaces import VocabularyRepository
from vocabulary.application.dtos import VocabularyEntryDTO
from words.domain.interfaces import WordRepository

class VocabularyService:
    def __init__(self, vocab_repo: VocabularyRepository, word_repo: WordRepository):
        self.vocab_repo = vocab_repo
        self.word_repo = word_repo

    def save_word(self, user_id: UUID, word_id: UUID) -> Optional[VocabularyEntryDTO]:
        """
        Add a word to a user's saved vocabulary.

        Process:
        1. Check if the word is already saved (prevent duplicates).
        2. Retrieve the word to get its definition for display.
        3. Create and save the vocabulary entry.
        4. Return the saved entry.

        Args:
            user_id: UUID of the user.
            word_id: UUID of the word to save.

        Returns:
            The saved VocabularyEntry if successful, None if word not found.
        """
        existing = self.vocab_repo.find_by_user_and_word(user_id, word_id)
        if existing:
            return None

        word = self.word_repo.get_by_id(word_id)
        if not word:
            return None

        meaning = self._get_primary_definition(word)
        entry = VocabularyEntry(
            id=None,
            user_id=user_id,
            word_id=word_id,
            meaning=meaning,
            saved_at=datetime.now(),
            review_count=0,
            last_reviewed_at=None,
        )
        saved = self.vocab_repo.add(entry)
        return VocabularyEntryDTO(
            id=saved.id,
            user_id=saved.user_id,
            word_id=saved.word_id,
            word_text=word.text,
            meaning=saved.meaning,
            saved_at=saved.saved_at,
            review_count=saved.review_count,
            last_reviewed_at=saved.last_reviewed_at,
        )

    def remove_word(self, user_id: UUID, word_id: UUID) -> bool:
        entry = self.vocab_repo.find_by_user_and_word(user_id, word_id)
        if not entry:
            return False
        self.vocab_repo.remove(entry.id)
        return True

    def get_user_vocabulary(self, user_id: UUID) -> List[VocabularyEntryDTO]:
        entries = self.vocab_repo.get_by_user(user_id)
        if not entries:
            return []
        word_ids = [e.word_id for e in entries]
        words = {w.id: w for w in self.word_repo.get_by_ids(word_ids)}  # bulk fetch
        dtos = []
        for entry in entries:
            word = words.get(entry.word_id)
            dtos.append(VocabularyEntryDTO(
                id=entry.id,
                user_id=entry.user_id,
                word_id=entry.word_id,
                word_text=word.text if word else "",
                meaning=entry.meaning,
                saved_at=entry.saved_at,
                review_count=entry.review_count,
                last_reviewed_at=entry.last_reviewed_at,
            ))
        return dtos

    def search_vocabulary(self, user_id: UUID, query: str) -> List[VocabularyEntryDTO]:
        entries = self.vocab_repo.search(user_id, query)
        if not entries:
            return []
        word_ids = [e.word_id for e in entries]
        words = {w.id: w for w in self.word_repo.get_by_ids(word_ids)}
        dtos = []
        for entry in entries:
            word = words.get(entry.word_id)
            dtos.append(VocabularyEntryDTO(
                id=entry.id,
                user_id=entry.user_id,
                word_id=entry.word_id,
                word_text=word.text if word else "",
                meaning=entry.meaning,
                saved_at=entry.saved_at,
                review_count=entry.review_count,
                last_reviewed_at=entry.last_reviewed_at,
            ))
        return dtos

    def is_word_saved(self, user_id: UUID, word_id: UUID) -> bool:
        entry = self.vocab_repo.find_by_user_and_word(user_id, word_id)
        return entry is not None

    def _get_primary_definition(self, word) -> str:
        if not word.definitions:
            return "Definition not available"
        return word.definitions[0].meaning