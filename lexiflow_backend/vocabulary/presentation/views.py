"""
DRF ViewSets for Vocabulary operations.

These views provide REST API endpoints for managing personal vocabulary.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from vocabulary.application.services.vocabulary_service import VocabularyService
from vocabulary.presentation.serializers import VocabularyEntrySerializer


class VocabularyViewSet(viewsets.ViewSet):
    """
    ViewSet for vocabulary management operations.

    Provides endpoints for saving, removing, and searching personal vocabulary.
    """

    permission_classes = [IsAuthenticated]

    def __init__(self, vocab_service: VocabularyService = None, **kwargs):
        super().__init__(**kwargs)
        if vocab_service is None:
            from vocabulary.infrastructure.repositories.vocabulary_repository_impl import VocabularyRepositoryImpl
            from words.infrastructure.repositories.word_repository_impl import WordRepositoryImpl

            vocab_repo = VocabularyRepositoryImpl()
            word_repo = WordRepositoryImpl()

            vocab_service = VocabularyService(
                vocab_repo=vocab_repo,
                word_repo=word_repo
            )
        self.vocab_service = vocab_service

    @extend_schema(
        summary="Save word to vocabulary",
        description="Save a word to the user's personal vocabulary list.",
        request=None,
        responses={201: VocabularyEntrySerializer}
    )
    @action(detail=False, methods=['post'], url_path='save/(?P<word_id>[^/.]+)')
    def save_word(self, request, word_id=None):
        """
        Save a word to user's vocabulary.

        POST /api/vocabulary/save/{word_id}/
        """
        from uuid import UUID
        user_id = request.user.id

        try:
            word_uuid = UUID(word_id)
        except ValueError:
            return Response(
                {"error": f"Invalid word ID format: {word_id}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            vocab_entry = self.vocab_service.save_word(user_id, word_uuid)
        except Exception as e:
            return Response(
                {"error": f"Failed to save word: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # If the service returns None, it means the word was already saved
        if vocab_entry is None:
            return Response(
                {"error": "Word already in vocabulary"},
                status=status.HTTP_409_CONFLICT
            )

        serializer = VocabularyEntrySerializer(vocab_entry)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Remove word from vocabulary",
        description="Remove a word from the user's personal vocabulary list.",
        responses={204: None}
    )
    @action(detail=False, methods=['delete'], url_path='remove/(?P<word_id>[^/.]+)')
    def remove_word(self, request, word_id=None):
        """
        Remove a word from user's vocabulary.

        DELETE /api/vocabulary/remove/{word_id}/
        """
        from uuid import UUID
        user_id = request.user.id

        try:
            word_uuid = UUID(word_id)
            self.vocab_service.remove_word(user_id, word_uuid)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValueError as e:
            return Response(
                {"error": f"Invalid word ID: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to remove word: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Check if word is saved",
        description="Check if a specific word is saved in user's vocabulary.",
        responses={200: dict}
    )
    @action(detail=False, methods=['get'], url_path='is-saved/(?P<word_id>[^/.]+)')
    def is_word_saved(self, request, word_id=None):
        """
        Check if word is saved in vocabulary.

        GET /api/vocabulary/is-saved/{word_id}/
        """
        from uuid import UUID
        user_id = request.user.id

        try:
            word_uuid = UUID(word_id)
            is_saved = self.vocab_service.is_word_saved(user_id, word_uuid)
            return Response({"is_saved": is_saved})

        except ValueError as e:
            return Response(
                {"error": f"Invalid word ID: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

    @extend_schema(
        summary="Search vocabulary",
        description="Search user's saved vocabulary by word text.",
        responses={200: VocabularyEntrySerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='search')
    def search_vocabulary(self, request):
        """
        Search user's vocabulary.

        GET /api/vocabulary/search/?q=word&limit=10
        """
        user_id = request.user.id
        query = request.query_params.get('q', '')
        #limit = int(request.query_params.get('limit', 50))

        try:
            vocab_entries = self.vocab_service.search_vocabulary(user_id, query)
            serializer = VocabularyEntrySerializer(vocab_entries, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response(
                {"error": f"Search failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Get user vocabulary",
        description="Get all words saved by the user.",
        responses={200: VocabularyEntrySerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='list')
    def get_user_vocabulary(self, request):
        """
        Get user's complete vocabulary list.

        GET /api/vocabulary/list/?limit=100
        """
        user_id = request.user.id
        #limit = int(request.query_params.get('limit', 1000))

        try:
            vocab_entries = self.vocab_service.get_user_vocabulary(user_id)
            serializer = VocabularyEntrySerializer(vocab_entries, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response(
                {"error": f"Failed to get vocabulary: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )