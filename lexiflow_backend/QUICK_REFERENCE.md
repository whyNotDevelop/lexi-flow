# Quick Reference: Service Instantiation & Usage

## 1. LookupService

### Import
```python
from words.application.services.lookup_service import LookupService
from words.infrastructure.repositories.word_repository_impl import WordRepositoryImpl
from words.infrastructure.providers.free_dictionary_provider import FreeDictionaryProvider
from history.infrastructure.repositories.history_repository_impl import HistoryRepositoryImpl
```

### Instantiate
```python
lookup_service = LookupService(
    word_repo=WordRepositoryImpl(),
    dict_provider=FreeDictionaryProvider(),
    history_repo=HistoryRepositoryImpl()
)
```

### Usage
```python
from uuid import UUID

user_id = UUID("550e8400-e29b-41d4-a716-446655440000")

# Look up a word
word = lookup_service.lookup_word("serendipity", user_id, "en")

if word:
    print(f"Word: {word.text}")
    print(f"Phonetic: {word.phonetic}")
    for definition in word.definitions:
        print(f"- {definition.meaning}")
else:
    print("Word not found")
```

---

## 2. VocabularyService

### Import
```python
from vocabulary.application.services.vocabulary_service import VocabularyService
from vocabulary.infrastructure.repositories.vocabulary_repository_impl import VocabularyRepositoryImpl
from words.infrastructure.repositories.word_repository_impl import WordRepositoryImpl
```

### Instantiate
```python
vocab_service = VocabularyService(
    vocab_repo=VocabularyRepositoryImpl(),
    word_repo=WordRepositoryImpl()
)
```

### Usage
```python
# Save a word
entry = vocab_service.save_word(user_id, word_id)
if entry:
    print(f"Saved: {entry.meaning}")

# Check if saved
is_saved = vocab_service.is_word_saved(user_id, word_id)
print(f"Saved: {is_saved}")

# Get all vocabulary
entries = vocab_service.get_user_vocabulary(user_id)
for entry in entries:
    print(f"- {entry.meaning}")

# Search vocabulary
results = vocab_service.search_vocabulary(user_id, "brain")
for result in results:
    print(f"Found: {result.meaning}")

# Remove from vocabulary
removed = vocab_service.remove_word(user_id, word_id)
print(f"Removed: {removed}")
```

---

## 3. HistoryService

### Import
```python
from history.application.services.history_service import HistoryService
from history.infrastructure.repositories.history_repository_impl import HistoryRepositoryImpl
from datetime import datetime, timedelta
```

### Instantiate
```python
history_service = HistoryService(
    history_repo=HistoryRepositoryImpl()
)
```

### Usage
```python
# Record a lookup
history_entry = history_service.record_lookup(user_id, word_id)
print(f"Recorded at: {history_entry.looked_up_at}")

# Get recent history
recent = history_service.get_user_history(user_id, limit=20)
for entry in recent:
    print(f"Looked up {entry.word_id} at {entry.looked_up_at}")

# Get history before a date
before = datetime.now() - timedelta(days=7)
old_history = history_service.get_user_history(user_id, before=before)

# Get statistics
total_lookups = history_service.get_lookup_count(user_id)
print(f"Total lookups: {total_lookups}")

# Count since a time
today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
today_lookups = history_service.get_looklup_count_since(user_id, today_start)
print(f"Lookups today: {today_lookups}")

# Clear history
count_deleted = history_service.clear_user_history(user_id)
print(f"Deleted {count_deleted} entries")

# Delete single entry
history_service.delete_lookup(history_id)
```

---

## 4. AnalyticsService

### Import
```python
from analytics.application.services.analytics_service import AnalyticsService
from analytics.infrastructure.repositories.reading_session_repository_impl import ReadingSessionRepositoryImpl
from history.infrastructure.repositories.history_repository_impl import HistoryRepositoryImpl
```

### Instantiate
```python
analytics_service = AnalyticsService(
    reading_session_repo=ReadingSessionRepositoryImpl(),
    history_repo=HistoryRepositoryImpl()
)
```

