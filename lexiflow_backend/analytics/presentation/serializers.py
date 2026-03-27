"""
DRF Serializers for Analytics domain entities.

These serializers handle reading session data and statistics.
"""

from rest_framework import serializers
from analytics.domain.entities import ReadingSession


class ReadingSessionSerializer(serializers.Serializer):
    """
    Serializer for ReadingSession domain entity.

    Handles serialization of reading session data.
    """
    id = serializers.UUIDField(read_only=True)
    user_id = serializers.UUIDField(read_only=True)
    book_id = serializers.CharField(required=False, allow_null=True)
    book_title = serializers.CharField(required=False, allow_null=True)
    started_at = serializers.DateTimeField(read_only=True)
    ended_at = serializers.DateTimeField(read_only=True, required=False)
    duration_seconds = serializers.IntegerField(read_only=True, default=0)
    words_looked_up = serializers.IntegerField(read_only=True, default=0)