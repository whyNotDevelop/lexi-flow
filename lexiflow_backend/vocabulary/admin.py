from django.contrib import admin
from .infrastructure.models import VocabularyEntry

@admin.register(VocabularyEntry)
class VocabularyEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'word', 'saved_at', 'review_count')
    list_filter = ('saved_at', 'review_count')
    search_fields = ('user__email', 'word__text', 'meaning')
    readonly_fields = ('id', 'saved_at')
    raw_id_fields = ('user', 'word')