### Usage
```python
# Get comprehensive stats
stats = analytics_service.get_user_stats(user_id)
print(f"Total sessions: {stats['total_sessions']}")
print(f"Reading time: {stats['reading_time_seconds']} seconds")
print(f"Lookups today: {stats['lookups_today']}")
print(f"Lookups this week: {stats['lookups_last_7_days']}")

# Get reading-only stats
reading_stats = analytics_service.get_reading_session_stats(user_id)
print(f"Active sessions: {reading_stats['active_sessions']}")

# Get lookup-only stats
lookup_stats = analytics_service.get_lookup_stats(user_id)
print(f"Total lookups: {lookup_stats['lookups_total']}")
```

---

## 5. AuthService

### Import
```python
from users.application.services.auth_service import AuthService
from users.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from users.infrastructure.repositories.preferences_repository_impl import PreferencesRepositoryImpl
```

### Instantiate
```python
auth_service = AuthService(
    user_repo=UserRepositoryImpl(),
    prefs_repo=PreferencesRepositoryImpl()
)
```

### Usage
```python
# Register a user
user = auth_service.register_user(
    email="john@example.com",
    password="secret123",
    full_name="John Doe"
)
if user:
    print(f"User created: {user.id}")

# Get user
user = auth_service.get_user(user_id)
print(f"User: {user.email}")

# Get by email
user = auth_service.get_user_by_email("john@example.com")

# Update profile
user = auth_service.update_profile(
    user_id,
    full_name="Jane Doe",
    avatar_url="https://example.com/avatar.jpg"
)

# Get preferences
prefs = auth_service.get_preferences(user_id)
print(f"Dark mode: {prefs.is_dark_mode}")
print(f"Language: {prefs.language}")

# Update single preference
prefs = auth_service.update_preferences(user_id, is_dark_mode=True)

# Update multiple preferences
prefs = auth_service.update_preferences(
    user_id,
    is_dark_mode=True,
    language="es",
    font_size="large",
    notifications_enabled=False
)
```

---

## 6. FreeDictionaryProvider

### Import
```python
from words.infrastructure.providers.free_dictionary_provider import FreeDictionaryProvider
```

### Instantiate
```python
dict_provider = FreeDictionaryProvider()
```

### Usage
```python
# Fetch a word
word = dict_provider.fetch_word("ephemeral", "en")

if word:
    print(f"Word: {word.text}")
    print(f"Phonetic: {word.phonetic}")
    print(f"Audio: {word.audio_url}")
    
    for definition in word.definitions:
        print(f"\n{definition.part_of_speech}")
        print(f"- {definition.meaning}")
        if definition.example:
            print(f"  Example: {definition.example}")
        if definition.synonyms:
            print(f"  Synonyms: {', '.join(definition.synonyms)}")
else:
    print("Not found")
```

---

## Using Services in Django REST Framework

### Create a Container (Recommended)

```python
# lexiflow_backend/container.py

from words.application.services.lookup_service import LookupService
from words.infrastructure.repositories.word_repository_impl import WordRepositoryImpl
from words.infrastructure.providers.free_dictionary_provider import FreeDictionaryProvider
from vocabulary.application.services.vocabulary_service import VocabularyService
from vocabulary.infrastructure.repositories.vocabulary_repository_impl import VocabularyRepositoryImpl
from history.application.services.history_service import HistoryService
from history.infrastructure.repositories.history_repository_impl import HistoryRepositoryImpl
from analytics.application.services.analytics_service import AnalyticsService
from analytics.infrastructure.repositories.reading_session_repository_impl import ReadingSessionRepositoryImpl
from users.application.services.auth_service import AuthService
from users.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from users.infrastructure.repositories.preferences_repository_impl import PreferencesRepositoryImpl


class ServiceContainer:
    def __init__(self):
        # Initialize repositories once
        self.word_repo = WordRepositoryImpl()
        self.vocab_repo = VocabularyRepositoryImpl()
        self.history_repo = HistoryRepositoryImpl()
        self.reading_session_repo = ReadingSessionRepositoryImpl()
        self.user_repo = UserRepositoryImpl()
        self.prefs_repo = PreferencesRepositoryImpl()
        
        # Initialize providers
        self.dict_provider = FreeDictionaryProvider()
    
    def get_lookup_service(self):
        return LookupService(self.word_repo, self.dict_provider, self.history_repo)
    
    def get_vocabulary_service(self):
        return VocabularyService(self.vocab_repo, self.word_repo)
    
    def get_history_service(self):
        return HistoryService(self.history_repo)
    
    def get_analytics_service(self):
        return AnalyticsService(self.reading_session_repo, self.history_repo)
    
    def get_auth_service(self):
        return AuthService(self.user_repo, self.prefs_repo)


# Global container
container = ServiceContainer()
```

