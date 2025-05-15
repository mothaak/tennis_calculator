"""handles tennis tournament management and scoring"""

from typing import Dict, List, Optional, Tuple
from tennis_calculator.core.rules import MATCH_NOT_STARTED
from tennis_calculator.core.exceptions import (
    MatchNotFoundException,
    PlayerNotFoundException,
    DuplicateMatchException,
)
from tennis_calculator.core.models.match import Match


class Tournament:
    """represents a tennis tournament with match tracking"""

    def __init__(self) -> None:
        """initializes tournament"""
        self.matches: Dict[str, Match] = {}

    def __getstate__(self):
        """Return state for pickling."""
        return self.matches

    def __setstate__(self, state):
        """Set state when unpickling."""
        self.matches = state

    def add_match(self, match: Match, overwrite: bool = False) -> None:
        """adds match to tournament

        Args:
            match: Match object to add
            overwrite: If True, overwrites existing match with same ID
        """
        if match.match_id in self.matches and not overwrite:
            raise DuplicateMatchException(f"Match {match.match_id} already exists")
        self.matches[match.match_id] = match

    def get_match(self, match_id: str) -> Match:
        """retrieves match by id"""
        if match_id not in self.matches:
            raise MatchNotFoundException(f"Match {match_id} not found")
        return self.matches[match_id]

    def record_match_point(self, match_id: str, player_number: int) -> None:
        """records point for a player in specified match"""
        match = self.get_match(match_id)
        match.record_point(player_number)

    def get_player_games(self, player_name: str) -> Tuple[int, int]:
        """retrieves total games won and lost for player"""
        if not any(
            player_name in (match.player_one, match.player_two)
            for match in self.matches.values()
        ):
            raise PlayerNotFoundException(f"Player {player_name} not found")

        total_won = 0
        total_lost = 0
        for match in self.matches.values():
            if player_name in (match.player_one, match.player_two):
                won, lost = match.games_summary(player_name)
                total_won += won
                total_lost += lost

        return total_won, total_lost

    def get_match_score(self, match_id: str) -> str:
        """retrieves formatted score for match"""
        match = self.get_match(match_id)
        if match._is_not_started_display():
            return MATCH_NOT_STARTED
        return match.score_display()

    def get_player_matches(self, player_name: str) -> List[Match]:
        """retrieves all matches for player"""
        matches = [
            match
            for match in self.matches.values()
            if player_name in (match.player_one, match.player_two)
        ]
        if not matches:
            raise PlayerNotFoundException(f"Player {player_name} not found")
        return matches
