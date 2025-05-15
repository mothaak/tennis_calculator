"""handles tennis game scoring and state management"""

from dataclasses import dataclass, field
from typing import Optional
from tennis_calculator.core.rules import (
    PLAYER_ONE,
    PLAYER_TWO,
    POINTS_TO_WIN_GAME,
    POINTS_LEAD_TO_WIN,
    POINTS_FOR_DEUCE,
    DEUCE,
    ADVANTAGE,
    GAME,
    POINT_NAMES,
)
from tennis_calculator.core.models.points import PlayerPoints
from tennis_calculator.core.exceptions import InvalidPlayerNumberException


@dataclass
class Game:
    """represents a tennis game with scoring and state tracking"""

    player_one: str
    player_two: str
    points: PlayerPoints = field(init=False, default_factory=PlayerPoints)
    winner: Optional[str] = field(init=False, default=None)

    def __getstate__(self):
        """Return state for pickling."""
        return {
            'player_one': self.player_one,
            'player_two': self.player_two,
            'points': self.points,
            'winner': self.winner
        }

    def __setstate__(self, state):
        """Set state when unpickling."""
        self.player_one = state['player_one']
        self.player_two = state['player_two']
        self.points = state['points']
        self.winner = state['winner']

    def record_point(self, player_number: int) -> None:
        """records point for a player and updates game state"""
        if player_number not in (PLAYER_ONE, PLAYER_TWO):
            raise InvalidPlayerNumberException(
                f"Invalid player number: {player_number}"
            )

        if self.winner:
            return

        self.points.add_point(player_number == PLAYER_ONE)
        if self._has_winner():
            self.winner = (
                self.player_one
                if self.points.player_one > self.points.player_two
                else self.player_two
            )

    def _has_winner(self) -> bool:
        """checks if current points state indicates a winner"""
        points_diff = abs(self.points.player_one - self.points.player_two)
        max_points = max(self.points.player_one, self.points.player_two)

        if max_points < POINTS_TO_WIN_GAME:
            return False

        if max_points >= POINTS_FOR_DEUCE:
            return points_diff >= POINTS_LEAD_TO_WIN

        return points_diff >= POINTS_LEAD_TO_WIN

    def score_display(self) -> str:
        """generates formatted score display"""
        if self.winner:
            return GAME

        if self._is_deuce():
            return DEUCE

        if self._is_advantage():
            leader = (
                self.player_one
                if self.points.player_one > self.points.player_two
                else self.player_two
            )
            return f"{ADVANTAGE} {leader}"

        return f"{POINT_NAMES[self.points.player_one]}-{POINT_NAMES[self.points.player_two]}"

    def _is_deuce(self) -> bool:
        """checks if game is in deuce state"""
        return (
            self.points.player_one >= POINTS_FOR_DEUCE
            and self.points.player_two >= POINTS_FOR_DEUCE
            and self.points.player_one == self.points.player_two
        )

    def _is_advantage(self) -> bool:
        """checks if game is in advantage state"""
        return (
            self.points.player_one >= POINTS_FOR_DEUCE
            and self.points.player_two >= POINTS_FOR_DEUCE
            and abs(self.points.player_one - self.points.player_two) == 1
        )

    def get_winner(self) -> Optional[str]:
        """Get the winner of this game.

        Returns:
            The player name of the winner, None if game not complete.
        """
        return self.winner
