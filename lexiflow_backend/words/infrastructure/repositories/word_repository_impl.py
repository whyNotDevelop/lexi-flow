"""
Word repository with Redis caching.
"""
import json
from typing import Optional, List
from uuid import UUID
from django.core.cache import cache
from ...domain.entities import Word, Definition
from ...domain.interfaces import WordRepository
from ..models import WordModel, DefinitionModel

class WordRepositoryImpl(WordRepository):
    """
    Implements word persistence with a two‑layer cache:
    - Redis for fast retrieval
    - PostgreSQL as the backing store
    """
    CACHE_TTL = 86400          # 24 hours
    CACHE_KEY_PREFIX = "lexiflow:word:"

    def _normalize_word(self, text: str) -> str:
        """Normalize word text for consistent caching."""
        return text.lower().strip()

    def _cache_key(self, text: str, language: str = "en") -> str:
        """Generate Redis cache key."""
        normalized = self._normalize_word(text)
        return f"{self.CACHE_KEY_PREFIX}{language}:{normalized}"

    def _to_entity(self, model: WordModel) -> Word:
        """Convert Django model to domain entity."""
        definitions = [
            Definition(
                id=def_model.id,
                meaning=def_model.meaning,
                part_of_speech=def_model.part_of_speech,
                example=def_model.example,
                synonyms=def_model.synonyms,
                order=def_model.order,
            )
            for def_model in model.definitions.all()
        ]
        return Word(
            id=model.id,
            text=model.text,
            language=model.language,
            phonetic=model.phonetic,
            audio_url=model.audio_url,
            created_at=model.created_at,
            definitions=definitions,
        )

    def find_by_text(self, text: str, language: str = "en") -> Optional[Word]:
        # 1. Try Redis cache
        cache_key = self._cache_key(text, language)
        cached = cache.get(cache_key)
        if cached:
            # For simplicity, we assume the cached value is a Word entity.
            # In a production system, you might store serialized JSON.
            return cached

        # 2. Try database
        try:
            model = WordModel.objects.get(text=text, language=language)
            entity = self._to_entity(model)
            # Store in cache for future requests
            cache.set(cache_key, entity, self.CACHE_TTL)
            return entity
        except WordModel.DoesNotExist:
            return None

    def save(self, word: Word) -> Word:
        """
        Save a word and its definitions. If the word already exists, update.
        """
        # Save/update the WordModel
        model, created = WordModel.objects.update_or_create(
            text=word.text,
            language=word.language,
            defaults={
                'phonetic': word.phonetic,
                'audio_url': word.audio_url,
            }
        )
        if not word.id:
            word.id = model.id
        word.created_at = model.created_at

        # Save definitions
        for def_entity in word.definitions:
            def_model, _ = DefinitionModel.objects.update_or_create(
                id=def_entity.id,
                defaults={
                    'word': model,
                    'part_of_speech': def_entity.part_of_speech,
                    'meaning': def_entity.meaning,
                    'example': def_entity.example or '',
                    'synonyms': def_entity.synonyms,
                    'order': def_entity.order,
                }
            )
            if not def_entity.id:
                def_entity.id = def_model.id

        # Update cache
        cache_key = self._cache_key(word.text, word.language)
        cache.set(cache_key, word, self.CACHE_TTL)
        return word

    def add_definition(self, word_id: UUID, definition: Definition) -> Definition:
        """
        Add a new definition to an existing word.
        """
        try:
            word_model = WordModel.objects.get(id=word_id)
        except WordModel.DoesNotExist:
            raise ValueError(f"Word with id {word_id} not found")

        def_model = DefinitionModel.objects.create(
            word=word_model,
            part_of_speech=definition.part_of_speech,
            meaning=definition.meaning,
            example=definition.example or '',
            synonyms=definition.synonyms,
            order=definition.order,
        )
        definition.id = def_model.id
        # Invalidate cache for this word (or update it)
        cache_key = self._cache_key(word_model.text, word_model.language)
        cache.delete(cache_key)
        return definition

    def get_definitions(self, word_id: UUID) -> List[Definition]:
        """
        Retrieve all definitions for a given word.
        """
        definitions = DefinitionModel.objects.filter(word_id=word_id).order_by('order')
        return [
            Definition(
                id=def_model.id,
                meaning=def_model.meaning,
                part_of_speech=def_model.part_of_speech,
                example=def_model.example,
                synonyms=def_model.synonyms,
                order=def_model.order,
            )
            for def_model in definitions
        ]