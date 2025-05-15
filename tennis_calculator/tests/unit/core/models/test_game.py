"""verifies game scoring functionality"""

import pytest
from tennis_calculator.core.models.game import Game
from tennis_calculator.core.rules import (
    PLAYER_ONE,
    PLAYER_TWO,
    POINT_NAMES,
    DEUCE,
    ADVANTAGE,
    GAME,
)
from tennis_calculator.core.exceptions import InvalidPlayerNumberException


class TestGame:
    """validates game scoring behavior"""

    def test_initial_state(self):
        """verifies initial game state"""
        game = Game("Player One", "Player Two")
        assert game.score_display() == "0-0"
        assert not game.winner
        assert game.points.player_one == 0
        assert game.points.player_two == 0

    def test_record_point(self):
        """verifies point recording"""
        game = Game("Player One", "Player Two")
        game.record_point(PLAYER_ONE)
        assert game.score_display() == "15-0"
        assert game.points.player_one == 1
        assert game.points.player_two == 0

    def test_deuce(self):
        """verifies deuce scoring"""
        game = Game("Player One", "Player Two")
        for _ in range(3):
            game.record_point(PLAYER_ONE)
            game.record_point(PLAYER_TWO)
        assert game.score_display() == DEUCE

    def test_advantage(self):
        """verifies advantage scoring"""
        game = Game("Player One", "Player Two")
        for _ in range(3):
            game.record_point(PLAYER_ONE)
            game.record_point(PLAYER_TWO)
        game.record_point(PLAYER_ONE)
        assert game.score_display() == f"{ADVANTAGE} Player One"

    def test_win_from_advantage(self):
        """verifies winning from advantage"""
        game = Game("Player One", "Player Two")
        for _ in range(3):
            game.record_point(PLAYER_ONE)
            game.record_point(PLAYER_TWO)
        game.record_point(PLAYER_ONE)
        game.record_point(PLAYER_ONE)
        assert game.score_display() == GAME
        assert game.winner == "Player One"

    def test_back_to_deuce(self):
        """verifies returning to deuce from advantage"""
        game = Game("Player One", "Player Two")
        for _ in range(3):
            game.record_point(PLAYER_ONE)
            game.record_point(PLAYER_TWO)
        game.record_point(PLAYER_ONE)
        game.record_point(PLAYER_TWO)
        assert game.score_display() == DEUCE

    def test_normal_win(self):
        """verifies normal game win without deuce"""
        game = Game("Player One", "Player Two")
        for _ in range(4):
            game.record_point(PLAYER_ONE)
        assert game.score_display() == GAME
        assert game.winner == "Player One"

    def test_record_after_win(self):
        """verifies point recording after game completion"""
        game = Game("Player One", "Player Two")
        for _ in range(4):
            game.record_point(PLAYER_ONE)
        game.record_point(PLAYER_TWO)
        assert game.score_display() == GAME
        assert game.winner == "Player One"

    def test_invalid_player_number(self):
        """verifies invalid player number handling"""
        game = Game("Player One", "Player Two")
        with pytest.raises(InvalidPlayerNumberException):
            game.record_point(3)
