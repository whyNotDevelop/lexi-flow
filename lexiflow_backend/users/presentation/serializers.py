"""
DRF Serializers for User domain entities.

These serializers handle user registration, profile management, and preferences.
"""

from rest_framework import serializers
from users.domain.entities import User, UserPreferences


class UserSerializer(serializers.Serializer):
    """
    Serializer for User domain entity.

    Handles user profile data for registration and profile updates.
    """
    id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField()
    full_name = serializers.CharField(required=False, allow_null=True)
    avatar_url = serializers.URLField(required=False, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class UserRegistrationSerializer(serializers.Serializer):
    """
    Serializer for user registration.

    Includes password field for registration (not returned in responses).
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    full_name = serializers.CharField(required=False, allow_null=True)


class UserPreferencesSerializer(serializers.Serializer):
    """
    Serializer for UserPreferences domain entity.

    Handles user UI and reading preferences.
    """
    id = serializers.UUIDField(read_only=True)
    user_id = serializers.UUIDField(read_only=True)
    is_dark_mode = serializers.BooleanField(default=False)
    language = serializers.CharField(default="en")
    notifications_enabled = serializers.BooleanField(default=True)
    font_size = serializers.ChoiceField(choices=['small', 'medium', 'large'], default='medium')
    reading_line_height = serializers.FloatField(default=1.6, min_value=1.0, max_value=2.0)