### Use in ViewSet

```python
# words/presentation/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from lexiflow_backend.container import container

class WordViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def lookup(self, request):
        service = container.get_lookup_service()
        
        word = service.lookup_word(
            request.data['word'],
            request.user.id,
            request.data.get('language', 'en')
        )
        
        if not word:
            return Response(
                {'error': 'Word not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response({
            'id': str(word.id),
            'text': word.text,
            'phonetic': word.phonetic,
            'definitions': [
                {
                    'meaning': d.meaning,
                    'part_of_speech': d.part_of_speech,
                    'example': d.example,
                    'synonyms': d.synonyms
                }
                for d in word.definitions
            ]
        })
```

---

## Testing Services

### Test Template

```python
# words/tests/test_application/test_lookup_service.py

import pytest
from unittest.mock import Mock
from uuid import uuid4
from words.application.services.lookup_service import LookupService
from words.domain.entities import Word

@pytest.mark.django_db
def test_lookup_word():
    # Mock dependencies
    word_repo = Mock()
    dict_provider = Mock()
    history_repo = Mock()
    
    # Create service
    service = LookupService(word_repo, dict_provider, history_repo)
    
    # Set up mock behavior
    word = Word(id=uuid4(), text="test", language="en", ...)
    word_repo.find_by_text.return_value = word
    
    # Test
    result = service.lookup_word("test", uuid4())
    
    # Assert
    assert result == word
    assert word_repo.find_by_text.called
```

---

## Common Patterns

### Pattern 1: Check Then Create
```python
# Check if exists, create if needed
entry = vocab_service.save_word(user_id, word_id)
if entry:
    print("Word saved or already in vocabulary")
else:
    print("Word not found")
```

### Pattern 2: Search Then Act
```python
# Search for items, then operate on them
results = vocab_service.search_vocabulary(user_id, "brain")
for result in results:
    # Do something with result
    pass
```

### Pattern 3: Get Stats for Dashboard
```python
# Aggregate stats from multiple sources
stats = analytics_service.get_user_stats(user_id)

dashboard_data = {
    'reading': stats['total_sessions'],
    'lookups': stats['lookups_total'],
    'today': stats['lookups_today'],
}
```

### Pattern 4: Error Handling
```python
# Services return None on failure
word = lookup_service.lookup_word("test", user_id)
if word is None:
    # Handle error
    return Response({'error': 'Not found'}, status=404)
```

---

## Checklist for Using Services

- [ ] Import service class
- [ ] Import concrete repository/provider implementations
- [ ] Instantiate with dependencies via constructor
- [ ] Call service method with required parameters
- [ ] Check for None return (indicates error)
- [ ] Use returned domain entities (not Django models)
- [ ] Let repository handle all persistence
- [ ] Never call ORM directly from view

---

## Performance Tips

1. **Use repository caching** - WordRepository already uses Redis
2. **Limit pagination** - Use `limit` parameter in history/search
3. **Time-bound queries** - Use `before` and time ranges for analytics
4. **Batch operations** - Process multiple items in loops
5. **Async tasks** - For long operations, consider Celery

---

**Version**: 1.0  
**Last Updated**: March 2026  
**Status**: Complete and reviewed
