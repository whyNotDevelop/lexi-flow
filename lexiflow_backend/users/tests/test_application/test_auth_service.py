"""
Unit tests for AuthService.
"""
import pytest
from datetime import datetime
from unittest.mock import Mock, call
from uuid import uuid4

from users.application.services.auth_service import AuthService
from users.domain.entities import User, UserPreferences


@pytest.mark.django_db
class TestAuthService:
    """Test suite for the AuthService."""

    def setup_method(self):
        """Set up mocks for each test."""
        self.user_repo = Mock()
        self.prefs_repo = Mock()
        self.service = AuthService(self.user_repo, self.prefs_repo)
        
        self.user_id = uuid4()
        self.email = "test@example.com"

    def test_register_user_success(self):
        """Test: register a new user successfully."""
        new_user = User(
            id=self.user_id,
            email=self.email,
            full_name="John Doe",
            avatar_url=None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        
        default_prefs = UserPreferences(
            id=uuid4(),
            user_id=self.user_id,
            is_dark_mode=False,
            language="en",
            notifications_enabled=True,
            font_size="medium",
            reading_line_height=1.6,
        )
        
        self.user_repo.create.return_value = new_user
        self.prefs_repo.save.return_value = default_prefs

        result = self.service.register_user(self.email, "password123", "John Doe")

        assert result == new_user
        assert result.id == self.user_id
        self.user_repo.create.assert_called_once_with(
            self.email, "password123", "John Doe"
        )
        self.prefs_repo.save.assert_called_once()

    def test_register_user_without_full_name(self):
        """Test: register a user without providing full name."""
        new_user = User(
            id=self.user_id,
            email=self.email,
            full_name=None,
            avatar_url=None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        
        self.user_repo.create.return_value = new_user
        self.prefs_repo.save.return_value = Mock()

        result = self.service.register_user(self.email, "password123")

        assert result == new_user
        self.user_repo.create.assert_called_once_with(self.email, "password123", None)

    def test_register_user_email_already_exists(self):
        """Test: register fails if email already exists."""
        self.user_repo.create.side_effect = Exception("Duplicate email")

        result = self.service.register_user(self.email, "password123")

        assert result is None
        self.prefs_repo.save.assert_not_called()

    def test_get_user(self):
        """Test: retrieve a user by ID."""
        user = User(
            id=self.user_id,
            email=self.email,
            full_name="Jane Doe",
            avatar_url="https://example.com/avatar.jpg",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self.user_repo.get_by_id.return_value = user

        result = self.service.get_user(self.user_id)

        assert result == user
        self.user_repo.get_by_id.assert_called_once_with(self.user_id)

    def test_get_user_not_found(self):
        """Test: get user returns None if not found."""
        self.user_repo.get_by_id.return_value = None

        result = self.service.get_user(self.user_id)

        assert result is None

    def test_get_user_by_email(self):
        """Test: retrieve a user by email."""
        user = User(
            id=self.user_id,
            email=self.email,
            full_name="John Doe",
            avatar_url=None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self.user_repo.get_by_email.return_value = user

        result = self.service.get_user_by_email(self.email)

        assert result == user
        self.user_repo.get_by_email.assert_called_once_with(self.email)

    def test_get_user_by_email_not_found(self):
        """Test: get user by email returns None if not found."""
        self.user_repo.get_by_email.return_value = None

        result = self.service.get_user_by_email(self.email)

        assert result is None

    def test_update_profile_full_name_only(self):
        """Test: update user profile with new full name."""
        user = User(
            id=self.user_id,
            email=self.email,
            full_name="John Doe",
            avatar_url=None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        
        updated_user = User(
            id=self.user_id,
            email=self.email,
            full_name="Jane Doe",
            avatar_url=None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        
        self.user_repo.get_by_id.return_value = user
        self.user_repo.update.return_value = updated_user

        result = self.service.update_profile(self.user_id, full_name="Jane Doe")

        assert result == updated_user
        assert result.full_name == "Jane Doe"
        self.user_repo.update.assert_called_once()

    def test_update_profile_avatar_url_only(self):
        """Test: update user profile with new avatar URL."""
        user = User(
            id=self.user_id,
            email=self.email,
            full_name="John Doe",
            avatar_url=None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        
        updated_user = User(
            id=self.user_id,
            email=self.email,
            full_name="John Doe",
            avatar_url="https://example.com/new-avatar.jpg",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        
        self.user_repo.get_by_id.return_value = user
        self.user_repo.update.return_value = updated_user

        result = self.service.update_profile(
            self.user_id, avatar_url="https://example.com/new-avatar.jpg"
        )

        assert result == updated_user
        assert result.avatar_url == "https://example.com/new-avatar.jpg"

    def test_update_profile_both_fields(self):
        """Test: update user profile with both name and avatar."""
        user = User(
            id=self.user_id,
            email=self.email,
            full_name="John Doe",
            avatar_url=None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        
        updated_user = User(
            id=self.user_id,
            email=self.email,
            full_name="Jane Doe",
            avatar_url="https://example.com/avatar.jpg",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        
        self.user_repo.get_by_id.return_value = user
        self.user_repo.update.return_value = updated_user

        result = self.service.update_profile(
            self.user_id,
            full_name="Jane Doe",
            avatar_url="https://example.com/avatar.jpg",
        )

        assert result == updated_user

    def test_update_profile_user_not_found(self):
        """Test: update profile for non-existent user."""
        self.user_repo.get_by_id.return_value = None

        result = self.service.update_profile(self.user_id, full_name="Jane Doe")

        assert result is None
        self.user_repo.update.assert_not_called()

    def test_get_preferences(self):
        """Test: retrieve user preferences."""
        prefs = UserPreferences(
            id=uuid4(),
            user_id=self.user_id,
            is_dark_mode=True,
            language="es",
            notifications_enabled=False,
            font_size="large",
            reading_line_height=2.0,
        )
        self.prefs_repo.get_for_user.return_value = prefs

        result = self.service.get_preferences(self.user_id)

        assert result == prefs
        assert result.is_dark_mode is True
        self.prefs_repo.get_for_user.assert_called_once_with(self.user_id)

    def test_get_preferences_not_found(self):
        """Test: get preferences returns None if not set."""
        self.prefs_repo.get_for_user.return_value = None

        result = self.service.get_preferences(self.user_id)

        assert result is None

    def test_update_preferences_existing(self):
        """Test: update preferences that already exist."""
        existing_prefs = UserPreferences(
            id=uuid4(),
            user_id=self.user_id,
            is_dark_mode=False,
            language="en",
            notifications_enabled=True,
            font_size="medium",
            reading_line_height=1.6,
        )
        
        updated_prefs = UserPreferences(
            id=existing_prefs.id,
            user_id=self.user_id,
            is_dark_mode=True,
            language="en",
            notifications_enabled=True,
            font_size="medium",
            reading_line_height=1.6,
        )
        
        self.prefs_repo.get_for_user.return_value = existing_prefs
        self.prefs_repo.save.return_value = updated_prefs

        result = self.service.update_preferences(self.user_id, is_dark_mode=True)

        assert result == updated_prefs
        assert result.is_dark_mode is True
        self.prefs_repo.save.assert_called_once()

    def test_update_preferences_non_existing_creates_new(self):
        """Test: updating preferences for non-existing user creates new defaults."""
        self.prefs_repo.get_for_user.return_value = None
        
        new_prefs = UserPreferences(
            id=uuid4(),
            user_id=self.user_id,
            is_dark_mode=True,
            language="es",
            notifications_enabled=False,
            font_size="large",
            reading_line_height=1.8,
        )
        
        self.prefs_repo.save.return_value = new_prefs

        result = self.service.update_preferences(
            self.user_id,
            is_dark_mode=True,
            language="es",
            notifications_enabled=False,
            font_size="large",
            reading_line_height=1.8,
        )

        assert result == new_prefs
        self.prefs_repo.save.assert_called_once()

    def test_update_preferences_multiple_fields(self):
        """Test: update multiple preferences at once."""
        existing_prefs = UserPreferences(
            id=uuid4(),
            user_id=self.user_id,
            is_dark_mode=False,
            language="en",
            notifications_enabled=True,
            font_size="medium",
            reading_line_height=1.6,
        )
        
        updated_prefs = UserPreferences(
            id=existing_prefs.id,
            user_id=self.user_id,
            is_dark_mode=True,
            language="fr",
            notifications_enabled=False,
            font_size="medium",
            reading_line_height=1.6,
        )
        
        self.prefs_repo.get_for_user.return_value = existing_prefs
        self.prefs_repo.save.return_value = updated_prefs

        result = self.service.update_preferences(
            self.user_id,
            is_dark_mode=True,
            language="fr",
            notifications_enabled=False,
        )

        assert result == updated_prefs
        assert result.is_dark_mode is True
        assert result.language == "fr"
        assert result.notifications_enabled is False
