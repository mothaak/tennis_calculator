"""verifies match processing functionality"""

import pytest
from tennis_calculator.core.exceptions import InvalidMatchFormatException


def test_process_matches(match_processor, sample_match_data):
    """verifies match processing from input"""
    match_processor.process_matches(sample_match_data)
    match = match_processor.get_match("01")
    assert match is not None
    assert match.player_one == "Player One"
    assert match.player_two == "Player Two"


def test_process_multiple_matches(match_processor):
    """verifies multiple match processing"""
    data = [
        "Match: 01",
        "Player One vs Player Two",
        "0",
        "1",
        "Match: 02",
        "Player Three vs Player Four",
        "0",
        "1",
    ]
    match_processor.process_matches(data)
    assert match_processor.get_match("01") is not None
    assert match_processor.get_match("02") is not None


def test_invalid_match_data(match_processor):
    """verifies invalid match data handling"""
    invalid_data = ["Invalid Match"]
    with pytest.raises(InvalidMatchFormatException):
        match_processor.process_matches(invalid_data)
