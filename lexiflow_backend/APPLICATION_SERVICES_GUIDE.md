"""
Application Services Implementation Guide
=========================================

This document describes the implemented Application Services layer for LexiFlow backend.
All services follow Clean Architecture principles and SOLID design.

Overview
--------
The Application Services layer contains business logic that orchestrates:
- Domain entities (pure Python dataclasses)
- Repository interfaces (for data access)
- External providers (for API calls)

Services depend only on interfaces, never on concrete implementations, enabling:
- Testability (easy to mock dependencies)
- Loose coupling (swappable implementations)
- Maintainability (isolated business logic)


Services Implemented
====================

1. LookupService (words/application/services/lookup_service.py)
   Purpose: Handles word lookups with cache → DB → external API fallback
   
   Methods:
   - lookup_word(word_text, user_id, language='en') -> Optional[Word]
     * Check repository (Redis cache + DB)
     * Fetch from external API if not found
     * Save to DB and record in history
   
   Dependencies: WordRepository, DictionaryProvider, HistoryRepository
   
   Example usage:
   ```python
   from words.application.services.lookup_service import LookupService
   from words.infrastructure.repositories.word_repository_impl import WordRepositoryImpl
   from words.infrastructure.providers.free_dictionary_provider import FreeDictionaryProvider
   from history.infrastructure.repositories.history_repository_impl import HistoryRepositoryImpl
   
   word_repo = WordRepositoryImpl()
   dict_provider = FreeDictionaryProvider()
   history_repo = HistoryRepositoryImpl()
   
   lookup_service = LookupService(word_repo, dict_provider, history_repo)
   word = lookup_service.lookup_word("serendipity", user_id)
   ```

2. VocabularyService (vocabulary/application/services/vocabulary_service.py)
   Purpose: Manages user's saved vocabulary (save, remove, search)
   
   Methods:
   - save_word(user_id, word_id) -> Optional[VocabularyEntry]
     * Check for duplicates
     * Retrieve word definition for display
     * Save to vocabulary
   
   - remove_word(user_id, word_id) -> bool
     * Remove from vocabulary
   
   - get_user_vocabulary(user_id) -> List[VocabularyEntry]
     * Retrieve all saved words
   
   - search_vocabulary(user_id, query) -> List[VocabularyEntry]
     * Search by word text
   
   - is_word_saved(user_id, word_id) -> bool
     * Check if word is in vocabulary
   
   Dependencies: VocabularyRepository, WordRepository
   
   Example usage:
   ```python
   from vocabulary.application.services.vocabulary_service import VocabularyService
   from vocabulary.infrastructure.repositories.vocabulary_repository_impl import VocabularyRepositoryImpl
   from words.infrastructure.repositories.word_repository_impl import WordRepositoryImpl
   
   vocab_repo = VocabularyRepositoryImpl()
   word_repo = WordRepositoryImpl()
   
   vocab_service = VocabularyService(vocab_repo, word_repo)
   entry = vocab_service.save_word(user_id, word_id)
   results = vocab_service.search_vocabulary(user_id, "brain")
   ```

3. HistoryService (history/application/services/history_service.py)
   Purpose: Records and retrieves word lookup history
   
   Methods:
   - record_lookup(user_id, word_id) -> LookupHistory
     * Record a new lookup
   
   - get_user_history(user_id, limit=50, before=None) -> List[LookupHistory]
     * Retrieve paginated history
   
   - delete_lookup(history_id) -> None
     * Delete single entry
   
   - clear_user_history(user_id) -> int
     * Clear all entries for user (returns count)
   
   - get_lookup_count(user_id) -> int
     * Total lookups for user
   
   - get_looklup_count_since(user_id, since: datetime) -> int
     * Lookups since specific time (typo in method name should be fixed)
   
   Dependencies: HistoryRepository
   
   Example usage:
   ```python
   from history.application.services.history_service import HistoryService
   from history.infrastructure.repositories.history_repository_impl import HistoryRepositoryImpl
   from datetime import datetime, timedelta
   
   history_repo = HistoryRepositoryImpl()
   history_service = HistoryService(history_repo)
   
   # Record lookup
   entry = history_service.record_lookup(user_id, word_id)
   
   # Get history
   recent_lookups = history_service.get_user_history(user_id)
   
   # Get today's lookups
   today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
   today_count = history_service.get_looklup_count_since(user_id, today_start)
   ```

4. AnalyticsService (analytics/application/services/analytics_service.py)
   Purpose: Aggregates reading sessions and lookup statistics
   
   Methods:
   - get_user_stats(user_id) -> Dict[str, Any]
     * Comprehensive analytics (reading + lookups)
     * Returns: total_sessions, active_sessions, reading_time_seconds,
               average_session_duration_seconds, total_words_looked_up,
               lookups_total, lookups_today, lookups_last_7_days, lookups_last_30_days
   
   - get_reading_session_stats(user_id) -> Dict[str, Any]
     * Reading only statistics
   
   - get_lookup_stats(user_id) -> Dict[str, int]
     * Lookup only statistics
   
   Dependencies: ReadingSessionRepository, HistoryRepository
   
   Example usage:
   ```python
   from analytics.application.services.analytics_service import AnalyticsService
   from analytics.infrastructure.repositories.reading_session_repository_impl import ReadingSessionRepositoryImpl
   from history.infrastructure.repositories.history_repository_impl import HistoryRepositoryImpl
   
   reading_repo = ReadingSessionRepositoryImpl()
   history_repo = HistoryRepositoryImpl()
   
   analytics_service = AnalyticsService(reading_repo, history_repo)
   stats = analytics_service.get_user_stats(user_id)
   ```

5. AuthService (users/application/services/auth_service.py)
   Purpose: User registration, profile updates, and preferences management
   
   Methods:
   - register_user(email, password, full_name=None) -> Optional[User]
     * Create new user
     * Initialize default preferences
   
   - get_user(user_id) -> Optional[User]
     * Retrieve user by ID
   
   - get_user_by_email(email) -> Optional[User]
     * Retrieve user by email
   
   - update_profile(user_id, full_name=None, avatar_url=None) -> Optional[User]
     * Update name or avatar
   
   - get_preferences(user_id) -> Optional[UserPreferences]
     * Retrieve preferences
   
   - update_preferences(user_id, **kwargs) -> Optional[UserPreferences]
     * Update any preference field
     * Supported: is_dark_mode, language, notifications_enabled, font_size, reading_line_height
   
   Dependencies: UserRepository, PreferencesRepository
   
   Example usage:
   ```python
   from users.application.services.auth_service import AuthService
   from users.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
   from users.infrastructure.repositories.preferences_repository_impl import PreferencesRepositoryImpl
   
   user_repo = UserRepositoryImpl()
   prefs_repo = PreferencesRepositoryImpl()
   
   auth_service = AuthService(user_repo, prefs_repo)
   
   # Register
   user = auth_service.register_user("john@example.com", "secret123", "John Doe")
   
   # Update preferences
   prefs = auth_service.update_preferences(user.id, is_dark_mode=True, language="es")
   ```


External Providers Implemented
==============================

FreeDictionaryProvider (words/infrastructure/providers/free_dictionary_provider.py)
   Purpose: Fetch word definitions from the Free Dictionary API
   
   API Endpoint: https://api.dictionaryapi.dev/api/v2/entries/{language}/{word}
   
   Methods:
   - fetch_word(word: str, language: str = 'en') -> Optional[Word]
     * Fetches fully populated Word with definitions
     * Returns None if not found or on error
   
   Features:
   - Handles network errors gracefully
   - Maps API responses to domain entities
   - Extracts IPA phonetics, audio URLs, definitions, synonyms
   
   Dependencies: None (external HTTP client)
   
   Example usage:
   ```python
   from words.infrastructure.providers.free_dictionary_provider import FreeDictionaryProvider
   
   provider = FreeDictionaryProvider()
   word = provider.fetch_word("ephemeral", "en")
   if word:
       print(f"Found: {word.text}")
       for defn in word.definitions:
           print(f"  - {defn.meaning}")
   ```


Testing
=======

All services include comprehensive unit test suites using pytest and mocks:

- words/tests/test_application/test_lookup_service.py (9 tests)
- vocabulary/tests/test_application/test_vocabulary_service.py (12 tests)
- history/tests/test_application/test_history_service.py (12 tests)
- analytics/tests/test_application/test_analytics_service.py (8 tests)
- users/tests/test_application/test_auth_service.py (17 tests)
- words/tests/test_infrastructure/test_free_dictionary_provider.py (13 tests)

Run tests:
```bash
pytest words/tests/test_application/ -v
pytest vocabulary/tests/test_application/ -v
pytest history/tests/test_application/ -v
pytest analytics/tests/test_application/ -v
pytest users/tests/test_application/ -v
pytest words/tests/test_infrastructure/ -v

# Run all tests
pytest -v
```


Architectural Decisions
=======================

1. Dependency Injection
   - Services receive dependencies via constructor
   - Enables easy testing with mocks
   - Follows Dependency Inversion Principle

2. Domain Entities Only
   - Services work with domain entities (Word, User, etc.)
   - Never expose Django models
   - Enables framework independence

3. Repository Pattern
   - All data access goes through repositories
   - Services never import models or query ORM directly
   - Centralizes data access logic

4. Provider Pattern
   - External APIs wrapped behind interfaces
   - Multiple providers can be swapped
   - Services depend on interface, not implementation

5. Error Handling
   - Services return None or raise domain exceptions
   - Infrastructure errors (DB, network) handled gracefully
   - No framework-specific exceptions leaked

6. No Framework Coupling
   - Services are pure Python
   - No Django imports (except types)
   - Can be reused in different contexts


File Structure
==============

words/
  application/
    services/
      __init__.py
      lookup_service.py
  infrastructure/
    providers/
      __init__.py
      free_dictionary_provider.py
  tests/
    test_application/
      __init__.py
      test_lookup_service.py
    test_infrastructure/
      __init__.py
      test_free_dictionary_provider.py

vocabulary/
  application/
    services/
      __init__.py
      vocabulary_service.py
  tests/
    test_application/
      __init__.py
      test_vocabulary_service.py

history/
  application/
    services/
      __init__.py
      history_service.py
  tests/
    test_application/
      __init__.py
      test_history_service.py

analytics/
  application/
    services/
      __init__.py
      analytics_service.py
  tests/
    test_application/
      __init__.py
      test_analytics_service.py

users/
  application/
    services/
      __init__.py
      auth_service.py
  tests/
    test_application/
      __init__.py
      test_auth_service.py


Next Steps
==========

1. REVIEW: Code review by team and architect
2. TESTING: Run full test suite to ensure all passes
3. INTEGRATION: Wire services into DRF views (Presentation layer)
4. API ENDPOINTS: Create ViewSet and Serializers
5. DOCUMENTATION: Add API docs and usage examples

Known Issues
============

1. HistoryService.get_looklup_count_since() has typo in method name
   - Should be: get_lookup_count_since()
   - Will need refactor after review

2. FreeDictionaryProvider error handling uses print()
   - Should use proper logging in production

3. Services don't include retry logic for external API calls
   - Consider adding retry mechanism for prod (e.g., exponential backoff)


Dependencies
============

Required packages (already in requirements.txt):
- requests (for FreeDictionaryProvider)
- pytest
- pytest-django
- mock (part of unittest)
"""
