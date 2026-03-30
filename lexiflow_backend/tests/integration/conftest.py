import json
import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from unittest.mock import MagicMock

User = get_user_model()

@pytest.fixture
def authenticated_api_client():
    """Provide an authenticated API client with a test user."""
    user = User.objects.create_user(
        email='testuser@example.com',
        username='testuser@example.com',
        password='TestPassword123!',
        full_name='Test User'
    )
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client, user

@pytest.fixture
def mock_dictionary_response():
    """Factory to create mock dictionary API responses."""
    def _make_response(word: str, status_code: int = 200):
        response = MagicMock()
        response.status_code = status_code
        if status_code == 200:
            response.raise_for_status = MagicMock()  # no-op
            response.json.return_value = [
                {
                    "word": word,
                    "phonetic": f"/{word}/",
                    "phonetics": [
                        {
                            "text": f"/{word}/",
                            "audio": f"https://api.dictionaryapi.dev/media/pronunciations/en/{word}-us.mp3"
                        }
                    ],
                    "meanings": [
                        {
                            "partOfSpeech": "noun",
                            "definitions": [
                                {
                                    "definition": f"Definition of {word}",
                                    "example": f"Example sentence with {word}",
                                    "synonyms": ["similar", "alike"]
                                }
                            ]
                        }
                    ]
                }
            ]
        else:
            response.raise_for_status.side_effect = Exception(f"HTTP {status_code}")
            response.json.side_effect = json.JSONDecodeError("msg", "doc", 0)
        return response
    return _make_response