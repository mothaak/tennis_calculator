from typing import Any, Tuple


class QueryProcessor:
    def __init__(self, match_processor: Any) -> None:
        self.match_processor = match_processor

    def handle_query(self, query: str) -> str:
        try:
            command, entity, identifier = self._parse_query(query)
        except ValueError:
            return "Invalid query"

        if command == 'score' and entity == 'match':
            return self._get_match_score(identifier)
        elif command == 'games' and entity == 'player':
            return self._get_player_games(identifier)

        return "Invalid query"

    def _parse_query(self, query: str) -> Tuple[str, str, str]:
        parts = query.split()
        if len(parts) < 3:
            raise ValueError("Invalid query")

        command = parts[0].lower()
        entity = parts[1].lower()
        identifier = ' '.join(parts[2:])

        return command, entity, identifier

    def _get_match_score(self, match_id: str) -> str:
        match = self.match_processor.get_match(match_id)
        if match is None:
            return f"Match {match_id} not found"
        if match:
            if 'winner' in match and 'loser' in match:
                winner_sets, loser_sets = match['result']
                if match['winner'] == match['player2']:
                    winner_sets, loser_sets = loser_sets, winner_sets
                return f"{match['winner']} defeated {match['loser']} \n{winner_sets} sets to {loser_sets}"
            else:
                return "Match data incomplete"

    def _get_player_games(self, player_name: str) -> str:
        games_won, games_lost = self._calculate_player_games(player_name)
        if games_won is None and games_lost is None:
            return f"Player {player_name} not found"

        return f"{games_won} {games_lost}"

    def _calculate_player_games(self, player_name: str) -> Tuple[int, int]:
        games_won, games_lost = 0, 0
        player_found = False

        for match in self.match_processor.matches:
            player1_points, player2_points = 0, 0
            player1_games, player2_games = 0, 0

            for point in match['points']:
                if point == 0:
                    player1_points += 1
                else:
                    player2_points += 1

                if (player1_points >= 4 and player1_points - player2_points >= 2) or \
                   (player2_points >= 4 and player2_points - player1_points >= 2):
                    if player1_points > player2_points:
                        player1_games += 1
                    else:
                        player2_games += 1
                    player1_points, player2_points = 0, 0

            if match['player1'] == player_name:
                player_found = True
                games_won += player1_games
                games_lost += player2_games
            elif match['player2'] == player_name:
                player_found = True
                games_won += player2_games
                games_lost += player1_games

        if not player_found:
            return None, None

        return games_won, games_lost
