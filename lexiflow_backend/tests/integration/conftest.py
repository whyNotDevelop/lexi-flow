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
            response.json.return_value = [
                {
                    "word": word,
                    "phonetic": f"/{word}/",
                    "meanings": [
                        {
                            "partOfSpeech": "noun",
                            "definitions": [
                                {
                                    "definition": f"Definition of {word}",
                                    "example": f"Example sentence with {word}"
                                }
                            ],
                            "synonyms": ["similar", "alike"]
                        }
                    ]
                }
            ]
        else:
            # Simulate a non‑200 response
            response.json.side_effect = Exception("Not found")
            response.raise_for_status.side_effect = Exception("Error")
        return response
    return _make_response