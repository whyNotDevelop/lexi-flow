# users/infrastructure/repositories/preferences_repository_impl.py
from typing import Optional
from uuid import UUID
from ...domain.entities import UserPreferences
from ...domain.interfaces import PreferencesRepository
from ..models import UserPreferencesModel

class PreferencesRepositoryImpl(PreferencesRepository):
    def get_for_user(self, user_id: UUID) -> Optional[UserPreferences]:
        try:
            model = UserPreferencesModel.objects.get(user_id=user_id)
            return UserPreferences(
                id=model.id,
                user_id=model.user_id,
                is_dark_mode=model.is_dark_mode,
                language=model.language,
                notifications_enabled=model.notifications_enabled,
                font_size=model.font_size,
                reading_line_height=model.reading_line_height,
            )
        except UserPreferencesModel.DoesNotExist:
            return None

    def save(self, preferences: UserPreferences) -> UserPreferences:
        model, _ = UserPreferencesModel.objects.update_or_create(
            user_id=preferences.user_id,
            defaults={
                'is_dark_mode': preferences.is_dark_mode,
                'language': preferences.language,
                'notifications_enabled': preferences.notifications_enabled,
                'font_size': preferences.font_size,
                'reading_line_height': preferences.reading_line_height,
            }
        )
        preferences.id = model.id
        return preferences