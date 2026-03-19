import uuid
from django.db import models
from users.infrastructure.models import User
from words.infrastructure.models import Word

class LookupHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lookup_history')
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    looked_up_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-looked_up_at']

    def __str__(self):
        return f"{self.user.email} - {self.word.text} at {self.looked_up_at}"