"""
Service Integration Guide for Django REST Framework Views
==========================================================

This guide explains how to integrate the Application Services into
Django REST Framework views and viewsets (Presentation layer).


Service Instantiation Patterns
==============================

Option 1: Direct Instantiation in Views (Simple)
-------------------------------------------------

```python
# words/presentation/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from words.application.services.lookup_service import LookupService
from words.infrastructure.repositories.word_repository_impl import WordRepositoryImpl
from words.infrastructure.providers.free_dictionary_provider import FreeDictionaryProvider
from history.infrastructure.repositories.history_repository_impl import HistoryRepositoryImpl

class WordViewSet(viewsets.ViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize service with dependencies
        self.lookup_service = LookupService(
            WordRepositoryImpl(),
            FreeDictionaryProvider(),
            HistoryRepositoryImpl()
        )

    @action(detail=False, methods=['post'])
    def lookup(self, request):
        word_text = request.data.get('word')
        language = request.data.get('language', 'en')
        
        word = self.lookup_service.lookup_word(
            word_text, 
            request.user.id,
            language
        )
        
        if not word:
            return Response({'detail': 'Word not found'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            'id': str(word.id),
            'text': word.text,
            'phonetic': word.phonetic,
            'definitions': [
                {
                    'meaning': d.meaning,
                    'part_of_speech': d.part_of_speech,
                    'example': d.example,
                }
                for d in word.definitions
            ]
        })
```

Option 2: Dependency Injection Container (Recommended for larger apps)
-----------------------------------------------------------------------

```python
# lexiflow_backend/container.py

from words.application.services.lookup_service import LookupService
from words.infrastructure.repositories.word_repository_impl import WordRepositoryImpl
from words.infrastructure.providers.free_dictionary_provider import FreeDictionaryProvider
from history.infrastructure.repositories.history_repository_impl import HistoryRepositoryImpl
from vocabulary.application.services.vocabulary_service import VocabularyService
from vocabulary.infrastructure.repositories.vocabulary_repository_impl import VocabularyRepositoryImpl
from history.application.services.history_service import HistoryService
from analytics.application.services.analytics_service import AnalyticsService
from analytics.infrastructure.repositories.reading_session_repository_impl import ReadingSessionRepositoryImpl
from users.application.services.auth_service import AuthService
from users.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from users.infrastructure.repositories.preferences_repository_impl import PreferencesRepositoryImpl


class ServiceContainer:
    \"\"\"Central place to instantiate all services\"\"\"
    
    def __init__(self):
        # Initialize repositories
        self.word_repo = WordRepositoryImpl()
        self.vocab_repo = VocabularyRepositoryImpl()
        self.history_repo = HistoryRepositoryImpl()
        self.reading_session_repo = ReadingSessionRepositoryImpl()
        self.user_repo = UserRepositoryImpl()
        self.prefs_repo = PreferencesRepositoryImpl()
        
        # Initialize providers
        self.dict_provider = FreeDictionaryProvider()
    
    def get_lookup_service(self) -> LookupService:
        return LookupService(self.word_repo, self.dict_provider, self.history_repo)
    
    def get_vocabulary_service(self) -> VocabularyService:
        return VocabularyService(self.vocab_repo, self.word_repo)
    
    def get_history_service(self) -> HistoryService:
        return HistoryService(self.history_repo)
    
    def get_analytics_service(self) -> AnalyticsService:
        return AnalyticsService(self.reading_session_repo, self.history_repo)
    
    def get_auth_service(self) -> AuthService:
        return AuthService(self.user_repo, self.prefs_repo)


# Global container instance
container = ServiceContainer()
```

Then in views:

```python
# words/presentation/views.py

from lexiflow_backend.container import container
from rest_framework import viewsets, status
from rest_framework.response import Response

class WordViewSet(viewsets.ViewSet):
    def lookup_word(self, request):
        lookup_service = container.get_lookup_service()
        word = lookup_service.lookup_word(
            request.data['word'],
            request.user.id,
            request.data.get('language', 'en')
        )
        
        if not word:
            return Response({'detail': 'Not found'}, status=404)
        
        return Response(serialize_word(word))
```

Option 3: Using pytest-django Fixtures (For Testing)
-----------------------------------------------------

```python
# conftest.py (in tests root)

import pytest
from unittest.mock import Mock
from lexiflow_backend.container import ServiceContainer

@pytest.fixture
def service_container():
    \"\"\"Provide service container for tests\"\"\"
    return ServiceContainer()

@pytest.fixture
def lookup_service(service_container):
    return service_container.get_lookup_service()

# Usage in tests:
def test_word_lookup(lookup_service):
    word = lookup_service.lookup_word("test", uuid4())
    assert word is not None
```


Example View Implementations
============================

1. LookupService in WordViewSet
---------------------------------

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from words.application.services.lookup_service import LookupService
from lexiflow_backend.container import container

class WordViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def lookup(self, request):
        \"\"\"Look up a word and record history\"\"\"
        service = container.get_lookup_service()
        
        word = service.lookup_word(
            request.data.get('word'),
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
            'audio_url': word.audio_url,
            'definitions': [
                {
                    'meaning': d.meaning,
                    'part_of_speech': d.part_of_speech,
                    'example': d.example,
                    'synonyms': d.synonyms,
                }
                for d in word.definitions
            ]
        }, status=status.HTTP_200_OK)
```

2. VocabularyService in VocabularyViewSet
--------------------------------------------

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from vocabulary.application.services.vocabulary_service import VocabularyService
from lexiflow_backend.container import container

class VocabularyViewSet(viewsets.ViewSet):
    def list(self, request):
        \"\"\"Get user's saved vocabulary\"\"\"
        service = container.get_vocabulary_service()
        entries = service.get_user_vocabulary(request.user.id)
        
        return Response([
            {
                'id': str(e.id),
                'word_id': str(e.word_id),
                'meaning': e.meaning,
                'saved_at': e.saved_at.isoformat(),
                'review_count': e.review_count,
            }
            for e in entries
        ])
    
    @action(detail=False, methods=['post'])
    def add(self, request):
        \"\"\"Save a word to vocabulary\"\"\"
        service = container.get_vocabulary_service()
        
        entry = service.save_word(
            request.user.id,
            request.data.get('word_id')
        )
        
        if not entry:
            return Response(
                {'error': 'Word not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response({
            'id': str(entry.id),
            'saved': True
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['delete'])
    def remove(self, request):
        \"\"\"Remove word from vocabulary\"\"\"
        service = container.get_vocabulary_service()
        
        removed = service.remove_word(
            request.user.id,
            request.data.get('word_id')
        )
        
        if not removed:
            return Response(
                {'error': 'Word not in vocabulary'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        \"\"\"Search vocabulary\"\"\"
        service = container.get_vocabulary_service()
        query = request.query_params.get('q', '')
        
        entries = service.search_vocabulary(request.user.id, query)
        
        return Response([
            {
                'id': str(e.id),
                'word_id': str(e.word_id),
                'meaning': e.meaning,
            }
            for e in entries
        ])
```

3. AuthService in UserViewSet
------------------------------

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.application.services.auth_service import AuthService
from lexiflow_backend.container import container

class UserViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        \"\"\"Register a new user\"\"\"
        service = container.get_auth_service()
        
        user = service.register_user(
            request.data.get('email'),
            request.data.get('password'),
            request.data.get('full_name')
        )
        
        if not user:
            return Response(
                {'error': 'Registration failed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({
            'id': str(user.id),
            'email': user.email,
            'full_name': user.full_name,
            'created_at': user.created_at.isoformat(),
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        \"\"\"Get current user profile\"\"\"
        service = container.get_auth_service()
        user = service.get_user(request.user.id)
        prefs = service.get_preferences(request.user.id)
        
        return Response({
            'id': str(user.id),
            'email': user.email,
            'full_name': user.full_name,
            'avatar_url': user.avatar_url,
            'preferences': {
                'is_dark_mode': prefs.is_dark_mode,
                'language': prefs.language,
                'notifications_enabled': prefs.notifications_enabled,
                'font_size': prefs.font_size,
                'reading_line_height': prefs.reading_line_height,
            }
        })
    
    @action(detail=False, methods=['patch'], permission_classes=[IsAuthenticated])
    def update_preferences(self, request):
        \"\"\"Update user preferences\"\"\"
        service = container.get_auth_service()
        
        prefs = service.update_preferences(
            request.user.id,
            **request.data.get('preferences', {})
        )
        
        return Response({
            'is_dark_mode': prefs.is_dark_mode,
            'language': prefs.language,
            'notifications_enabled': prefs.notifications_enabled,
            'font_size': prefs.font_size,
            'reading_line_height': prefs.reading_line_height,
        })
```

4. AnalyticsService in AnalyticsViewSet
----------------------------------------

```python
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from analytics.application.services.analytics_service import AnalyticsService
from lexiflow_backend.container import container

class AnalyticsViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def user_stats(self, request):
        \"\"\"Get comprehensive user analytics\"\"\"
        service = container.get_analytics_service()
        stats = service.get_user_stats(request.user.id)
        
        return Response(stats)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def reading_stats(self, request):
        \"\"\"Get reading session statistics\"\"\"
        service = container.get_analytics_service()
        stats = service.get_reading_session_stats(request.user.id)
        
        return Response(stats)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def lookup_stats(self, request):
        \"\"\"Get lookup statistics\"\"\"
        service = container.get_analytics_service()
        stats = service.get_lookup_stats(request.user.id)
        
        return Response(stats)
```


Django URL Configuration
========================

```python
# lexiflow_backend/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from words.presentation.views import WordViewSet
from vocabulary.presentation.views import VocabularyViewSet
from history.presentation.views import HistoryViewSet
from analytics.presentation.views import AnalyticsViewSet
from users.presentation.views import UserViewSet

router = DefaultRouter()
router.register(r'words', WordViewSet, basename='word')
router.register(r'vocabulary', VocabularyViewSet, basename='vocabulary')
router.register(r'history', HistoryViewSet, basename='history')
router.register(r'analytics', AnalyticsViewSet, basename='analytics')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
```


Error Handling Best Practices
=============================

```python
# Always check for None returns
result = service.some_method()
if result is None:
    return Response({'error': 'Operation failed'}, status=status.HTTP_400_BAD_REQUEST)

# Catch service errors
try:
    result = service.some_method()
except Exception as e:
    # Log the error (use server logger)
    logger.error(f"Service error: {e}")
    return Response({'error': 'Internal error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Pass user context (never Django request objects)
service.some_operation(user_id=request.user.id)  # ✓ Good
service.some_operation(request=request)  # ✗ Bad
```


Testing Services in Views
==========================

```python
# words/tests/test_presentation/test_word_views.py

import pytest
from unittest.mock import Mock, patch
from rest_framework.test import APIRequestFactory
from rest_framework import status

@pytest.mark.django_db
def test_lookup_endpoint():
    factory = APIRequestFactory()
    request = factory.post('/api/words/lookup/', {'word': 'test'})
    request.user = Mock(id=uuid4())
    
    # Mock the service
    with patch('lexiflow_backend.container.container.get_lookup_service') as mock_service:
        mock_lookup_service = Mock()
        mock_lookup_service.lookup_word.return_value = Word(...)
        mock_service.return_value = mock_lookup_service
        
        view = WordViewSet.as_view({'post': 'lookup'})
        response = view(request)
        
        assert response.status_code == status.HTTP_200_OK
```


Running the Application
=======================

Once services are wired into views:

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Run tests
pytest -v

# Start development server
python manage.py runserver
```

API Endpoints will be available at:
- POST /api/words/lookup/
- GET /api/vocabulary/
- POST /api/vocabulary/add/
- GET /api/history/
- POST /api/users/register/
- GET /api/users/profile/
- GET /api/analytics/user_stats/
"""
