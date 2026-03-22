"""
Unit tests for UserRepositoryImpl.
"""
import pytest
from django.contrib.auth.hashers import check_password
from users.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from users.infrastructure.models import UserModel

@pytest.mark.django_db
class TestUserRepository:
    """Test suite for user repository."""

    def test_create_user(self):
        """Creating a user should store it in the database."""
        repo = UserRepositoryImpl()
        user = repo.create(email="test@example.com", password="secret", full_name="Test User")

        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.full_name == "Test User"

        # Verify the password was hashed correctly
        db_user = UserModel.objects.get(id=user.id)
        assert check_password("secret", db_user.password)

    def test_get_by_email_found(self):
        """Retrieve existing user by email."""
        repo = UserRepositoryImpl()
        created = repo.create(email="findme@example.com", password="pass")
        found = repo.get_by_email("findme@example.com")
        assert found is not None
        assert found.id == created.id

    def test_get_by_email_not_found(self):
        """Return None when user does not exist."""
        repo = UserRepositoryImpl()
        found = repo.get_by_email("nonexistent@example.com")
        assert found is None

    def test_update_user(self):
        """Updating a user should modify the stored fields."""
        repo = UserRepositoryImpl()
        user = repo.create(email="update@example.com", password="pass", full_name="Old Name")
        user.full_name = "New Name"
        updated = repo.update(user)

        assert updated.full_name == "New Name"
        db_user = UserModel.objects.get(id=user.id)
        assert db_user.full_name == "New Name"