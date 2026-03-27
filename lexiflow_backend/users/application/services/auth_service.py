"""
AuthService: user authentication and profile management.

This service handles:
- User registration (create account with email/password)
- Profile updates (name, avatar)
- Preferences management (theme, language, notifications, font size)
- User lookup and profile retrieval

Note: Authentication (login, token generation) is typically handled via JWT middleware
or DRF authentication backends and is NOT part of this service. This service focuses
on user lifecycle management.

Clean Architecture principles:
- Service depends only on repository interfaces (UserRepository, PreferencesRepository).
- Password hashing is delegated to UserRepository.
- Business logic for user ops is centralized here.
"""

from typing import Optional
from uuid import UUID

from users.domain.entities import User, UserPreferences
from users.domain.interfaces import UserRepository, PreferencesRepository


class AuthService:
    """
    Manages user lifecycle: registration, profile updates, and preferences.

    Dependencies:
        - user_repo: UserRepository for user account management.
        - prefs_repo: PreferencesRepository for user preferences.
    """

    def __init__(
        self, user_repo: UserRepository, prefs_repo: PreferencesRepository
    ):
        """
        Initialize the AuthService.

        Args:
            user_repo: Repository for user account operations.
            prefs_repo: Repository for user preferences.
        """
        self.user_repo = user_repo
        self.prefs_repo = prefs_repo

    def register_user(
        self, email: str, password: str, full_name: Optional[str] = None
    ) -> Optional[User]:
        """
        Register a new user account.

        Args:
            email: Email address (used as login).
            password: Plaintext password (will be hashed by repository).
            full_name: Optional display name.

        Returns:
            The created User entity, or None if registration fails (e.g., email exists).
        """
        try:
            user = self.user_repo.create(email, password, full_name)
            
            # Create default preferences for the user
            self._create_default_preferences(user.id)
            
            return user
        except Exception:
            # Registration failed (e.g., duplicate email, DB error)
            return None

    def get_user(self, user_id: UUID) -> Optional[User]:
        """
        Retrieve a user by ID.

        Args:
            user_id: UUID of the user.

        Returns:
            The User entity, or None if not found.
        """
        return self.user_repo.get_by_id(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by email address.

        Args:
            email: Email address to search for.

        Returns:
            The User entity, or None if not found.
        """
        return self.user_repo.get_by_email(email)

    def update_profile(
        self,
        user_id: UUID,
        full_name: Optional[str] = None,
        avatar_url: Optional[str] = None,
    ) -> Optional[User]:
        """
        Update a user's profile information.

        Args:
            user_id: UUID of the user.
            full_name: New display name (optional).
            avatar_url: New avatar URL (optional).

        Returns:
            The updated User entity, or None if user not found.
        """
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return None

        # Update provided fields
        if full_name is not None:
            user.full_name = full_name
        if avatar_url is not None:
            user.avatar_url = avatar_url

        return self.user_repo.update(user)

    def get_preferences(self, user_id: UUID) -> Optional[UserPreferences]:
        """
        Retrieve a user's preferences.

        Args:
            user_id: UUID of the user.

        Returns:
            The UserPreferences entity, or None if not set.
        """
        return self.prefs_repo.get_for_user(user_id)

    def update_preferences(self, user_id: UUID, **kwargs) -> Optional[UserPreferences]:
        """
        Update one or more user preferences.

        Supported keys:
        - is_dark_mode (bool)
        - language (str)
        - notifications_enabled (bool)
        - font_size (str): 'small', 'medium', 'large'
        - reading_line_height (float)

        Args:
            user_id: UUID of the user.
            **kwargs: Preference fields to update.

        Returns:
            The updated UserPreferences entity, or None if user not found.
        """
        prefs = self.prefs_repo.get_for_user(user_id)
        if not prefs:
            # No preferences exist yet; create default and update
            prefs = UserPreferences(
                id=None,
                user_id=user_id,
                is_dark_mode=kwargs.get("is_dark_mode", False),
                language=kwargs.get("language", "en"),
                notifications_enabled=kwargs.get("notifications_enabled", True),
                font_size=kwargs.get("font_size", "medium"),
                reading_line_height=kwargs.get("reading_line_height", 1.6),
            )
            return self.prefs_repo.save(prefs)

        # Update existing preferences
        for key, value in kwargs.items():
            if hasattr(prefs, key):
                setattr(prefs, key, value)

        return self.prefs_repo.save(prefs)

    def _create_default_preferences(self, user_id: UUID) -> UserPreferences:
        """
        Create default preferences for a newly registered user.

        This is a private helper called during registration.

        Args:
            user_id: UUID of the new user.

        Returns:
            The created UserPreferences entity.
        """
        prefs = UserPreferences(
            id=None,
            user_id=user_id,
            is_dark_mode=False,
            language="en",
            notifications_enabled=True,
            font_size="medium",
            reading_line_height=1.6,
        )
        return self.prefs_repo.save(prefs)
