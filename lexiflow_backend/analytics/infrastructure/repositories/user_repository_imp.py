"""
Concrete implementation of UserRepository using Django ORM.
"""
from typing import Optional
from uuid import UUID
from django.contrib.auth.hashers import make_password
from ...domain.entities import User
from ...domain.interfaces import UserRepository
from ..models import UserModel

class UserRepositoryImpl(UserRepository):
    """
    Implements user persistence using Django's built-in User model (customized).
    """

    def _to_entity(self, model: UserModel) -> User:
        """Convert Django ORM model to domain entity."""
        return User(
            id=model.id,
            email=model.email,
            full_name=model.full_name,
            avatar_url=model.avatar_url,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        try:
            model = UserModel.objects.get(id=user_id)
            return self._to_entity(model)
        except UserModel.DoesNotExist:
            return None

    def get_by_email(self, email: str) -> Optional[User]:
        try:
            model = UserModel.objects.get(email=email)
            return self._to_entity(model)
        except UserModel.DoesNotExist:
            return None

    def create(self, email: str, password: str, full_name: Optional[str] = None) -> User:
        """
        Create a new user. The password is hashed using Django's make_password.
        Note: Django's AbstractUser requires a username; we set it equal to email.
        """
        model = UserModel.objects.create(
            email=email,
            password=make_password(password),
            full_name=full_name or "",
            username=email,  # required by Django's User model
        )
        return self._to_entity(model)

    def update(self, user: User) -> User:
        model = UserModel.objects.get(id=user.id)
        model.full_name = user.full_name
        model.avatar_url = user.avatar_url
        model.save()
        return self._to_entity(model)