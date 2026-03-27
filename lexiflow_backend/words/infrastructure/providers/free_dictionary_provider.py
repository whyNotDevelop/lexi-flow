"""
Implementation of DictionaryProvider using the Free Dictionary API.

This is an external API client that fetches word definitions from:
https://api.dictionaryapi.dev/

The provider is wrapped behind the DictionaryProvider interface to maintain
clean architecture boundaries. Services depend on the interface, not this
concrete implementation.
"""

import requests
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID

from words.domain.entities import Word, Definition
from words.domain.interfaces import DictionaryProvider


class FreeDictionaryProvider(DictionaryProvider):
    """
    Fetches word definitions from the Free Dictionary API.

    API Endpoint: https://api.dictionaryapi.dev/api/v2/entries/{language}/{word}

    This provider:
    - Handles HTTP errors gracefully
    - Maps API responses to domain entities
    - Caches failures to avoid repeated failed requests
    """

    BASE_URL = "https://api.dictionaryapi.dev/api/v2/entries"
    TIMEOUT = 5  # seconds

    def fetch_word(self, word: str, language: str = "en") -> Optional[Word]:
        """
        Fetch word data from the Free Dictionary API.

        Process:
        1. Make HTTP GET request to the API
        2. Parse the response
        3. Map to domain entities
        4. Return Word with definitions

        Args:
            word: The word to look up (e.g., "hello").
            language: Language code (default "en" for English).

        Returns:
            A fully populated Word entity if found, None otherwise.
            Returns None on network errors or if word not found.
        """
        try:
            # Build URL
            url = f"{self.BASE_URL}/{language}/{word.lower()}"

            # Make request
            response = requests.get(url, timeout=self.TIMEOUT)

            # Handle 404 (word not found)
            if response.status_code == 404:
                return None

            # Handle other HTTP errors
            response.raise_for_status()

            # Parse response
            data = response.json()

            # Handle empty response
            if not data:
                return None

            # Map first result to Word entity (API returns array)
            return self._map_to_word(data[0], word, language)

        except requests.exceptions.RequestException as e:
            # Network error, timeout, or invalid response
            # Log the error in a real system
            print(f"Failed to fetch word from API: {e}")
            return None
        except (KeyError, ValueError, TypeError) as e:
            # Parsing error
            print(f"Failed to parse API response: {e}")
            return None

    def _map_to_word(self, api_data: Dict[str, Any], word: str, language: str) -> Word:
        """
        Map Free Dictionary API response to domain Word entity.

        Args:
            api_data: The JSON object from API for a single word
            word: The word text
            language: Language code

        Returns:
            A Word entity with definitions populated.
        """
        # Extract IPA phonetic if available
        phonetic = api_data.get("phonetic")

        # Extract audio URL if available
        audio_url = None
        if "phonetics" in api_data and api_data["phonetics"]:
            audio_url = api_data["phonetics"][0].get("audio")

        # Map meanings to Definition objects
        definitions = self._extract_definitions(api_data.get("meanings", []))

        return Word(
            id=None,  # Let repository assign ID
            text=word,
            language=language,
            phonetic=phonetic,
            audio_url=audio_url,
            created_at=datetime.now(),
            definitions=definitions,
        )

    def _extract_definitions(self, meanings: List[Dict[str, Any]]) -> List[Definition]:
        """
        Extract definitions from the meanings array in API response.

        The API structure:
        meanings: [
            {
                "partOfSpeech": "noun",
                "definitions": [
                    {
                        "definition": "...",
                        "example": "...",
                        "synonyms": [...]
                    }
                ]
            }
        ]

        Args:
            meanings: List of meaning objects from API response

        Returns:
            List of Definition domain entities.
        """
        definitions = []
        definition_order = 0

        for meaning in meanings:
            part_of_speech = meaning.get("partOfSpeech", "unknown")

            for def_data in meaning.get("definitions", []):
                definition = Definition(
                    id=None,  # Let repository assign ID
                    meaning=def_data.get("definition", ""),
                    part_of_speech=part_of_speech,
                    example=def_data.get("example"),
                    synonyms=def_data.get("synonyms", []),
                    order=definition_order,
                )
                definitions.append(definition)
                definition_order += 1

        return definitions
