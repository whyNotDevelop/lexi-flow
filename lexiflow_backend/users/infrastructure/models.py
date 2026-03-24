import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class UserModel(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.
    Uses email as the unique identifier instead of username.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    avatar_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Django still requires a username field

    def __str__(self):
        return self.email


class UserPreferencesModel(models.Model):
    """
    User preferences model, linked one‑to‑one to the user.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='preferences')
    is_dark_mode = models.BooleanField(default=False)
    language = models.CharField(max_length=10, default='en')
    notifications_enabled = models.BooleanField(default=True)
    font_size = models.CharField(max_length=20, default='medium')
    reading_line_height = models.FloatField(default=1.6)