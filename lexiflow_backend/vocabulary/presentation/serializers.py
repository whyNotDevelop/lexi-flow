"""
DRF Serializers for Vocabulary domain entities.

These serializers handle saved vocabulary entries.
"""

from rest_framework import serializers
from vocabulary.domain.entities import VocabularyEntry
from words.infrastructure.models import WordModel  # import only for serialization; careful with coupling


class VocabularyEntrySerializer(serializers.Serializer):
    """
    Serializer for VocabularyEntry domain entity.

    Handles serialization of saved words in user's vocabulary.
    """
    id = serializers.UUIDField(read_only=True)
    user_id = serializers.UUIDField(read_only=True)
    word_id = serializers.UUIDField()
    word = serializers.SerializerMethodField()  # Add this line
    meaning = serializers.CharField()
    saved_at = serializers.DateTimeField(read_only=True)
    review_count = serializers.IntegerField(read_only=True, default=0)
    last_reviewed_at = serializers.DateTimeField(read_only=True, required=False)

    def get_word(self, obj):
        """
        Retrieve the word text from the related WordModel.
        obj is a VocabularyEntry domain entity, which has a word_id.
        """
        try:
            word_model = WordModel.objects.get(id=obj.word_id)
            return word_model.text
        except WordModel.DoesNotExist:
            return ""