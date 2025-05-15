"""handles tennis match processing"""

from tennis_calculator.core.models.tournament import Tournament
from tennis_calculator.core.parsers.match_parser import MatchParser
from tennis_calculator.core.exceptions import InvalidMatchDataException


class MatchProcessor:
    """processes tennis matches"""

    def __init__(self) -> None:
        """initializes match processor"""
        self.tournament = Tournament()

    def process_matches(self, match_lines: list[str], overwrite: bool = True) -> None:
        """processes match data and updates tournament state

        Args:
            match_lines: List of lines containing match data
            overwrite: If True, overwrites existing matches with same ID
        """
        if not match_lines:
            raise InvalidMatchDataException("No match data provided")

        current_match_lines = []
        for line in match_lines:
            line = line.strip()
            if not line:  # Skip empty lines
                continue
            if line.startswith("Match:"):  # New match starts
                if current_match_lines:  # Process previous match if exists
                    self._process_match(current_match_lines, overwrite)
                current_match_lines = [line]
            else:
                current_match_lines.append(line)

        # Process last match
        if current_match_lines:
            self._process_match(current_match_lines, overwrite)

    def _process_match(self, match_lines: list[str], overwrite: bool = True) -> None:
        """processes single match data"""
        if not match_lines:
            raise InvalidMatchDataException("Empty match data")

        match = MatchParser.create_match(match_lines)
        self.tournament.add_match(match, overwrite)

    def get_match(self, match_id: str):
        """gets match by id"""
        return self.tournament.get_match(match_id)
