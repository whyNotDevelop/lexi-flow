"""
Domain entities for words and definitions.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from uuid import UUID

@dataclass
class Definition:
    """
    A single definition of a word, including part of speech, meaning, example,
    and synonyms.
    
    Attributes:
        id: Unique identifier (UUID)
        meaning: The definition text
        part_of_speech: e.g., 'noun', 'verb', 'adjective'
        example: An example sentence showing usage
        synonyms: List of synonyms
        order: Display order (when multiple definitions exist)
    """
    id: Optional[UUID]
    meaning: str
    part_of_speech: str
    example: Optional[str] = None
    synonyms: List[str] = field(default_factory=list)
    order: int = 0

@dataclass
class Word:
    """
    A word entry, containing its text, pronunciation, and definitions.
    
    Attributes:
        id: Unique identifier (UUID)
        text: The word itself (e.g., "serendipity")
        language: Language code (default "en")
        phonetic: IPA pronunciation (optional)
        audio_url: URL to audio pronunciation (optional)
        created_at: Timestamp when first seen/looked up
        definitions: List of Definition objects (can be empty initially)
    """
    id: Optional[UUID]
    text: str
    language: str
    phonetic: Optional[str] = None
    audio_url: Optional[str] = None
    created_at: datetime = None
    definitions: List[Definition] = field(default_factory=list)