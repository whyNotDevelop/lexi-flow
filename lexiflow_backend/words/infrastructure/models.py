import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField

class WordModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=255, db_index=True)
    language = models.CharField(max_length=10, default='en')
    phonetic = models.CharField(max_length=255, blank=True)
    audio_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('text', 'language')

    def __str__(self):
        return self.text


class DefinitionModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    word = models.ForeignKey(WordModel, on_delete=models.CASCADE, related_name='definitions')
    part_of_speech = models.CharField(max_length=50)
    meaning = models.TextField()
    example = models.TextField(blank=True)
    synonyms = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.word.text} - {self.part_of_speech}"