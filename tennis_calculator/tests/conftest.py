"""test configuration and fixtures"""

import pytest
from tennis_calculator.core.models.match import Match
from tennis_calculator.core.models.tournament import Tournament
from tennis_calculator.core.processors.match_processor import MatchProcessor
from tennis_calculator.core.processors.query_processor import QueryProcessor


@pytest.fixture
def tournament():
    """provides tournament instance"""
    return Tournament()


@pytest.fixture
def match_processor():
    """Create a match processor instance."""
    return MatchProcessor()


@pytest.fixture
def query_processor(match_processor):
    """Create a query processor instance."""
    return QueryProcessor(match_processor)


@pytest.fixture
def sample_match():
    """Create a sample match."""
    return Match("01", "Player One", "Player Two")


@pytest.fixture
def sample_match_data():
    """provides sample match input data"""
    return ["Match: 01", "Player One vs Player Two", "0", "1", "0", "0"]
