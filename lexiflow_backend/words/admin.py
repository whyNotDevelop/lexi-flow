from django.contrib import admin
from .infrastructure.models import Word, Definition

class DefinitionInline(admin.TabularInline):
    model = Definition
    extra = 0
    fields = ('part_of_speech', 'meaning', 'example', 'order')
    ordering = ('order',)

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('text', 'language', 'phonetic', 'created_at')
    list_filter = ('language', 'created_at')
    search_fields = ('text',)
    readonly_fields = ('id', 'created_at')
    inlines = [DefinitionInline]


@admin.register(Definition)
class DefinitionAdmin(admin.ModelAdmin):
    list_display = ('word', 'part_of_speech', 'meaning_preview', 'order')
    list_filter = ('part_of_speech',)
    search_fields = ('word__text', 'meaning')
    readonly_fields = ('id',)

    def meaning_preview(self, obj):
        return obj.meaning[:50] + '…' if len(obj.meaning) > 50 else obj.meaning
    meaning_preview.short_description = 'Meaning'