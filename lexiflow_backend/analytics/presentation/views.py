"""
DRF ViewSets for Analytics operations.

These views provide REST API endpoints for reading statistics and analytics.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from analytics.application.services.analytics_service import AnalyticsService
from analytics.presentation.serializers import ReadingSessionSerializer


class AnalyticsViewSet(viewsets.ViewSet):
    """
    ViewSet for analytics and statistics operations.

    Provides endpoints for retrieving user reading and lookup statistics.
    """

    permission_classes = [IsAuthenticated]

    def __init__(self, analytics_service: AnalyticsService = None, **kwargs):
        super().__init__(**kwargs)
        if analytics_service is None:
            from analytics.infrastructure.repositories.reading_session_repository_impl import ReadingSessionRepositoryImpl
            from history.infrastructure.repositories.history_repository_impl import HistoryRepositoryImpl

            reading_repo = ReadingSessionRepositoryImpl()
            history_repo = HistoryRepositoryImpl()

            analytics_service = AnalyticsService(
                reading_session_repo=reading_repo,
                history_repo=history_repo
            )
        self.analytics_service = analytics_service

    @extend_schema(
        summary="Get user statistics",
        description="Get comprehensive statistics for the current user including reading sessions and lookups.",
        responses={200: dict}
    )
    @action(detail=False, methods=['get'], url_path='stats')
    def get_user_stats(self, request):
        """
        Get comprehensive user statistics.

        GET /api/analytics/stats/
        """
        user_id = request.user.id

        try:
            stats = self.analytics_service.get_user_stats(user_id)
            return Response(stats)

        except Exception as e:
            return Response(
                {"error": f"Failed to get stats: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Get reading session statistics",
        description="Get statistics about user's reading sessions.",
        responses={200: dict}
    )
    @action(detail=False, methods=['get'], url_path='reading-sessions')
    def get_reading_session_stats(self, request):
        """
        Get reading session statistics.

        GET /api/analytics/reading-sessions/
        """
        user_id = request.user.id

        try:
            stats = self.analytics_service.get_reading_session_stats(user_id)
            return Response(stats)

        except Exception as e:
            return Response(
                {"error": f"Failed to get reading stats: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Get lookup statistics",
        description="Get statistics about user's word lookups.",
        responses={200: dict}
    )
    @action(detail=False, methods=['get'], url_path='lookups')
    def get_lookup_stats(self, request):
        """
        Get lookup statistics.

        GET /api/analytics/lookups/
        """
        user_id = request.user.id

        try:
            stats = self.analytics_service.get_lookup_stats(user_id)
            return Response(stats)

        except Exception as e:
            return Response(
                {"error": f"Failed to get lookup stats: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )