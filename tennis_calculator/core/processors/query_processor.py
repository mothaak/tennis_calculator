"""handles tennis query processing"""

from typing import Optional, Tuple
from tennis_calculator.core.processors.match_processor import MatchProcessor
from tennis_calculator.core.exceptions import (
    InvalidQueryException,
    MatchNotFoundException,
    PlayerNotFoundException,
)


class QueryProcessor:
    """processes tennis match queries"""

    def __init__(self, match_processor: MatchProcessor) -> None:
        """initializes query processor"""
        self.match_processor = match_processor

    def handle_query(self, query: str) -> str:
        """processes query and returns result"""
        parts = query.strip().split()
        if len(parts) < 3:
            raise InvalidQueryException("Invalid query format")

        query_type = parts[0].lower()
        if query_type == "score":
            if parts[1].lower() != "match":
                raise InvalidQueryException("Invalid score query format")
            return self._handle_score_query(parts[2])
        elif query_type == "games":
            if parts[1].lower() != "player":
                raise InvalidQueryException("Invalid games query format")
            return self._handle_games_query(" ".join(parts[2:]))
        else:
            raise InvalidQueryException("Unknown query type")

    def _handle_score_query(self, match_id: str) -> str:
        """handles score query"""
        match = self.match_processor.get_match(match_id)
        if not match.winner:
            return match.score_display()

        loser = match.get_loser()
        winner_sets = (
            match.sets_score.player_one
            if match.winner == match.player_one
            else match.sets_score.player_two
        )
        loser_sets = (
            match.sets_score.player_two
            if match.winner == match.player_one
            else match.sets_score.player_one
        )

        return f"{match.winner} defeated {loser}\n{winner_sets} sets to {loser_sets}"

    def _handle_games_query(self, player_name: str) -> str:
        """handles games query"""
        won, lost = self.match_processor.tournament.get_player_games(player_name)
        return f"{won} {lost}"
