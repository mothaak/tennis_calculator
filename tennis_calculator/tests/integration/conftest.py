"""Integration test configuration and fixtures."""

import pytest
from tennis_calculator.core.models.tournament import Tournament
from tennis_calculator.core.processors.match_processor import MatchProcessor
from tennis_calculator.core.processors.query_processor import QueryProcessor


@pytest.fixture
def tournament_with_match():
    """Create a tournament with a sample match."""
    tournament = Tournament()
    match_processor = MatchProcessor()
    match_processor.tournament = tournament

    match_data = [
        "Match: 01",
        "Player One vs Player Two",
        "0",  # Player One scores
        "1",  # Player Two scores
        "0",
        "0",
    ]
    match_processor.process_matches(match_data)
    return tournament


@pytest.fixture
def processors():
    """Create connected processor instances."""
    match_processor = MatchProcessor()
    query_processor = QueryProcessor(match_processor)
    return match_processor, query_processor
