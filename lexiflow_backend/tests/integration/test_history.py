import pytest
from unittest.mock import patch
from rest_framework import status
from datetime import datetime, timedelta
from django.utils import timezone

from words.infrastructure.models import WordModel
from history.infrastructure.models import LookupHistoryModel

@pytest.mark.django_db
class TestHistoryFlow:
    """Integration tests for lookup history management."""

    def test_record_lookup_on_word_lookup(self, authenticated_api_client, mock_dictionary_response):
        """
        Test that looking up a word automatically records history.
        """
        client, user = authenticated_api_client

        with patch('words.infrastructure.providers.free_dictionary_provider.requests.get') as mock_get:
            mock_get.return_value = mock_dictionary_response('historyword')
            response = client.get('/api/words/lookup/historyword/')
            assert response.status_code == status.HTTP_200_OK

        word = WordModel.objects.get(text='historyword')
        history_exists = LookupHistoryModel.objects.filter(user=user, word=word).exists()
        assert history_exists

    def test_get_history_list(self, authenticated_api_client, mock_dictionary_response):
        """
        Test retrieving user's lookup history.
        """
        client, user = authenticated_api_client

        with patch('words.infrastructure.providers.free_dictionary_provider.requests.get') as mock_get:
            mock_get.return_value = mock_dictionary_response('historylist')
            client.get('/api/words/lookup/historylist/')
            client.get('/api/words/lookup/historylist/')  # duplicate

        response = client.get('/api/history/list/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert 'looked_up_at' in response.data[0]

    def test_get_history_with_limit(self, authenticated_api_client, mock_dictionary_response):
        """
        Test pagination of history with limit parameter.
        """
        client, user = authenticated_api_client

        with patch('words.infrastructure.providers.free_dictionary_provider.requests.get') as mock_get:
            mock_get.return_value = mock_dictionary_response('paginate')
            for _ in range(5):
                client.get('/api/words/lookup/paginate/')

        response = client.get('/api/history/list/?limit=2')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_get_lookup_count(self, authenticated_api_client, mock_dictionary_response):
        """
        Test getting total lookup count.
        """
        client, user = authenticated_api_client

        with patch('words.infrastructure.providers.free_dictionary_provider.requests.get') as mock_get:
            mock_get.return_value = mock_dictionary_response('countword')
            for _ in range(3):
                client.get('/api/words/lookup/countword/')

        response = client.get('/api/history/count/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 3

    def test_get_lookup_count_since(self, authenticated_api_client, mock_dictionary_response):
        """
        Test getting lookup count since a specific date.
        """
        client, user = authenticated_api_client

        with patch('words.infrastructure.providers.free_dictionary_provider.requests.get') as mock_get:
            mock_get.return_value = mock_dictionary_response('sinceword')
            client.get('/api/words/lookup/sinceword/')
            # Wait a moment to ensure timestamps differ? Not needed for mock, but we'll use a since date far in the past.
            since = (timezone.now() - timedelta(hours=1)).replace(microsecond=0).isoformat().replace('+00:00', 'Z')
            response = client.get(f'/api/history/count-since/?since={since}')
            print("Response status:", response.status_code)
            print("Response data:", response.data)
            assert response.status_code == status.HTTP_200_OK
            assert response.data['count'] >= 1

    def test_clear_all_history(self, authenticated_api_client, mock_dictionary_response):
        """
        Test clearing all user's history.
        """
        client, user = authenticated_api_client

        with patch('words.infrastructure.providers.free_dictionary_provider.requests.get') as mock_get:
            mock_get.return_value = mock_dictionary_response('clearword')
            for _ in range(3):
                client.get('/api/words/lookup/clearword/')

        response = client.delete('/api/history/clear/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['deleted_count'] == 3

        remaining = LookupHistoryModel.objects.filter(user=user).count()
        assert remaining == 0

    def test_unauthenticated_history_access_fails(self, api_client):
        """
        Test that unauthenticated requests to history endpoints are rejected.
        """
        response = api_client.get('/api/history/list/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.fixture(autouse=True)
def clear_cache():
    """Clear Redis cache before each test to ensure isolation."""
    from django.core.cache import cache
    print("Clearing cache")  # This will appear with -s flag
    cache.clear()
    yield