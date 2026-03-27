"""
DRF ViewSets for Word operations.

These views provide REST API endpoints for word lookup and search.
They use the LookupService from the application layer.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema

from words.application.services.lookup_service import LookupService
from words.presentation.serializers import WordSerializer


class WordViewSet(viewsets.ViewSet):
    """
    ViewSet for word lookup operations.

    Provides endpoints for looking up words with caching and external API fallback.
    """

    permission_classes = [IsAuthenticated]

    def __init__(self, lookup_service: LookupService = None, **kwargs):
        super().__init__(**kwargs)
        # In production, use dependency injection container
        # For now, we'll initialize services here (to be replaced with DI)
        if lookup_service is None:
            from words.infrastructure.repositories.word_repository_impl import WordRepositoryImpl
            from words.infrastructure.providers.free_dictionary_provider import FreeDictionaryProvider
            from history.infrastructure.repositories.history_repository_impl import HistoryRepositoryImpl

            word_repo = WordRepositoryImpl()
            history_repo = HistoryRepositoryImpl()
            provider = FreeDictionaryProvider()

            lookup_service = LookupService(
                word_repo=word_repo,
                dict_provider=provider,
                history_repo=history_repo
            )
        self.lookup_service = lookup_service

    @extend_schema(
        summary="Look up a word",
        description="Look up a word definition with caching and external API fallback. Records lookup in history.",
        responses={200: WordSerializer}
    )
    @action(detail=False, methods=['get'], url_path='lookup/(?P<word>[^/.]+)')
    def lookup(self, request, word=None):
        """
        Look up a word by text.

        GET /api/words/lookup/{word}/?language=en

        Returns word definition or 404 if not found.
        """
        language = request.query_params.get('language', 'en')
        user_id = request.user.id

        try:
            word_entity = self.lookup_service.lookup_word(word, user_id, language)

            if word_entity is None:
                return Response(
                    {"error": f"Word '{word}' not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = WordSerializer(word_entity)
            return Response(serializer.data)

        except Exception as e:
            return Response(
                {"error": f"Lookup failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )