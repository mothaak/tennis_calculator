"""verifies match parsing functionality"""

import pytest
from tennis_calculator.core.parsers.match_parser import MatchParser
from tennis_calculator.core.exceptions import InvalidMatchFormatException


def test_parse_match_details(sample_match_data):
    """verifies match details parsing from input"""
    match_id, player_one, player_two = MatchParser.parse_match_details(
        sample_match_data
    )
    assert match_id == "01"
    assert player_one == "Player One"
    assert player_two == "Player Two"


def test_parse_match_with_empty_lines():
    """verifies match parsing with empty lines"""
    data = ["", "Match: 01", "", "Player One vs Player Two", "", "0", "1", "", "0"]
    # Filter empty lines before parsing
    non_empty_lines = [line for line in data if line.strip()]
    match_id, player_one, player_two = MatchParser.parse_match_details(non_empty_lines)
    assert match_id == "01"
    assert player_one == "Player One"
    assert player_two == "Player Two"


def test_invalid_match_format():
    """verifies invalid match format handling"""
    invalid_data = ["Invalid format"]
    with pytest.raises(InvalidMatchFormatException):
        MatchParser.parse_match_details(invalid_data)


def test_invalid_player_format():
    """verifies invalid player format handling"""
    invalid_data = ["Match: 01", "Invalid player format"]
    with pytest.raises(InvalidMatchFormatException):
        MatchParser.parse_match_details(invalid_data)


def test_invalid_point_format():
    """verifies invalid point format handling"""
    invalid_data = ["Match: 01", "Player One vs Player Two", "invalid"]
    with pytest.raises(InvalidMatchFormatException):
        MatchParser.parse_points(invalid_data)


def test_create_match():
    """verifies match creation from data"""
    data = ["Match: 01", "Player One vs Player Two", "0", "1", "0", "0"]
    match = MatchParser.create_match(data)
    assert match.match_id == "01"
    assert match.player_one == "Player One"
    assert match.player_two == "Player Two"


def test_parse_incomplete_match():
    """verifies incomplete match data handling"""
    incomplete_data = ["Match: 01"]
    with pytest.raises(InvalidMatchFormatException):
        MatchParser.parse_match_details(incomplete_data)
