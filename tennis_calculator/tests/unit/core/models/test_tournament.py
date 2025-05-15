"""Unit tests for Tournament model."""

import pytest
from tennis_calculator.core.models.tournament import Tournament
from tennis_calculator.core.models.match import Match
from tennis_calculator.core.rules import MATCH_NOT_STARTED
from tennis_calculator.core.exceptions import (
    MatchNotFoundException,
    PlayerNotFoundException,
    DuplicateMatchException,
)


class TestTournament:
    """Tests for Tournament model."""

    def test_initial_state(self):
        """Test initial tournament state."""
        tournament = Tournament()
        assert not tournament.matches

    def test_add_match(self):
        """Test adding a match."""
        tournament = Tournament()
        match = Match("01", "Player One", "Player Two")
        tournament.add_match(match)
        assert tournament.get_match("01") == match

    def test_add_duplicate_match(self):
        """Test adding a duplicate match."""
        tournament = Tournament()
        match1 = Match("01", "Player One", "Player Two")
        match2 = Match("01", "Player Three", "Player Four")
        tournament.add_match(match1)
        with pytest.raises(DuplicateMatchException):
            tournament.add_match(match2)

    def test_get_match_not_found(self):
        """Test getting a non-existent match."""
        tournament = Tournament()
        with pytest.raises(MatchNotFoundException):
            tournament.get_match("99")

    def test_get_match_score_not_found(self):
        """Test getting score for non-existent match."""
        tournament = Tournament()
        with pytest.raises(MatchNotFoundException):
            tournament.get_match_score("99")

    def test_get_match_score_not_started(self):
        """Test getting score for not started match."""
        tournament = Tournament()
        match = Match("01", "Player One", "Player Two")
        tournament.add_match(match)
        score = tournament.get_match_score("01")
        assert MATCH_NOT_STARTED in score

    def test_get_player_games_not_found(self):
        """Test getting games for non-existent player."""
        tournament = Tournament()
        with pytest.raises(PlayerNotFoundException):
            tournament.get_player_games("Invalid Player")

    def test_get_player_games(self):
        """Test getting player games."""
        tournament = Tournament()
        match = Match("01", "Player One", "Player Two")
        tournament.add_match(match)
        # Win a game
        for _ in range(4):
            match.record_point(1)  # Player One
        won, lost = tournament.get_player_games("Player One")
        assert won == 1
        assert lost == 0
        won, lost = tournament.get_player_games("Player Two")
        assert won == 0
        assert lost == 1
