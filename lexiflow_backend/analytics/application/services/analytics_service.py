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
from django.utils import timezone
from typing import Dict, Any
from uuid import UUID

class AnalyticsService:
    def __init__(self, reading_session_repo, history_repo):
        self.reading_session_repo = reading_session_repo
        self.history_repo = history_repo

    def get_user_stats(self, user_id: UUID) -> Dict[str, Any]:
        # Reading stats
        reading_stats = self.get_reading_session_stats(user_id)
        # Lookup stats
        lookup_stats = self.get_lookup_stats(user_id)
        # Merge
        return {**reading_stats, **lookup_stats}

    def get_reading_session_stats(self, user_id: UUID) -> Dict[str, Any]:
        sessions = self.reading_session_repo.get_by_user(user_id)
        total_sessions = len(sessions)
        total_reading_time = sum(s.duration_seconds for s in sessions)
        total_words_looked_up = sum(s.words_looked_up for s in sessions)
        avg_duration = total_reading_time / total_sessions if total_sessions > 0 else 0
        return {
            "total_sessions": total_sessions,
            "active_sessions": sum(1 for s in sessions if s.ended_at is None),
            "reading_time_seconds": total_reading_time,
            "average_session_duration_seconds": avg_duration,
            "total_words_looked_up": total_words_looked_up,
        }

    def get_lookup_stats(self, user_id: UUID) -> Dict[str, int]:
        total = self.history_repo.count_by_user(user_id)
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today_start - timedelta(days=7)
        month_start = today_start - timedelta(days=30)
        return {
            "lookups_total": total,
            "lookups_today": self.history_repo.count_by_user_since(user_id, today_start),
            "lookups_last_7_days": self.history_repo.count_by_user_since(user_id, week_start),
            "lookups_last_30_days": self.history_repo.count_by_user_since(user_id, month_start),
        }