"""
LookupService: word lookup with caching, external API fallback, and history tracking.

This service orchestrates the process of looking up a word:
1. Check the word repository (which uses Redis and DB caching).
2. If not found, fetch from external dictionary API.
3. Save the word to the repository.
4. Record the lookup in history.

This follows the Clean Architecture principle of separation of concerns:
- Repositories handle persistence (DB + cache).
- External providers handle API calls.
- The service orchestrates the workflow and enforces business rules.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from django.utils import timezone 

from words.domain.entities import Word
from words.domain.interfaces import WordRepository, DictionaryProvider
from history.domain.entities import LookupHistory
from history.domain.interfaces import HistoryRepository


class LookupService:
    """
    Orchestrates word lookups with multi-layer resolution:
    Cache (Redis) → Database → External API.

    Dependencies:
        - word_repo: WordRepository for word persistence and caching.
        - dict_provider: DictionaryProvider for external API calls.
        - history_repo: HistoryRepository for recording lookup history.
    """

    def __init__(
        self,
        word_repo: WordRepository,
        dict_provider: DictionaryProvider,
        history_repo: HistoryRepository,
    ):
        """
        Initialize the LookupService with required repositories and providers.

        Args:
            word_repo: Repository for word persistence (with caching).
            dict_provider: External dictionary provider.
            history_repo: Repository for recording lookup history.
        """
        self.word_repo = word_repo
        self.dict_provider = dict_provider
        self.history_repo = history_repo

    def lookup_word(
        self, word_text: str, user_id: UUID, language: str = "en"
    ) -> Optional[Word]:
        """
        Look up a word and record the lookup in history.

        Process:
        1. Try to find the word in the cache/DB (includes Redis check).
        2. If not found, fetch from the external dictionary API.
        3. If found externally, save it to the DB (and cache).
        4. Record the lookup in history.
        5. Return the Word entity.

        Args:
            word_text: The word to look up (e.g., "serendipity").
            user_id: UUID of the user performing the lookup.
            language: Language code (default "en" for English).

        Returns:
            A Word entity with definitions if found, None otherwise.
            The Word is populated from cache/DB or external source.
        """
        # Step 1: Try repository (which checks Redis and DB)
        word = self.word_repo.find_by_text(word_text, language)
        if word:
            self._record_history(user_id, word.id)
            return word

        # Step 2: Fetch from external dictionary provider
        word = self.dict_provider.fetch_word(word_text, language)
        if not word:
            # Word not found anywhere
            return None

        # Step 3: Save word to repository (populates cache)
        word = self.word_repo.save(word)

        # Step 4: Record lookup in history
        self._record_history(user_id, word.id)

        return word

    def _record_history(self, user_id: UUID, word_id: UUID) -> None:
        """
        Record a word lookup in user history.

        This is a private helper to avoid redundant history recording.
        Catches potential history repository errors gracefully to avoid
        disrupting the lookup flow.

        Args:
            user_id: UUID of the user.
            word_id: UUID of the word being looked up.
        """
        try:
            history = LookupHistory(
                id=None,  # Let the repository assign the ID
                user_id=user_id,
                word_id=word_id,
                looked_up_at=timezone.now(),
            )
            self.history_repo.add(history)
        except Exception as e:
            # Log the error but don't fail the lookup
            # In a real system, this would use a logger
            print(f"Failed to record lookup history: {e}")
