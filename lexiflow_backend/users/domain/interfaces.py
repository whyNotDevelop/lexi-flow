"""
Repository interfaces for user management.
These abstract away the persistence mechanism (database, cache, etc.).
Application services will depend on these interfaces, not on concrete implementations.
"""
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from .entities import User, UserPreferences

class UserRepository(ABC):
    """
    Interface for user persistence operations.
    """
    @abstractmethod
    def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Retrieve a user by their UUID."""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by email address."""
        pass

    @abstractmethod
    def create(self, email: str, password: str, full_name: Optional[str] = None) -> User:
        """
        Create a new user with the given credentials.
        The password is hashed internally.
        Returns the created User entity (with ID assigned).
        """
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        """
        Update an existing user's profile.
        Returns the updated User entity.
        """
        pass

class PreferencesRepository(ABC):
    """
    Interface for user preferences persistence.
    """
    @abstractmethod
    def get_for_user(self, user_id: UUID) -> Optional[UserPreferences]:
        """Retrieve preferences for a given user."""
        pass

    @abstractmethod
    def save(self, preferences: UserPreferences) -> UserPreferences:
        """
        Save or update preferences.
        Returns the saved preferences (with ID if new).
        """
        pass