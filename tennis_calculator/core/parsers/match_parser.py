"""Parser for tennis match input."""

import re
from dataclasses import dataclass
from typing import List, Optional, Tuple
from tennis_calculator.core.rules import (
    PLAYER_ONE,
    PLAYER_TWO,
    POINT_VALUE_PLAYER_ONE,
    POINT_VALUE_PLAYER_TWO,
)
from tennis_calculator.core.exceptions import InvalidMatchFormatException
from tennis_calculator.core.models.match import Match


@dataclass
class MatchData:
    """Class representing parsed match data."""

    match_id: str
    player_one: str
    player_two: str
    points: List[int]


class MatchParser:
    """Parser for tennis match input."""

    MATCH_ID_PATTERN = r"^Match: (\w+)$"
    PLAYERS_PATTERN = r"^(.+) vs (.+)$"

    @classmethod
    def parse_match_details(cls, lines: List[str]) -> tuple[str, str, str]:
        """Parse match details from input lines.

        Args:
            lines: List of input lines.

        Returns:
            Tuple containing match_id, player_one, and player_two.

        Raises:
            InvalidMatchFormatException: If input format is invalid.
        """
        if len(lines) < 2:
            raise InvalidMatchFormatException("Match data must have at least 2 lines")

        # Parse match ID
        match_id_line = lines[0].strip()
        if not match_id_line.startswith("Match: "):
            raise InvalidMatchFormatException("First line must start with 'Match: '")
        match_id = match_id_line[7:].strip()

        # Parse player names
        players_line = lines[1].strip()
        if " vs " not in players_line:
            raise InvalidMatchFormatException("Second line must contain ' vs '")
        player_one, player_two = players_line.split(" vs ")

        return match_id, player_one, player_two

    @classmethod
    def parse_points(cls, lines: List[str]) -> List[int]:
        """Parse point values from input lines.

        Args:
            lines: List of input lines.

        Returns:
            List of point values.

        Raises:
            InvalidMatchFormatException: If point format is invalid.
        """
        points = []
        for line in lines[2:]:  # Skip match ID and player lines
            line = line.strip()
            if not line:  # Skip empty lines
                continue
            if line not in (str(POINT_VALUE_PLAYER_ONE), str(POINT_VALUE_PLAYER_TWO)):
                raise InvalidMatchFormatException(
                    f"Invalid point value: {line}. Must be {POINT_VALUE_PLAYER_ONE} or {POINT_VALUE_PLAYER_TWO}"
                )
            points.append(
                PLAYER_ONE if line == str(POINT_VALUE_PLAYER_ONE) else PLAYER_TWO
            )
        return points

    @classmethod
    def create_match(cls, lines: List[str]) -> Match:
        """Create a Match object from input lines.

        Args:
            lines: List of input lines.

        Returns:
            Match object.

        Raises:
            InvalidMatchFormatException: If match format is invalid.
        """
        match_id, player_one, player_two = cls.parse_match_details(lines)
        match = Match(match_id, player_one, player_two)

        points = cls.parse_points(lines)
        for point in points:
            try:
                match.record_point(point)  # Points are already mapped to 1 or 2
            except Exception:  # Stop processing points if match is complete
                break

        return match
