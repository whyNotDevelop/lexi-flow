"""
DRF Serializers for Word domain entities.

These serializers convert domain entities to/from JSON for API responses.
They maintain clean architecture by depending only on domain entities.
"""

from rest_framework import serializers
from words.domain.entities import Word, Definition


class DefinitionSerializer(serializers.Serializer):
    """
    Serializer for Definition domain entity.

    Handles serialization of word definitions including part of speech,
    meaning, examples, and synonyms.
    """
    id = serializers.UUIDField(read_only=True)
    meaning = serializers.CharField()
    part_of_speech = serializers.CharField()
    example = serializers.CharField(required=False, allow_null=True)
    synonyms = serializers.ListField(child=serializers.CharField(), default=list)
    order = serializers.IntegerField(default=0)


class WordSerializer(serializers.Serializer):
    """
    Serializer for Word domain entity.

    Handles serialization of complete word entries including definitions,
    pronunciation, and metadata.
    """
    id = serializers.UUIDField(read_only=True)
    text = serializers.CharField()
    language = serializers.CharField()
    phonetic = serializers.CharField(required=False, allow_null=True)
    audio_url = serializers.URLField(required=False, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)
    definitions = DefinitionSerializer(many=True, read_only=True)