from django.contrib import admin
from .infrastructure.models import ReadingSessionModel

@admin.register(ReadingSessionModel)
class ReadingSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'book_title', 'started_at', 'duration_seconds', 'words_looked_up')
    list_filter = ('started_at',)
    search_fields = ('user__email', 'book_title', 'book_id')
    readonly_fields = ('id', 'started_at')
    raw_id_fields = ('user',)
    date_hierarchy = 'started_at'