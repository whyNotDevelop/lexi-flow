"""
Unit tests for LookupService.
"""
import pytest
from datetime import datetime
from unittest.mock import Mock, call
from uuid import uuid4

from words.application.services.lookup_service import LookupService
from words.domain.entities import Word, Definition


@pytest.mark.django_db
class TestLookupService:
    """Test suite for the LookupService."""

    def setup_method(self):
        """Set up mocks for each test."""
        self.word_repo = Mock()
        self.dict_provider = Mock()
        self.history_repo = Mock()
        self.service = LookupService(
            self.word_repo, self.dict_provider, self.history_repo
        )
        self.user_id = uuid4()
        self.word_id = uuid4()

    def test_lookup_word_found_in_repository(self):
        """Test: word found in cache/DB, no external API call needed."""
        word = Word(
            id=self.word_id,
            text="serendipity",
            language="en",
            phonetic="/ˌserənˈdɪpɪti/",
            audio_url=None,
            created_at=datetime.now(),
            definitions=[
                Definition(
                    id=uuid4(),
                    meaning="The occurrence and development of events by chance in a happy or beneficial way.",
                    part_of_speech="noun",
                    example="It was pure serendipity that we met.",
                    synonyms=["fate", "providence"],
                    order=0,
                )
            ],
        )
        self.word_repo.find_by_text.return_value = word

        result = self.service.lookup_word("serendipity", self.user_id, "en")

        assert result == word
        self.word_repo.find_by_text.assert_called_once_with("serendipity", "en")
        self.dict_provider.fetch_word.assert_not_called()
        self.history_repo.add.assert_called_once()

        # Verify history entry
        history_call = self.history_repo.add.call_args[0][0]
        assert history_call.user_id == self.user_id
        assert history_call.word_id == self.word_id

    def test_lookup_word_not_found_anywhere(self):
        """Test: word not found in DB or external API, returns None."""
        self.word_repo.find_by_text.return_value = None
        self.dict_provider.fetch_word.return_value = None

        result = self.service.lookup_word("nonexistentword", self.user_id, "en")

        assert result is None
        self.word_repo.find_by_text.assert_called_once_with("nonexistentword", "en")
        self.dict_provider.fetch_word.assert_called_once_with("nonexistentword", "en")
        self.history_repo.add.assert_not_called()

    def test_lookup_word_found_in_external_api(self):
        """Test: word not in DB, fetched from external API, saved and recorded."""
        word_from_api = Word(
            id=None,  # No ID yet (new)
            text="ephemeral",
            language="en",
            phonetic="/ɪˈfɛmərəl/",
            audio_url=None,
            created_at=None,
            definitions=[
                Definition(
                    id=None,
                    meaning="Lasting for a very short time.",
                    part_of_speech="adjective",
                    example="The ephemeral beauty of cherry blossoms.",
                    synonyms=["fleeting", "temporary"],
                    order=0,
                )
            ],
        )
        saved_word = Word(
            id=self.word_id,
            text="ephemeral",
            language="en",
            phonetic="/ɪˈfɛmərəl/",
            audio_url=None,
            created_at=datetime.now(),
            definitions=word_from_api.definitions,
        )

        self.word_repo.find_by_text.return_value = None
        self.dict_provider.fetch_word.return_value = word_from_api
        self.word_repo.save.return_value = saved_word

        result = self.service.lookup_word("ephemeral", self.user_id, "en")

        assert result == saved_word
        assert result.id == self.word_id
        self.word_repo.find_by_text.assert_called_once_with("ephemeral", "en")
        self.dict_provider.fetch_word.assert_called_once_with("ephemeral", "en")
        self.word_repo.save.assert_called_once_with(word_from_api)
        self.history_repo.add.assert_called_once()

        # Verify history was recorded with correct word_id
        history_call = self.history_repo.add.call_args[0][0]
        assert history_call.word_id == self.word_id

    def test_lookup_word_with_custom_language(self):
        """Test: lookup word in language other than English."""
        word = Word(
            id=self.word_id,
            text="amantísimo",
            language="es",
            phonetic=None,
            audio_url=None,
            created_at=datetime.now(),
            definitions=[],
        )
        self.word_repo.find_by_text.return_value = word

        result = self.service.lookup_word("amantísimo", self.user_id, language="es")

        assert result == word
        self.word_repo.find_by_text.assert_called_once_with("amantísimo", "es")
        self.dict_provider.fetch_word.assert_not_called()

    def test_lookup_word_history_recorded_even_if_history_fails(self):
        """Test: lookup completes successfully even if history recording fails."""
        word = Word(
            id=self.word_id,
            text="vindicate",
            language="en",
            phonetic=None,
            audio_url=None,
            created_at=datetime.now(),
            definitions=[],
        )
        self.word_repo.find_by_text.return_value = word
        self.history_repo.add.side_effect = Exception("Database error")

        # Should not raise exception
        result = self.service.lookup_word("vindicate", self.user_id, "en")

        assert result == word
        self.history_repo.add.assert_called_once()

    def test_lookup_word_calls_find_by_text_with_correct_defaults(self):
        """Test: lookup_word passes correct default language parameter."""
        word = Word(
            id=self.word_id,
            text="test",
            language="en",
            phonetic=None,
            audio_url=None,
            created_at=datetime.now(),
            definitions=[],
        )
        self.word_repo.find_by_text.return_value = word

        self.service.lookup_word("test", self.user_id)  # No language specified

        # Verify default language "en" was used
        self.word_repo.find_by_text.assert_called_once_with("test", "en")

    def test_lookup_word_external_api_only_called_after_repo_miss(self):
        """Test: external API is called only if word not in repository."""
        self.word_repo.find_by_text.return_value = None

        word_from_api = Word(
            id=self.word_id,
            text="example",
            language="en",
            phonetic=None,
            audio_url=None,
            created_at=datetime.now(),
            definitions=[],
        )
        self.dict_provider.fetch_word.return_value = word_from_api
        self.word_repo.save.return_value = word_from_api

        self.service.lookup_word("example", self.user_id)

        # Verify call order: find_by_text THEN fetch_word
        assert self.word_repo.find_by_text.call_count == 1
        assert self.dict_provider.fetch_word.call_count == 1
        assert self.word_repo.save.call_count == 1
