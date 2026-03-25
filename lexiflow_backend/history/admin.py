from django.contrib import admin
from .infrastructure.models import LookupHistoryModel

@admin.register(LookupHistoryModel)
class LookupHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'word', 'looked_up_at')
    list_filter = ('looked_up_at',)
    search_fields = ('user__email', 'word__text')
    readonly_fields = ('id', 'looked_up_at')
    raw_id_fields = ('user', 'word')
    date_hierarchy = 'looked_up_at'