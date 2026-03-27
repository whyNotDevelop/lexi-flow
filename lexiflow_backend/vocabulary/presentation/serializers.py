"""
DRF Serializers for Vocabulary domain entities.

These serializers handle saved vocabulary entries.
"""

from rest_framework import serializers
from vocabulary.domain.entities import VocabularyEntry


class VocabularyEntrySerializer(serializers.Serializer):
    """
    Serializer for VocabularyEntry domain entity.

    Handles serialization of saved words in user's vocabulary.
    """
    id = serializers.UUIDField(read_only=True)
    user_id = serializers.UUIDField(read_only=True)
    word_id = serializers.UUIDField()
    meaning = serializers.CharField()
    saved_at = serializers.DateTimeField(read_only=True)
    review_count = serializers.IntegerField(read_only=True, default=0)
    last_reviewed_at = serializers.DateTimeField(read_only=True, required=False)