from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from .entities import Word, Definition

class WordRepository(ABC):
    """
    Interface for word and definition persistence.
    """
    @abstractmethod
    def get_by_id(self, word_id: UUID) -> Optional[Word]:
        """Retrieve a word by its ID."""
        pass

    @abstractmethod
    def find_by_text(self, text: str, language: str = "en") -> Optional[Word]:
        """
        Find a word by its exact text and language.
        Returns None if not found.
        """
        pass

    @abstractmethod
    def save(self, word: Word) -> Word:
        """
        Save a word and its definitions.
        If the word doesn't exist, it is created; if it does, it is updated.
        Returns the saved word with ID populated.
        """
        pass

    @abstractmethod
    def add_definition(self, word_id: UUID, definition: Definition) -> Definition:
        """
        Add a new definition to an existing word.
        Returns the definition with ID assigned.
        """
        pass

    @abstractmethod
    def get_definitions(self, word_id: UUID) -> List[Definition]:
        """Retrieve all definitions for a given word."""
        pass

class DictionaryProvider(ABC):
    """
    Interface for external dictionary APIs.
    """
    @abstractmethod
    def fetch_word(self, word: str, language: str = "en") -> Optional[Word]:
        """
        Fetch word data from an external source.
        Returns a fully populated Word entity (with definitions) if found,
        otherwise None.
        """
        pass