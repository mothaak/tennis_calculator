"""handles tennis match scoring and state management"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from tennis_calculator.core.rules import (
    PLAYER_ONE,
    PLAYER_TWO,
    SETS_TO_WIN_MATCH,
    GAME,
    POINT_NAMES,
    MATCH_NOT_STARTED,
)
from tennis_calculator.core.exceptions import (
    PlayerNotFoundException,
    MatchCompletedException,
    InvalidPlayerNumberException,
)
from tennis_calculator.core.models.set import Set
from tennis_calculator.core.models.points import PlayerPoints


@dataclass
class Match:
    """represents a tennis match with scoring and state tracking"""

    match_id: str
    player_one: str
    player_two: str
    current_set: Optional[Set] = field(init=False, default=None)
    completed_sets: List[Set] = field(init=False, default_factory=list)
    winner: Optional[str] = field(init=False, default=None)
    sets_score: PlayerPoints = field(init=False, default_factory=PlayerPoints)
    result: Optional[Tuple[int, int]] = field(init=False, default=None)

    def __post_init__(self) -> None:
        """initializes match with first set"""
        self.current_set = Set(self.player_one, self.player_two)

    def __getstate__(self):
        """Return state for pickling."""
        return {
            'match_id': self.match_id,
            'player_one': self.player_one,
            'player_two': self.player_two,
            'current_set': self.current_set,
            'completed_sets': self.completed_sets,
            'winner': self.winner,
            'sets_score': self.sets_score,
            'result': self.result
        }

    def __setstate__(self, state):
        """Set state when unpickling."""
        self.match_id = state['match_id']
        self.player_one = state['player_one']
        self.player_two = state['player_two']
        self.current_set = state['current_set']
        self.completed_sets = state['completed_sets']
        self.winner = state['winner']
        self.sets_score = state['sets_score']
        self.result = state['result']

    def validate_player_number(self, player_number: int) -> None:
        """validates if player number is valid"""
        if player_number not in (PLAYER_ONE, PLAYER_TWO):
            raise InvalidPlayerNumberException(
                f"Invalid player number: {player_number}"
            )

    def get_player_name(self, player_number: int) -> str:
        """retrieves player name from player number"""
        self.validate_player_number(player_number)
        return self.player_one if player_number == PLAYER_ONE else self.player_two

    def record_point(self, player_number: int) -> None:
        """records point for a player and updates match state"""
        if self.winner:
            raise MatchCompletedException("Cannot record points after match completion")

        self.validate_player_number(player_number)

        if not self.current_set:
            raise MatchCompletedException("Match is already completed")

        self.current_set.record_point(player_number)
        if self.current_set.winner:
            self._handle_set_completion()

    def _handle_set_completion(self) -> None:
        """processes set completion and updates match state"""
        if not self.current_set or not self.current_set.winner:
            return

        winner_number = (
            PLAYER_ONE if self.current_set.winner == self.player_one else PLAYER_TWO
        )
        self.sets_score.add_point(winner_number == PLAYER_ONE)
        self.completed_sets.append(self.current_set)

        if self.sets_score.player_one >= SETS_TO_WIN_MATCH:
            self._complete_match(self.player_one)
        elif self.sets_score.player_two >= SETS_TO_WIN_MATCH:
            self._complete_match(self.player_two)
        else:
            self.current_set = Set(self.player_one, self.player_two)

    def _complete_match(self, winner: str) -> None:
        """finalizes match with winner"""
        self.winner = winner
        self.result = (self.sets_score.player_one, self.sets_score.player_two)
        self.current_set = None

    def _is_not_started_display(self) -> bool:
        """checks if match has any points played"""
        return (
            not self.completed_sets
            and self.current_set is not None
            and self.current_set.games.player_one == 0
            and self.current_set.games.player_two == 0
            and self.current_set.current_game.points.player_one == 0
            and self.current_set.current_game.points.player_two == 0
        )

    def score_display(self) -> str:
        """generates formatted score display"""
        if self._is_not_started_display():
            return "0-0"

        set_scores = [set_obj.score_display() for set_obj in self.completed_sets]

        if self.current_set:
            current_game_score = self.current_set.current_game.score_display()
            current_set_score = self.current_set.score_display()

            if current_game_score == GAME:
                set_scores.append(current_set_score)
            elif (
                current_game_score == POINT_NAMES[0] + "-" + POINT_NAMES[0]
                and current_set_score != "0-0"
            ):
                set_scores.append(current_set_score)
            else:
                set_scores.append(f"{current_set_score} ({current_game_score})")

        return ", ".join(set_scores) or "0-0"

    def is_completed(self) -> bool:
        """checks if match has a winner"""
        return self.winner is not None

    def games_summary(self, player_name: str) -> Tuple[int, int]:
        """returns games won and lost for a player"""
        if player_name not in (self.player_one, self.player_two):
            raise PlayerNotFoundException(f"Player {player_name} not found in match")

        is_player_one = player_name == self.player_one
        completed_won, completed_lost = self._completed_sets_games(is_player_one)
        current_won, current_lost = self._current_set_games(is_player_one)

        return completed_won + current_won, completed_lost + current_lost

    def _completed_sets_games(self, is_player_one: bool) -> Tuple[int, int]:
        """calculates games won and lost in completed sets"""
        won = sum(
            set_obj.games.player_one if is_player_one else set_obj.games.player_two
            for set_obj in self.completed_sets
        )
        lost = sum(
            set_obj.games.player_two if is_player_one else set_obj.games.player_one
            for set_obj in self.completed_sets
        )
        return won, lost

    def _current_set_games(self, is_player_one: bool) -> Tuple[int, int]:
        """calculates games won and lost in current set"""
        if not self.current_set:
            return 0, 0

        if is_player_one:
            return self.current_set.games.player_one, self.current_set.games.player_two
        return self.current_set.games.player_two, self.current_set.games.player_one

    def get_winner(self) -> Optional[str]:
        """retrieves match winner if exists"""
        return self.winner

    def get_loser(self) -> Optional[str]:
        """retrieves match loser if exists"""
        if not self.winner:
            return None
        return self.player_two if self.winner == self.player_one else self.player_one

    def reset(self) -> None:
        """resets match to initial state"""
        self.completed_sets = []
        self.current_set = Set(self.player_one, self.player_two)
        self.sets_score.reset()
        self.winner = None

    def sets_won_by(self, player_number: int) -> int:
        """retrieves number of sets won by player"""
        self.validate_player_number(player_number)
        return (
            self.sets_score.player_one
            if player_number == PLAYER_ONE
            else self.sets_score.player_two
        )
