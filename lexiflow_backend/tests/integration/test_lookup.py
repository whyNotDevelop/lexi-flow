import pytest
from unittest.mock import patch
from rest_framework import status

from words.infrastructure.models import WordModel
from history.infrastructure.models import LookupHistoryModel

@pytest.mark.django_db
class TestLookupFlow:
    def test_first_lookup_success(self, authenticated_api_client, mock_dictionary_response):
        client, user = authenticated_api_client

        with patch('words.infrastructure.providers.free_dictionary_provider.requests.get') as mock_get:
            mock_get.return_value = mock_dictionary_response('serendipity')

            response = client.get('/api/words/lookup/serendipity/')
            assert response.status_code == status.HTTP_200_OK
            assert response.data['text'] == 'serendipity'
            assert 'definitions' in response.data
            assert len(response.data['definitions']) > 0
            assert response.data['definitions'][0]['meaning'] == 'Definition of serendipity'

            # Verify API was called
            mock_get.assert_called_once()

            # Verify word was saved to DB
            assert WordModel.objects.filter(text='serendipity').exists()

            # Verify definitions in DB
            word = WordModel.objects.get(text='serendipity')
            assert word.definitions.count() > 0

            # Verify history recorded
            assert LookupHistoryModel.objects.filter(user=user, word=word).exists()