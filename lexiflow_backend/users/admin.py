from django.contrib import admin
from .infrastructure.models import UserModel, UserPreferencesModel

@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'is_active', 'created_at')
    list_filter = ('is_active', 'is_staff', 'created_at')
    search_fields = ('email', 'full_name')
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('id', 'email', 'full_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    ordering = ('email',)


@admin.register(UserPreferencesModel)
class UserPreferencesAdmin(admin.ModelAdmin):
    list_display = ('user', 'language', 'is_dark_mode', 'notifications_enabled')
    list_filter = ('language', 'is_dark_mode', 'notifications_enabled')
    search_fields = ('user__email', 'user__full_name')
    readonly_fields = ('id',)