"""
DRF ViewSets for History operations.

These views provide REST API endpoints for lookup history management.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware
from drf_spectacular.utils import extend_schema

from history.application.services.history_service import HistoryService
from history.presentation.serializers import LookupHistorySerializer


class HistoryViewSet(viewsets.ViewSet):
    """
    ViewSet for lookup history operations.

    Provides endpoints for retrieving and managing lookup history.
    """

    permission_classes = [IsAuthenticated]

    def __init__(self, history_service: HistoryService = None, **kwargs):
        super().__init__(**kwargs)
        if history_service is None:
            from history.infrastructure.repositories.history_repository_impl import HistoryRepositoryImpl

            history_repo = HistoryRepositoryImpl()
            history_service = HistoryService(history_repo=history_repo)
        self.history_service = history_service

    @extend_schema(
        summary="Get lookup history",
        description="Get user's word lookup history with pagination.",
        responses={200: LookupHistorySerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='list')
    def get_history(self, request):
        """
        Get user's lookup history.

        GET /api/history/list/?limit=20&before=2024-01-01T00:00:00Z
        """
        user_id = request.user.id
        limit = int(request.query_params.get('limit', 20))
        before_str = request.query_params.get('before')

        before = None
        if before_str:
            from datetime import datetime
            before = datetime.fromisoformat(before_str.replace('Z', '+00:00'))

        try:
            history_entries = self.history_service.get_user_history(user_id, limit, before)
            serializer = LookupHistorySerializer(history_entries, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response(
                {"error": f"Failed to get history: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Clear lookup history",
        description="Delete all lookup history for the current user.",
        responses={200: dict}
    )
    @action(detail=False, methods=['delete'], url_path='clear')
    def clear_history(self, request):
        """
        Clear user's lookup history.

        DELETE /api/history/clear/
        """
        user_id = request.user.id

        try:
            deleted_count = self.history_service.clear_user_history(user_id)
            return Response({"deleted_count": deleted_count})

        except Exception as e:
            return Response(
                {"error": f"Failed to clear history: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Get lookup count",
        description="Get total number of word lookups for the user.",
        responses={200: dict}
    )
    @action(detail=False, methods=['get'], url_path='count')
    def get_lookup_count(self, request):
        """
        Get user's total lookup count.

        GET /api/history/count/
        """
        user_id = request.user.id

        try:
            count = self.history_service.get_lookup_count(user_id)
            return Response({"count": count})

        except Exception as e:
            return Response(
                {"error": f"Failed to get count: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Get lookup count since date",
        description="Get number of lookups since a specific date.",
        responses={200: dict}
    )

    @action(detail=False, methods=['get'], url_path='count-since')
    def get_lookup_count_since(self, request):
        """
        Get lookup count since a specific time.

        GET /api/history/count-since/?since=2024-01-01T00:00:00Z
        """
        user_id = request.user.id
        since_str = request.query_params.get('since')

        if not since_str:
            return Response(
                {"error": "Missing 'since' parameter"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Use Django's parse_datetime (handles ISO 8601 with timezone)
        since = parse_datetime(since_str)
        if since is None:
            return Response(
                {"error": "Invalid date format. Use ISO 8601 (e.g., 2024-01-01T00:00:00Z)."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Ensure the datetime is timezone-aware (Django's ORM expects aware for comparisons)
        if not is_aware(since):
            since = make_aware(since)

        try:
            count = self.history_service.get_lookup_count_since(user_id, since)
            return Response({"count": count})
        except Exception as e:
            return Response(
                {"error": f"Failed to get count: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )