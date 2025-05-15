"""Fixtures for processor tests."""

import pytest
from unittest.mock import Mock
from tennis_calculator.core.models.match import Match
from tennis_calculator.core.models.tournament import Tournament
from tennis_calculator.core.processors.match_processor import MatchProcessor
from tennis_calculator.core.processors.query_processor import QueryProcessor
from tennis_calculator.core.parsers.match_parser import MatchParser


@pytest.fixture
def match_processor_with_tournament() -> MatchProcessor:
    """Return a MatchProcessor with an empty tournament."""
    return MatchProcessor()


@pytest.fixture
def query_processor(match_processor_with_tournament: MatchProcessor) -> QueryProcessor:
    """Return a QueryProcessor initialized with a MatchProcessor."""
    return QueryProcessor(match_processor_with_tournament)


@pytest.fixture
def tournament_with_match(
    match_processor_with_tournament: MatchProcessor,
) -> Tournament:
    """Return a tournament with one processed match."""
    sample_match_data = [
        "Match: 01",
        "Player Alpha vs Player Beta",
        # First set - Player Alpha wins 6-0
        "0",
        "0",
        "0",
        "0",  # Game 1
        "0",
        "0",
        "0",
        "0",  # Game 2
        "0",
        "0",
        "0",
        "0",  # Game 3
        "0",
        "0",
        "0",
        "0",  # Game 4
        "0",
        "0",
        "0",
        "0",  # Game 5
        "0",
        "0",
        "0",
        "0",  # Game 6
        # Second set - Player Alpha wins 6-0
        "0",
        "0",
        "0",
        "0",  # Game 1
        "0",
        "0",
        "0",
        "0",  # Game 2
        "0",
        "0",
        "0",
        "0",  # Game 3
        "0",
        "0",
        "0",
        "0",  # Game 4
        "0",
        "0",
        "0",
        "0",  # Game 5
        "0",
        "0",
        "0",
        "0",  # Game 6
    ]
    match_processor_with_tournament.process_matches(sample_match_data)
    return match_processor_with_tournament.tournament
