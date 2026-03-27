"""
Unit tests for VocabularyService.
"""
import pytest
from datetime import datetime
from unittest.mock import Mock
from uuid import uuid4

from vocabulary.application.services.vocabulary_service import VocabularyService
from vocabulary.domain.entities import VocabularyEntry
from words.domain.entities import Word, Definition


@pytest.mark.django_db
class TestVocabularyService:
    """Test suite for the VocabularyService."""

    def setup_method(self):
        """Set up mocks for each test."""
        self.vocab_repo = Mock()
        self.word_repo = Mock()
        self.service = VocabularyService(self.vocab_repo, self.word_repo)
        
        self.user_id = uuid4()
        self.word_id = uuid4()
        self.vocab_entry_id = uuid4()

    def test_save_word_success(self):
        """Test: save a new word to vocabulary."""
        word = Word(
            id=self.word_id,
            text="perspicacious",
            language="en",
            phonetic=None,
            audio_url=None,
            created_at=datetime.now(),
            definitions=[
                Definition(
                    id=uuid4(),
                    meaning="Having keen judgment or insight.",
                    part_of_speech="adjective",
                    example="Her perspicacious observations were valuable.",
                    synonyms=["astute", "perceptive"],
                    order=0,
                )
            ],
        )
        
        self.vocab_repo.find_by_user_and_word.return_value = None
        self.word_repo.get_by_id.return_value = word
        
        saved_entry = VocabularyEntry(
            id=self.vocab_entry_id,
            user_id=self.user_id,
            word_id=self.word_id,
            meaning="Having keen judgment or insight.",
            saved_at=datetime.now(),
            review_count=0,
            last_reviewed_at=None,
        )
        self.vocab_repo.add.return_value = saved_entry

        result = self.service.save_word(self.user_id, self.word_id)

        assert result == saved_entry
        assert result.user_id == self.user_id
        assert result.word_id == self.word_id
        self.vocab_repo.find_by_user_and_word.assert_called_once_with(
            self.user_id, self.word_id
        )
        self.word_repo.get_by_id.assert_called_once_with(self.word_id)
        self.vocab_repo.add.assert_called_once()

    def test_save_word_already_exists(self):
        """Test: saving a word that's already in vocabulary returns existing entry."""
        existing_entry = VocabularyEntry(
            id=self.vocab_entry_id,
            user_id=self.user_id,
            word_id=self.word_id,
            meaning="Some meaning",
            saved_at=datetime.now(),
        )
        self.vocab_repo.find_by_user_and_word.return_value = existing_entry

        result = self.service.save_word(self.user_id, self.word_id)

        assert result == existing_entry
        self.word_repo.get_by_id.assert_not_called()
        self.vocab_repo.add.assert_not_called()

    def test_save_word_not_found(self):
        """Test: save word that doesn't exist in word repository."""
        self.vocab_repo.find_by_user_and_word.return_value = None
        self.word_repo.get_by_id.return_value = None

        result = self.service.save_word(self.user_id, self.word_id)

        assert result is None
        self.vocab_repo.add.assert_not_called()

    def test_save_word_with_no_definitions(self):
        """Test: save a word with no definitions available."""
        word = Word(
            id=self.word_id,
            text="test",
            language="en",
            phonetic=None,
            audio_url=None,
            created_at=datetime.now(),
            definitions=[],  # No definitions
        )

        self.vocab_repo.find_by_user_and_word.return_value = None
        self.word_repo.get_by_id.return_value = word
        
        saved_entry = VocabularyEntry(
            id=self.vocab_entry_id,
            user_id=self.user_id,
            word_id=self.word_id,
            meaning="Definition not available",
            saved_at=datetime.now(),
        )
        self.vocab_repo.add.return_value = saved_entry

        result = self.service.save_word(self.user_id, self.word_id)

        assert result == saved_entry
        # Verify the default message was used
        call_args = self.vocab_repo.add.call_args[0][0]
        assert call_args.meaning == "Definition not available"

    def test_remove_word_success(self):
        """Test: remove a word from vocabulary."""
        entry = VocabularyEntry(
            id=self.vocab_entry_id,
            user_id=self.user_id,
            word_id=self.word_id,
            meaning="Some meaning",
            saved_at=datetime.now(),
        )
        self.vocab_repo.find_by_user_and_word.return_value = entry

        result = self.service.remove_word(self.user_id, self.word_id)

        assert result is True
        self.vocab_repo.remove.assert_called_once_with(self.vocab_entry_id)

    def test_remove_word_not_found(self):
        """Test: remove a word that's not in vocabulary."""
        self.vocab_repo.find_by_user_and_word.return_value = None

        result = self.service.remove_word(self.user_id, self.word_id)

        assert result is False
        self.vocab_repo.remove.assert_not_called()

    def test_get_user_vocabulary(self):
        """Test: retrieve all saved words for a user."""
        entries = [
            VocabularyEntry(
                id=uuid4(),
                user_id=self.user_id,
                word_id=uuid4(),
                meaning="Definition 1",
                saved_at=datetime.now(),
            ),
            VocabularyEntry(
                id=uuid4(),
                user_id=self.user_id,
                word_id=uuid4(),
                meaning="Definition 2",
                saved_at=datetime.now(),
            ),
        ]
        self.vocab_repo.get_by_user.return_value = entries

        result = self.service.get_user_vocabulary(self.user_id)

        assert result == entries
        assert len(result) == 2
        self.vocab_repo.get_by_user.assert_called_once_with(self.user_id)

    def test_get_user_vocabulary_empty(self):
        """Test: retrieve vocabulary for user with no saved words."""
        self.vocab_repo.get_by_user.return_value = []

        result = self.service.get_user_vocabulary(self.user_id)

        assert result == []
        self.vocab_repo.get_by_user.assert_called_once_with(self.user_id)

    def test_search_vocabulary(self):
        """Test: search user vocabulary by query."""
        entries = [
            VocabularyEntry(
                id=uuid4(),
                user_id=self.user_id,
                word_id=uuid4(),
                meaning="A quality of being quick",
                saved_at=datetime.now(),
            )
        ]
        self.vocab_repo.search.return_value = entries

        result = self.service.search_vocabulary(self.user_id, "quick")

        assert result == entries
        assert len(result) == 1
        self.vocab_repo.search.assert_called_once_with(self.user_id, "quick")

    def test_search_vocabulary_no_matches(self):
        """Test: search vocabulary with no matching results."""
        self.vocab_repo.search.return_value = []

        result = self.service.search_vocabulary(self.user_id, "nonexistent")

        assert result == []
        self.vocab_repo.search.assert_called_once_with(self.user_id, "nonexistent")

    def test_is_word_saved_true(self):
        """Test: check if word is saved (word exists in vocabulary)."""
        entry = VocabularyEntry(
            id=self.vocab_entry_id,
            user_id=self.user_id,
            word_id=self.word_id,
            meaning="Some meaning",
            saved_at=datetime.now(),
        )
        self.vocab_repo.find_by_user_and_word.return_value = entry

        result = self.service.is_word_saved(self.user_id, self.word_id)

        assert result is True

    def test_is_word_saved_false(self):
        """Test: check if word is saved (word not in vocabulary)."""
        self.vocab_repo.find_by_user_and_word.return_value = None

        result = self.service.is_word_saved(self.user_id, self.word_id)

        assert result is False
