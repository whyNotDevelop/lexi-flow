import pytest
from unittest.mock import patch
from rest_framework import status
from datetime import datetime, timedelta
from django.utils import timezone

from words.infrastructure.models import WordModel
from history.infrastructure.models import LookupHistoryModel
from analytics.infrastructure.models import ReadingSessionModel

@pytest.mark.django_db
class TestAnalyticsFlow:
    """Integration tests for analytics endpoints."""

    def test_get_user_stats_success(self, authenticated_api_client, mock_dictionary_response):
        """Test retrieving comprehensive user statistics."""
        client, user = authenticated_api_client

        # Create a reading session
        session = ReadingSessionModel.objects.create(
            user=user,
            book_title="Test Book",
            started_at=timezone.now(),
            ended_at=timezone.now(),
            duration_seconds=120,
            words_looked_up=5
        )

        # Perform a lookup
        with patch('words.infrastructure.providers.free_dictionary_provider.requests.get') as mock_get:
            mock_get.return_value = mock_dictionary_response('statsword')
            client.get('/api/words/lookup/statsword/')

        response = client.get('/api/analytics/stats/')
        assert response.status_code == status.HTTP_200_OK
        data = response.data

        # Verify reading stats
        assert data['total_sessions'] == 1
        assert data['reading_time_seconds'] == 120
        assert data['total_words_looked_up'] == 5  # from session
        # Lookup stats may be separate; adjust based on your actual response shape
        # For now, just ensure keys exist
        assert 'lookups_total' in data

    def test_get_user_stats_zero_activity(self, authenticated_api_client):
        """Test stats when user has no activity."""
        client, user = authenticated_api_client

        response = client.get('/api/analytics/stats/')
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert data.get('total_sessions', 0) == 0
        assert data.get('lookups_total', 0) == 0

    def test_get_reading_session_stats(self, authenticated_api_client):
        """Test retrieving reading session statistics."""
        client, user = authenticated_api_client

        # Create multiple sessions
        for i in range(3):
            ReadingSessionModel.objects.create(
                user=user,
                started_at=timezone.now() - timedelta(days=i),
                ended_at=timezone.now() - timedelta(days=i) + timedelta(minutes=30),
                duration_seconds=1800,
                words_looked_up=10
            )

        response = client.get('/api/analytics/reading-sessions/')
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        # Adjust assertions based on actual endpoint response
        assert 'total_sessions' in data
        assert data['total_sessions'] == 3

    def test_get_lookup_stats(self, authenticated_api_client, mock_dictionary_response):
        """Test retrieving lookup statistics."""
        client, user = authenticated_api_client

        with patch('words.infrastructure.providers.free_dictionary_provider.requests.get') as mock_get:
            mock_get.return_value = mock_dictionary_response('lookupstats')
            for _ in range(5):
                client.get('/api/words/lookup/lookupstats/')

        response = client.get('/api/analytics/lookups/')
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert data['lookups_total'] == 5
        assert 'lookups_today' in data
        assert 'lookups_last_7_days' in data
        assert 'lookups_last_30_days' in data

    def test_analytics_unauthenticated_fails(self, api_client):
        """Test unauthenticated requests to analytics endpoints are rejected."""
        response = api_client.get('/api/analytics/stats/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.fixture(autouse=True)
def clear_cache():
    """Clear Redis cache before each test to ensure isolation."""
    from django.core.cache import cache
    print("Clearing cache")  # This will appear with -s flag
    cache.clear()
    yield