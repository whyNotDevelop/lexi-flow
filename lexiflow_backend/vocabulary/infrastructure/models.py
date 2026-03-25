import uuid
from django.db import models
from users.infrastructure.models import UserModel
from words.infrastructure.models import WordModel

class VocabularyEntryModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='vocabulary')
    word = models.ForeignKey(WordModel, on_delete=models.CASCADE)
    meaning = models.TextField()  # cached primary meaning
    saved_at = models.DateTimeField(auto_now_add=True)
    review_count = models.IntegerField(default=0)
    last_reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'word')
        ordering = ['-saved_at']

    def __str__(self):
        return f"{self.user.email} - {self.word.text}"