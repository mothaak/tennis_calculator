"""verifies query processing functionality"""

import pytest
from tennis_calculator.core.exceptions import (
    InvalidQueryException,
    MatchNotFoundException,
    PlayerNotFoundException,
)


def test_score_match_query(query_processor, tournament_with_match):
    """Test score match query."""
    result = query_processor.handle_query("Score Match 01")
    assert "Player Alpha defeated Player Beta" in result
    assert "2 sets to 0" in result


def test_games_player_query(query_processor, tournament_with_match):
    """verifies games player query processing"""
    result = query_processor.handle_query("Games Player Player Alpha")
    won, lost = map(int, result.split())
    assert won == 12
    assert lost == 0


def test_invalid_query_format(query_processor):
    """Test invalid query format."""
    with pytest.raises(InvalidQueryException):
        query_processor.handle_query("Invalid Query")


def test_score_match_not_found(query_processor):
    """Test score match not found."""
    with pytest.raises(MatchNotFoundException):
        query_processor.handle_query("Score Match 99")


def test_games_player_not_found(query_processor):
    """Test games player not found."""
    with pytest.raises(PlayerNotFoundException):
        query_processor.handle_query("Games Player Invalid")
