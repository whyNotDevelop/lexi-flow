"""
VocabularyService: user vocabulary management (save, remove, search).

This service orchestrates saving words to a user's personal vocabulary list,
removing saved words, and searching the vocabulary.

Clean Architecture principles:
- Service depends only on repository interfaces (VocabularyRepository, WordRepository).
- All business logic for vocabulary operations is centralized here.
- Repositories handle persistence; the service enforces business rules.
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from vocabulary.domain.entities import VocabularyEntry
from vocabulary.domain.interfaces import VocabularyRepository
from words.domain.entities import Word
from words.domain.interfaces import WordRepository


class VocabularyService:
    """
    Manages user vocabulary lists: saving, removing, and searching words.

    Dependencies:
        - vocab_repo: VocabularyRepository for vocabulary persistence.
        - word_repo: WordRepository for retrieving word definitions.
    """

    def __init__(
        self, vocab_repo: VocabularyRepository, word_repo: WordRepository
    ):
        """
        Initialize the VocabularyService.

        Args:
            vocab_repo: Repository for vocabulary management.
            word_repo: Repository for word lookup (to verify word exists).
        """
        self.vocab_repo = vocab_repo
        self.word_repo = word_repo

    def save_word(self, user_id: UUID, word_id: UUID) -> Optional[VocabularyEntry]:
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
         # Step 1: Check if already saved
        existing = self.vocab_repo.find_by_user_and_word(user_id, word_id)
        if existing:
            # Return None (or raise exception) to indicate duplicate
            return None

        # Step 2: Retrieve the word to get its definition
        word = self.word_repo.get_by_id(word_id)
        if not word:
            # Word not found
            return None

        # Step 3: Extract the primary definition
        meaning = self._get_primary_definition(word)

        # Step 4: Create and save vocabulary entry
        entry = VocabularyEntry(
            id=None,  # Let repository assign ID
            user_id=user_id,
            word_id=word_id,
            meaning=meaning,
            saved_at=datetime.now(),
            review_count=0,
            last_reviewed_at=None,
        )

        return self.vocab_repo.add(entry)

    def remove_word(self, user_id: UUID, word_id: UUID) -> bool:
        """
        Remove a word from a user's saved vocabulary.

        Args:
            user_id: UUID of the user.
            word_id: UUID of the word to remove.

        Returns:
            True if the word was removed, False if it wasn't in the vocabulary.
        """
        # Find the vocabulary entry
        entry = self.vocab_repo.find_by_user_and_word(user_id, word_id)
        if not entry:
            return False

        # Remove it
        self.vocab_repo.remove(entry.id)
        return True

    def get_user_vocabulary(self, user_id: UUID) -> List[VocabularyEntry]:
        """
        Retrieve all saved words for a user.

        Args:
            user_id: UUID of the user.

        Returns:
            List of VocabularyEntry objects (empty list if none saved).
        """
        return self.vocab_repo.get_by_user(user_id)

    def search_vocabulary(self, user_id: UUID, query: str) -> List[VocabularyEntry]:
        """
        Search a user's saved vocabulary by word text.

        Args:
            user_id: UUID of the user.
            query: Search string (case-insensitive).

        Returns:
            List of matching VocabularyEntry objects.
        """
        return self.vocab_repo.search(user_id, query)

    def is_word_saved(self, user_id: UUID, word_id: UUID) -> bool:
        """
        Check if a word is already in a user's vocabulary.

        Args:
            user_id: UUID of the user.
            word_id: UUID of the word.

        Returns:
            True if the word is saved, False otherwise.
        """
        entry = self.vocab_repo.find_by_user_and_word(user_id, word_id)
        return entry is not None

    def _get_primary_definition(self, word: Word) -> str:
        """
        Extract the primary (first) definition from a word.

        This is a private helper to ensure consistent definition selection.

        Args:
            word: The Word entity.

        Returns:
            The meaning of the first definition, or a default message.
        """
        if not word.definitions:
            return "Definition not available"
        
        # Return the first definition's meaning
        return word.definitions[0].meaning
