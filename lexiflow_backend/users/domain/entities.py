"""
Domain entities for user management.
These are pure Python dataclasses, independent of Django or any framework.
They represent the core business objects.
"""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from typing import Optional

@dataclass
class User:
    """
    Represents a registered user of the LexiFlow application.
    
    Attributes:
        id: Unique identifier (UUID)
        email: User's email address (used as login)
        full_name: Optional display name
        avatar_url: Optional profile picture URL
        created_at: Account creation timestamp
        updated_at: Last profile update timestamp
    """
    id: UUID
    email: str
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime = None
    updated_at: datetime = None

@dataclass
class UserPreferences:
    """
    Stores user-specific UI and reading preferences.
    
    Attributes:
        id: Unique identifier (UUID)
        user_id: Reference to the User (not stored directly, but used for linking)
        is_dark_mode: Dark/light theme preference
        language: Preferred language code (e.g., 'en', 'es')
        notifications_enabled: Whether to send push notifications
        font_size: Reading font size ('small', 'medium', 'large')
        reading_line_height: Line height multiplier (e.g., 1.6)
    """
    id: Optional[UUID]
    user_id: UUID
    is_dark_mode: bool = False
    language: str = "en"
    notifications_enabled: bool = True
    font_size: str = "medium"
    reading_line_height: float = 1.6