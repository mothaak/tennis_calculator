"""Tennis Calculator Package

A package for calculating tennis match scores and statistics.
"""

__version__ = "1.0.0"

from tennis_calculator.core.processors.match_processor import MatchProcessor
from tennis_calculator.core.processors.query_processor import QueryProcessor
from tennis_calculator.core.models.game import Game
from tennis_calculator.core.models.set import Set
from tennis_calculator.core.models.match import Match
from tennis_calculator.core.exceptions import (
    InvalidMatchFormatException,
    MatchNotFoundException,
    MatchCompletedException,
    PlayerNotFoundException,
    InvalidQueryException,
    DuplicateMatchException,
    InvalidPlayerNumberException,
)

__all__ = [
    "MatchProcessor",
    "QueryProcessor",
    "Game",
    "Set",
    "Match",
    "InvalidMatchFormatException",
    "MatchNotFoundException",
    "MatchCompletedException",
    "PlayerNotFoundException",
    "InvalidQueryException",
    "DuplicateMatchException",
    "InvalidPlayerNumberException",
]
