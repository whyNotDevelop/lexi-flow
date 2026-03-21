from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from .entities import VocabularyEntry

class VocabularyRepository(ABC):
    """
    Interface for saved vocabulary management.
    """
    @abstractmethod
    def add(self, entry: VocabularyEntry) -> VocabularyEntry:
        """
        Add a new word to the user's vocabulary.
        Returns the saved entry (with ID assigned).
        """
        pass

    @abstractmethod
    def get_by_user(self, user_id: UUID) -> List[VocabularyEntry]:
        """Retrieve all saved words for a user."""
        pass

    @abstractmethod
    def remove(self, entry_id: UUID) -> None:
        """Delete a vocabulary entry by its ID."""
        pass

    @abstractmethod
    def find_by_user_and_word(self, user_id: UUID, word_id: UUID) -> Optional[VocabularyEntry]:
        """Check if a specific word is already saved by a user."""
        pass

    @abstractmethod
    def search(self, user_id: UUID, query: str) -> List[VocabularyEntry]:
        """Search saved vocabulary by word text (case‑insensitive)."""
        pass