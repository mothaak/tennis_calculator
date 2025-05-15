"""verifies match scoring functionality"""

import pytest
from tennis_calculator.core.models.match import Match
from tennis_calculator.core.rules import (
    PLAYER_ONE,
    PLAYER_TWO,
    SETS_TO_WIN_MATCH,
    MATCH_NOT_STARTED,
)
from tennis_calculator.core.exceptions import (
    InvalidPlayerNumberException,
    MatchCompletedException,
)


class TestMatch:
    """validates match scoring behavior"""

    def test_initial_state(self):
        """verifies initial match state"""
        match = Match("01", "Player One", "Player Two")
        assert match.match_id == "01"
        assert match.player_one == "Player One"
        assert match.player_two == "Player Two"
        assert match.score_display() == "0-0"
        assert not match.winner
        assert match.sets_score.player_one == 0
        assert match.sets_score.player_two == 0

    def test_record_point(self):
        """verifies point recording"""
        match = Match("01", "Player One", "Player Two")
        match.record_point(PLAYER_ONE)
        assert match.current_set.current_game.points.player_one == 1
        assert match.current_set.current_game.points.player_two == 0

    def test_win_game(self):
        """verifies game completion"""
        match = Match("01", "Player One", "Player Two")
        for _ in range(4):
            match.record_point(PLAYER_ONE)
        assert match.current_set.games.player_one == 1
        assert match.current_set.games.player_two == 0

    def test_win_set(self):
        """verifies set completion"""
        match = Match("01", "Player One", "Player Two")
        for _ in range(24):
            match.record_point(PLAYER_ONE)
        assert match.sets_score.player_one == 1
        assert match.sets_score.player_two == 0

    def test_win_match(self):
        """verifies match completion"""
        match = Match("01", "Player One", "Player Two")
        for _ in range(48):
            match.record_point(PLAYER_ONE)
        assert match.winner == "Player One"
        assert match.sets_score.player_one == SETS_TO_WIN_MATCH
        assert match.sets_score.player_two == 0

    def test_record_point_after_completion(self):
        """verifies point recording after match completion"""
        match = Match("01", "Player One", "Player Two")
        for _ in range(48):
            match.record_point(PLAYER_ONE)
        with pytest.raises(MatchCompletedException):
            match.record_point(PLAYER_TWO)

    def test_invalid_player_number(self):
        """verifies invalid player number handling"""
        match = Match("01", "Player One", "Player Two")
        with pytest.raises(InvalidPlayerNumberException):
            match.record_point(3)

    def test_games_summary(self):
        """verifies games summary calculation"""
        match = Match("01", "Player One", "Player Two")
        for _ in range(4):
            match.record_point(PLAYER_ONE)
        won, lost = match.games_summary("Player One")
        assert won == 1
        assert lost == 0
        won, lost = match.games_summary("Player Two")
        assert won == 0
        assert lost == 1

    def test_not_started_display(self):
        """verifies not started match display"""
        match = Match("01", "Player One", "Player Two")
        assert match.score_display() == "0-0"
