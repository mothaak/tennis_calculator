"""Unit test configuration and fixtures."""

import pytest
from unittest.mock import Mock
from tennis_calculator.core.models.match import Match
from tennis_calculator.core.models.tournament import Tournament
from tennis_calculator.core.processors.match_processor import MatchProcessor


@pytest.fixture
def mock_match():
    """Create a mock match."""
    match = Mock(spec=Match)
    match.match_id = "01"
    match.player_one = "Player One"
    match.player_two = "Player Two"
    match.get_winner.return_value = "Player One"
    match.get_loser.return_value = "Player Two"
    match.result = (2, 0)
    return match


@pytest.fixture
def mock_tournament():
    """Create a mock tournament."""
    tournament = Mock(spec=Tournament)
    tournament.matches = {}
    return tournament


@pytest.fixture
def mock_match_processor():
    """Create a mock match processor."""
    processor = Mock(spec=MatchProcessor)
    processor.tournament = Mock(spec=Tournament)
    return processor
