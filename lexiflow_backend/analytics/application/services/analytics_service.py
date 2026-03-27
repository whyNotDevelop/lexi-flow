"""
AnalyticsService: aggregated user analytics and statistics.

This service provides consolidated analytics across:
- Reading sessions (duration, count, words looked up)
- Lookup history (total lookups, lookups by time period)

Clean Architecture principles:
- Service depends only on repository interfaces.
- Aggregates data from multiple repositories without direct ORM access.
- Business logic for stats calculations is centralized.
"""

from datetime import datetime, timedelta
from typing import Dict, Any
from uuid import UUID

from django.utils import timezone

from analytics.domain.interfaces import ReadingSessionRepository
from history.domain.interfaces import HistoryRepository


class AnalyticsService:
    """
    Aggregates and provides consolidated user analytics.

    Dependencies:
        - reading_session_repo: ReadingSessionRepository for session statistics.
        - history_repo: HistoryRepository for lookup history stats.
    """

    def __init__(
        self,
        reading_session_repo: ReadingSessionRepository,
        history_repo: HistoryRepository,
    ):
        """
        Initialize the AnalyticsService.

        Args:
            reading_session_repo: Repository for reading session data.
            history_repo: Repository for lookup history data.
        """
        self.reading_session_repo = reading_session_repo
        self.history_repo = history_repo

    def get_user_stats(self, user_id: UUID) -> Dict[str, Any]:
        """
        Get comprehensive analytics for a user.

        Aggregates:
        - Reading session stats (total sessions, duration, words looked up)
        - Lookup history (total, today, last 7 days, last 30 days)

        Args:
            user_id: UUID of the user.

        Returns:
            Dictionary with comprehensive user analytics.
        """
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today_start - timedelta(days=6)
        month_start = today_start - timedelta(days=29)

        # Get reading session statistics
        reading_stats = self.reading_session_repo.get_stats(user_id)

        # Get lookup history statistics
        lookups_total = self.history_repo.count_by_user(user_id)
        lookups_today = self.history_repo.count_by_user_since(user_id, today_start)
        lookups_last_7_days = self.history_repo.count_by_user_since(user_id, week_start)
        lookups_last_30_days = self.history_repo.count_by_user_since(user_id, month_start)

        return {
            **reading_stats,
            "lookups_total": lookups_total,
            "lookups_today": lookups_today,
            "lookups_last_7_days": lookups_last_7_days,
            "lookups_last_30_days": lookups_last_30_days,
        }

    def get_reading_session_stats(self, user_id: UUID) -> Dict[str, Any]:
        """
        Get reading session statistics only.

        Args:
            user_id: UUID of the user.

        Returns:
            Dictionary with reading session analytics.
        """
        return self.reading_session_repo.get_stats(user_id)

    def get_lookup_stats(self, user_id: UUID) -> Dict[str, int]:
        """
        Get lookup history statistics only.

        Args:
            user_id: UUID of the user.

        Returns:
            Dictionary with lookup analytics.
        """
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today_start - timedelta(days=6)
        month_start = today_start - timedelta(days=29)

        lookups_total = self.history_repo.count_by_user(user_id)
        lookups_today = self.history_repo.count_by_user_since(user_id, today_start)
        lookups_last_7_days = self.history_repo.count_by_user_since(user_id, week_start)
        lookups_last_30_days = self.history_repo.count_by_user_since(user_id, month_start)

        return {
            "lookups_total": lookups_total,
            "lookups_today": lookups_today,
            "lookups_last_7_days": lookups_last_7_days,
            "lookups_last_30_days": lookups_last_30_days,
        }
