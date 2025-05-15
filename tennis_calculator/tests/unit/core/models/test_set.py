"""verifies set scoring functionality"""

import pytest
from tennis_calculator.core.models.set import Set
from tennis_calculator.core.rules import PLAYER_ONE, PLAYER_TWO


class TestSet:
    """validates set scoring behavior"""

    def test_initial_state(self):
        """verifies initial set state"""
        set_obj = Set("Player One", "Player Two")
        assert set_obj.score_display() == "0-0"
        assert set_obj.winner is None
        assert set_obj.games.player_one == 0
        assert set_obj.games.player_two == 0

    def test_game_scoring(self):
        """verifies game scoring within set"""
        set_obj = Set("Player One", "Player Two")
        for _ in range(4):
            set_obj.record_point(PLAYER_ONE)
        assert set_obj.score_display() == "1-0"
        assert set_obj.games.player_one == 1
        assert set_obj.games.player_two == 0

    def test_set_completion(self):
        """verifies set completion with standard win"""
        set_obj = Set("Player One", "Player Two")
        for _ in range(24):
            set_obj.record_point(PLAYER_ONE)
        assert set_obj.winner == "Player One"
        assert set_obj.games.player_one == 6
        assert set_obj.games.player_two == 0

    def test_extended_set_completion(self):
        """verifies set completion with close score"""
        set_obj = Set("Player One", "Player Two")
        # First player gets to 5 games
        for _ in range(20):
            set_obj.record_point(PLAYER_ONE)
        # Second player gets to 5 games
        for _ in range(20):
            set_obj.record_point(PLAYER_TWO)
        # First player gets to 6 games and wins
        for _ in range(4):
            set_obj.record_point(PLAYER_ONE)
        assert set_obj.winner == "Player One"
        assert set_obj.games.player_one == 6
        assert set_obj.games.player_two == 5

    def test_record_point_after_completion(self):
        """verifies point recording after set completion"""
        set_obj = Set("Player One", "Player Two")
        for _ in range(24):
            set_obj.record_point(PLAYER_ONE)
        set_obj.record_point(PLAYER_ONE)
        assert set_obj.games.player_one == 6
        assert set_obj.games.player_two == 0

    def test_game_in_progress_score(self):
        """verifies score display during game"""
        set_obj = Set("Player One", "Player Two")
        set_obj.record_point(PLAYER_ONE)
        assert "15-0" in set_obj.current_game.score_display()
        assert set_obj.score_display() == "0-0"
