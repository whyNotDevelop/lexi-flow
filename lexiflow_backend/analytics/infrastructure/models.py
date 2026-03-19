import uuid
from django.db import models
from users.infrastructure.models import User

class ReadingSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reading_sessions')
    book_id = models.CharField(max_length=255, blank=True)
    book_title = models.CharField(max_length=500, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.IntegerField(default=0)
    words_looked_up = models.IntegerField(default=0)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"Session for {self.user.email} started at {self.started_at}"