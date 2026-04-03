import pytest
from unittest.mock import patch
from rest_framework import status

from words.infrastructure.models import WordModel
from vocabulary.infrastructure.models import VocabularyEntryModel

@pytest.mark.django_db
class TestVocabularyFlow:
    """Integration tests for vocabulary management (save, remove, list, search)."""

    def test_save_word_success(self, authenticated_api_client, mock_dictionary_response):
        """Save a word to user's vocabulary."""
        client, user = authenticated_api_client

        # 1. Create a word via lookup (mocked)
        with patch('words.infrastructure.providers.free_dictionary_provider.requests.get') as mock_get:
            mock_get.return_value = mock_dictionary_response('testword')
            response = client.get('/api/words/lookup/testword/')
            assert response.status_code == status.HTTP_200_OK

            word = WordModel.objects.get(text='testword')

        # 2. Save to vocabulary
        response = client.post(f'/api/vocabulary/save/{word.id}/', format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['word_id'] == str(word.id)
        assert response.data['user_id'] == str(user.id)

        # 3. Verify in database
        assert VocabularyEntryModel.objects.filter(user=user, word=word).exists()

    def test_save_word_duplicate_fails(self, authenticated_api_client, mock_dictionary_response):
        """Attempt to save the same word twice – should fail."""
        client, user = authenticated_api_client

        with patch('words.infrastructure.providers.free_dictionary_provider.requests.get') as mock_get:
            mock_get.return_value = mock_dictionary_response('duplicate')
            client.get('/api/words/lookup/duplicate/')
            word = WordModel.objects.get(text='duplicate')

        # First save
        response1 = client.post(f'/api/vocabulary/save/{word.id}/', format='json')
        assert response1.status_code == status.HTTP_201_CREATED

        # Second save (duplicate) should fail
        response2 = client.post(f'/api/vocabulary/save/{word.id}/', format='json')
        assert response2.status_code in [status.HTTP_409_CONFLICT, status.HTTP_400_BAD_REQUEST]

    def test_remove_word_success(self, authenticated_api_client, mock_dictionary_response):
        """Remove a word from vocabulary."""
        client, user = authenticated_api_client

        with patch('words.infrastructure.providers.free_dictionary_provider.requests.get') as mock_get:
            mock_get.return_value = mock_dictionary_response('removeword')
            client.get('/api/words/lookup/removeword/')
            word = WordModel.objects.get(text='removeword')

        # Save first
        client.post(f'/api/vocabulary/save/{word.id}/', format='json')
        assert VocabularyEntryModel.objects.filter(user=user, word=word).exists()

        # Remove
        response = client.delete(f'/api/vocabulary/remove/{word.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify removed
        assert not VocabularyEntryModel.objects.filter(user=user, word=word).exists()

    def test_list_vocabulary_empty(self, authenticated_api_client):
        """List vocabulary when user has no saved words."""
        client, user = authenticated_api_client
        response = client.get('/api/vocabulary/list/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data == []  # or paginated empty list

    def test_list_vocabulary_with_words(self, authenticated_api_client, mock_dictionary_response):
        """List vocabulary after saving multiple words."""
        client, user = authenticated_api_client

        words = []
        for w in ['alpha', 'beta', 'gamma']:
            with patch('words.infrastructure.providers.free_dictionary_provider.requests.get') as mock_get:
                mock_get.return_value = mock_dictionary_response(w)
                client.get(f'/api/words/lookup/{w}/')
                word = WordModel.objects.get(text=w)
                client.post(f'/api/vocabulary/save/{word.id}/', format='json')
                words.append(word)

        response = client.get('/api/vocabulary/list/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3
        # Optionally check order (newest first)

    def test_search_vocabulary(self, authenticated_api_client, mock_dictionary_response):
        """Search vocabulary by word text."""
        client, user = authenticated_api_client

        # Save words: serendipity, ephemeral, sentient
        for w in ['serendipity', 'ephemeral', 'sentient']:
            with patch('words.infrastructure.providers.free_dictionary_provider.requests.get') as mock_get:
                mock_get.return_value = mock_dictionary_response(w)
                client.get(f'/api/words/lookup/{w}/')
                word = WordModel.objects.get(text=w)
                client.post(f'/api/vocabulary/save/{word.id}/', format='json')

        # Search for 'se' – should match serendipity and sentient
        response = client.get('/api/vocabulary/search/?q=se')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        texts = [item['word_text'] for item in response.data]
        assert 'serendipity' in texts
        assert 'sentient' in texts
        assert 'ephemeral' not in texts

    def test_is_word_saved(self, authenticated_api_client, mock_dictionary_response):
        """Check if a word is saved."""
        client, user = authenticated_api_client

        with patch('words.infrastructure.providers.free_dictionary_provider.requests.get') as mock_get:
            mock_get.return_value = mock_dictionary_response('savedword')
            client.get('/api/words/lookup/savedword/')
            word = WordModel.objects.get(text='savedword')

        # Initially not saved
        response = client.get(f'/api/vocabulary/is-saved/{word.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_saved'] is False

        # Save it
        client.post(f'/api/vocabulary/save/{word.id}/', format='json')

        # Now should be saved
        response = client.get(f'/api/vocabulary/is-saved/{word.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_saved'] is True

@pytest.fixture(autouse=True)
def clear_cache():
    """Clear Redis cache before each test to ensure isolation."""
    from django.core.cache import cache
    cache.clear()
    yield