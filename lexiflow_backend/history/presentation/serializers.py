"""
DRF Serializers for History domain entities.

These serializers handle lookup history records.
"""

from rest_framework import serializers
from history.domain.entities import LookupHistory


class LookupHistorySerializer(serializers.Serializer):
    """
    Serializer for LookupHistory domain entity.

    Handles serialization of word lookup history entries.
    """
    id = serializers.UUIDField(read_only=True)
    user_id = serializers.UUIDField(read_only=True)
    word_id = serializers.UUIDField(read_only=True)
    looked_up_at = serializers.DateTimeField(read_only=True)