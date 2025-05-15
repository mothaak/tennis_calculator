"""handles tennis set scoring and state management"""

from dataclasses import dataclass, field
from typing import Optional
from tennis_calculator.core.rules import (
    GAMES_TO_WIN_SET,
    GAMES_FOR_TIEBREAK,
    POINTS_TO_WIN_TIEBREAK,
    PLAYER_ONE,
    PLAYER_TWO,
)
from tennis_calculator.core.models.game import Game
from tennis_calculator.core.models.points import PlayerPoints


@dataclass
class Set:
    """represents a tennis set with scoring and state tracking"""

    player_one: str
    player_two: str
    current_game: Game = field(init=False)
    games: PlayerPoints = field(init=False, default_factory=PlayerPoints)
    winner: Optional[str] = field(init=False, default=None)
    is_tiebreak: bool = False

    def __post_init__(self) -> None:
        """initializes set with first game"""
        self.current_game = Game(self.player_one, self.player_two)

    def __getstate__(self):
        """Return state for pickling."""
        return {
            'player_one': self.player_one,
            'player_two': self.player_two,
            'current_game': self.current_game,
            'games': self.games,
            'winner': self.winner,
            'is_tiebreak': self.is_tiebreak
        }

    def __setstate__(self, state):
        """Set state when unpickling."""
        self.player_one = state['player_one']
        self.player_two = state['player_two']
        self.current_game = state['current_game']
        self.games = state['games']
        self.winner = state['winner']
        self.is_tiebreak = state['is_tiebreak']

    def record_point(self, player_number: int) -> None:
        """records point for a player and updates set state"""
        if self.winner:
            return

        self.current_game.record_point(player_number)
        if self.current_game.winner:
            self._handle_game_completion()

    def _handle_game_completion(self) -> None:
        """processes game completion and updates set state"""
        if not self.current_game.winner:
            return

        winner_number = (
            PLAYER_ONE if self.current_game.winner == self.player_one else PLAYER_TWO
        )
        self.games.add_point(winner_number == PLAYER_ONE)

        if self._has_winner():
            self.winner = self.current_game.winner
        else:
            self._start_next_game()

    def _has_winner(self) -> bool:
        """checks if current games state indicates a winner"""
        if self.is_tiebreak:
            return self.current_game.winner is not None

        # First to 6 games wins the set
        if self.games.player_one >= GAMES_TO_WIN_SET:
            return True
        if self.games.player_two >= GAMES_TO_WIN_SET:
            return True
        return False

    def _start_next_game(self) -> None:
        """creates new game and checks for tiebreak"""
        if (
            self.games.player_one == GAMES_FOR_TIEBREAK
            and self.games.player_two == GAMES_FOR_TIEBREAK
        ):
            self.is_tiebreak = True
            self.current_game = TiebreakGame(self.player_one, self.player_two)
        else:
            self.current_game = Game(self.player_one, self.player_two)

    def score_display(self) -> str:
        """generates formatted score display"""
        return f"{self.games.player_one}-{self.games.player_two}"


class TiebreakGame(Game):
    """represents a tiebreak game in tennis"""

    def _has_winner(self) -> bool:
        """checks if current points state indicates a winner"""
        points_diff = abs(self.points.player_one - self.points.player_two)
        max_points = max(self.points.player_one, self.points.player_two)
        return max_points >= POINTS_TO_WIN_TIEBREAK and points_diff >= 2

    def score_display(self) -> str:
        """generates formatted score display"""
        if self.winner:
            return "Game"
        return f"{self.points.player_one}-{self.points.player_two}"
