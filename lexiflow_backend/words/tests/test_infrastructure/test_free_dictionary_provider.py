"""
Unit tests for FreeDictionaryProvider.
"""
import pytest
import logging
import requests
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from words.infrastructure.providers.free_dictionary_provider import (
    FreeDictionaryProvider,
)


class TestFreeDictionaryProvider:
    """Test suite for FreeDictionaryProvider."""

    def setup_method(self):
        """Set up test fixtures."""
        self.provider = FreeDictionaryProvider()

    @patch("words.infrastructure.providers.free_dictionary_provider.requests.get")
    def test_fetch_word_success(self, mock_get):
        """Test: successfully fetch word from API."""
        api_response = {
            "word": "hello",
            "phonetic": "/həˈloʊ/",
            "phonetics": [{"audio": "https://example.com/hello.mp3"}],
            "meanings": [
                {
                    "partOfSpeech": "interjection",
                    "definitions": [
                        {
                            "definition": "Used as a greeting or to begin a conversation.",
                            "example": "Hello! How are you?",
                            "synonyms": ["hi", "hey"],
                        }
                    ],
                }
            ],
        }

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [api_response]
        mock_get.return_value = mock_response

        result = self.provider.fetch_word("hello", "en")

        assert result is not None
        assert result.text == "hello"
        assert result.language == "en"
        assert result.phonetic == "/həˈloʊ/"
        assert result.audio_url == "https://example.com/hello.mp3"
        assert len(result.definitions) == 1
        assert result.definitions[0].meaning == "Used as a greeting or to begin a conversation."
        assert result.definitions[0].part_of_speech == "interjection"

    @patch("words.infrastructure.providers.free_dictionary_provider.requests.get")
    def test_fetch_word_multiple_definitions(self, mock_get):
        """Test: fetch word with multiple definitions."""
        api_response = {
            "word": "run",
            "phonetic": "/rʌn/",
            "phonetics": [],
            "meanings": [
                {
                    "partOfSpeech": "verb",
                    "definitions": [
                        {
                            "definition": "Move at a speed faster than a walk.",
                            "example": "She runs every morning.",
                            "synonyms": ["sprint", "jog"],
                        },
                        {
                            "definition": "Operate or function.",
                            "example": "The engine is running.",
                            "synonyms": [],
                        },
                    ],
                },
                {
                    "partOfSpeech": "noun",
                    "definitions": [
                        {
                            "definition": "An act or instance of running.",
                            "example": "I went for a run.",
                            "synonyms": ["jog"],
                        }
                    ],
                },
            ],
        }

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [api_response]
        mock_get.return_value = mock_response

        result = self.provider.fetch_word("run")

        assert result is not None
        assert len(result.definitions) == 3
        assert result.definitions[0].part_of_speech == "verb"
        assert result.definitions[1].part_of_speech == "verb"
        assert result.definitions[2].part_of_speech == "noun"

    @patch("words.infrastructure.providers.free_dictionary_provider.requests.get")
    def test_fetch_word_not_found(self, mock_get):
        """Test: word not found returns None."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = self.provider.fetch_word("nonexistentword123456")

        assert result is None

    @patch("words.infrastructure.providers.free_dictionary_provider.requests.get")
    def test_fetch_word_network_error(self, mock_get):
        """Test: network error returns None."""
        import requests

        mock_get.side_effect = requests.exceptions.ConnectionError("Network error")

        result = self.provider.fetch_word("hello")

        assert result is None

    @patch("words.infrastructure.providers.free_dictionary_provider.requests.get")
    def test_fetch_word_timeout(self, mock_get):
        """Test: timeout returns None."""
        import requests

        mock_get.side_effect = requests.exceptions.Timeout("Request timeout")

        result = self.provider.fetch_word("hello")

        assert result is None

    @patch("words.infrastructure.providers.free_dictionary_provider.requests.get")
    def test_fetch_word_http_error(self, mock_get):
        """Test: HTTP error returns None."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Server error")
        mock_get.return_value = mock_response

        with patch("words.infrastructure.providers.free_dictionary_provider.logger"):
            result = self.provider.fetch_word("hello")

        assert result is None

    @patch("words.infrastructure.providers.free_dictionary_provider.requests.get")
    def test_fetch_word_invalid_json(self, mock_get):
        """Test: invalid JSON response returns None."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response

        with patch("words.infrastructure.providers.free_dictionary_provider.logger"):
            result = self.provider.fetch_word("hello")

        assert result is None

    @patch("words.infrastructure.providers.free_dictionary_provider.requests.get")
    def test_fetch_word_empty_response(self, mock_get):
        """Test: empty response returns None."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        result = self.provider.fetch_word("hello")

        assert result is None

    @patch("words.infrastructure.providers.free_dictionary_provider.requests.get")
    def test_fetch_word_custom_language(self, mock_get):
        """Test: fetch word in different language."""
        api_response = {
            "word": "hola",
            "phonetic": None,
            "phonetics": [],
            "meanings": [
                {
                    "partOfSpeech": "interjection",
                    "definitions": [
                        {
                            "definition": "Used as a greeting.",
                            "example": None,
                            "synonyms": [],
                        }
                    ],
                }
            ],
        }

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [api_response]
        mock_get.return_value = mock_response

        result = self.provider.fetch_word("hola", "es")

        assert result is not None
        assert result.language == "es"
        mock_get.assert_called_once()
        call_args = mock_get.call_args[0][0]
        assert "es/hola" in call_args

    @patch("words.infrastructure.providers.free_dictionary_provider.requests.get")
    def test_fetch_word_normalizes_text_to_lowercase(self, mock_get):
        """Test: word is normalized to lowercase in API call."""
        api_response = {
            "word": "hello",
            "phonetic": None,
            "phonetics": [],
            "meanings": [],
        }

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [api_response]
        mock_get.return_value = mock_response

        self.provider.fetch_word("HELLO", "en")

        # Verify lowercase was used in URL
        call_args = mock_get.call_args[0][0]
        assert "hello" in call_args.lower()

    @patch("words.infrastructure.providers.free_dictionary_provider.requests.get")
    def test_fetch_word_missing_optional_fields(self, mock_get):
        """Test: handle missing optional fields gracefully."""
        api_response = {
            "word": "test",
            "meanings": [
                {
                    "partOfSpeech": "noun",
                    "definitions": [
                        {
                            "definition": "A procedure to assess something.",
                            # Missing: example, synonyms
                        }
                    ],
                }
            ],
            # Missing: phonetic, phonetics
        }

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [api_response]
        mock_get.return_value = mock_response

        result = self.provider.fetch_word("test")

        assert result is not None
        assert result.phonetic is None
        assert result.audio_url is None
        assert result.definitions[0].example is None
        assert result.definitions[0].synonyms == []

    @patch("words.infrastructure.providers.free_dictionary_provider.requests.get")
    def test_fetch_word_preserves_definition_order(self, mock_get):
        """Test: definitions maintain their order."""
        api_response = {
            "word": "word",
            "phonetic": None,
            "phonetics": [],
            "meanings": [
                {
                    "partOfSpeech": "noun",
                    "definitions": [
                        {"definition": "First definition", "synonyms": []},
                        {"definition": "Second definition", "synonyms": []},
                        {"definition": "Third definition", "synonyms": []},
                    ],
                }
            ],
        }

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [api_response]
        mock_get.return_value = mock_response

        result = self.provider.fetch_word("word")

        assert result.definitions[0].order == 0
        assert result.definitions[1].order == 1
        assert result.definitions[2].order == 2
        assert result.definitions[0].meaning == "First definition"
        assert result.definitions[1].meaning == "Second definition"
        assert result.definitions[2].meaning == "Third definition"
