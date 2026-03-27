"""
Unit tests for HistoryService.
"""
import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock
from uuid import uuid4

from history.application.services.history_service import HistoryService
from history.domain.entities import LookupHistory


@pytest.mark.django_db
class TestHistoryService:
    """Test suite for the HistoryService."""

    def setup_method(self):
        """Set up mocks for each test."""
        self.history_repo = Mock()
        self.service = HistoryService(self.history_repo)
        
        self.user_id = uuid4()
        self.word_id = uuid4()
        self.history_id = uuid4()

    def test_record_lookup(self):
        """Test: recording a new word lookup."""
        now = datetime.now()
        created_history = LookupHistory(
            id=self.history_id,
            user_id=self.user_id,
            word_id=self.word_id,
            looked_up_at=now,
        )
        self.history_repo.add.return_value = created_history

        result = self.service.record_lookup(self.user_id, self.word_id)

        assert result == created_history
        assert result.user_id == self.user_id
        assert result.word_id == self.word_id
        self.history_repo.add.assert_called_once()

        # Verify that a LookupHistory was created
        call_args = self.history_repo.add.call_args[0][0]
        assert isinstance(call_args, LookupHistory)
        assert call_args.user_id == self.user_id
        assert call_args.word_id == self.word_id

    def test_get_user_history(self):
        """Test: retrieving lookup history for a user."""
        histories = [
            LookupHistory(
                id=uuid4(),
                user_id=self.user_id,
                word_id=uuid4(),
                looked_up_at=datetime.now() - timedelta(hours=1),
            ),
            LookupHistory(
                id=uuid4(),
                user_id=self.user_id,
                word_id=uuid4(),
                looked_up_at=datetime.now() - timedelta(hours=2),
            ),
        ]
        self.history_repo.get_by_user.return_value = histories

        result = self.service.get_user_history(self.user_id)

        assert result == histories
        assert len(result) == 2
        self.history_repo.get_by_user.assert_called_once_with(
            self.user_id, 50, None
        )

    def test_get_user_history_with_limit(self):
        """Test: retrieving history with custom limit."""
        histories = [
            LookupHistory(
                id=uuid4(),
                user_id=self.user_id,
                word_id=uuid4(),
                looked_up_at=datetime.now(),
            ),
        ]
        self.history_repo.get_by_user.return_value = histories

        result = self.service.get_user_history(self.user_id, limit=10)

        assert result == histories
        self.history_repo.get_by_user.assert_called_once_with(
            self.user_id, 10, None
        )

    def test_get_user_history_with_before_parameter(self):
        """Test: retrieving history before a specific time."""
        before = datetime.now()
        histories = [
            LookupHistory(
                id=uuid4(),
                user_id=self.user_id,
                word_id=uuid4(),
                looked_up_at=before - timedelta(hours=1),
            )
        ]
        self.history_repo.get_by_user.return_value = histories

        result = self.service.get_user_history(self.user_id, before=before)

        assert result == histories
        self.history_repo.get_by_user.assert_called_once_with(
            self.user_id, 50, before
        )

    def test_get_user_history_empty(self):
        """Test: retrieving history for user with no lookups."""
        self.history_repo.get_by_user.return_value = []

        result = self.service.get_user_history(self.user_id)

        assert result == []

    def test_delete_lookup(self):
        """Test: deleting a single history entry."""
        self.service.delete_lookup(self.history_id)

        self.history_repo.delete.assert_called_once_with(self.history_id)

    def test_clear_user_history(self):
        """Test: deleting all history for a user."""
        self.history_repo.clear_for_user.return_value = 42

        result = self.service.clear_user_history(self.user_id)

        assert result == 42
        self.history_repo.clear_for_user.assert_called_once_with(self.user_id)

    def test_clear_user_history_empty(self):
        """Test: clearing history for user with no entries."""
        self.history_repo.clear_for_user.return_value = 0

        result = self.service.clear_user_history(self.user_id)

        assert result == 0

    def test_get_lookup_count(self):
        """Test: getting total lookup count for a user."""
        self.history_repo.count_by_user.return_value = 123

        result = self.service.get_lookup_count(self.user_id)

        assert result == 123
        self.history_repo.count_by_user.assert_called_once_with(self.user_id)

    def test_get_lookup_count_zero(self):
        """Test: getting lookup count for user with no lookups."""
        self.history_repo.count_by_user.return_value = 0

        result = self.service.get_lookup_count(self.user_id)

        assert result == 0

    def test_get_lookup_count_since(self):
        """Test: getting lookup count since a specific time."""
        since = datetime.now() - timedelta(days=7)
        self.history_repo.count_by_user_since.return_value = 15

        result = self.service.get_looklup_count_since(self.user_id, since)

        assert result == 15
        self.history_repo.count_by_user_since.assert_called_once_with(
            self.user_id, since
        )

    def test_get_lookup_count_since_zero(self):
        """Test: getting lookup count since a time when no lookups occurred."""
        since = datetime.now() + timedelta(days=1)
        self.history_repo.count_by_user_since.return_value = 0

        result = self.service.get_looklup_count_since(self.user_id, since)

        assert result == 0
