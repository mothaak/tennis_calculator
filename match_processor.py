from typing import List, Dict, Any

class MatchProcessor:
    def __init__(self) -> None:
        self.matches: List[Dict[str, Any]] = []

    def process_matches(self, lines: List[str]) -> None:
        current_match: Dict[str, Any] = {}
        points: List[int] = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith("Match:"):
                if current_match:
                    current_match['points'] = points
                    self.matches.append(current_match)
                current_match = {'id': line.split(":")[1].strip(), 'points': []}
                points = []
            elif " vs " in line:
                players = line.split(" vs ")
                current_match['player1'] = players[0].strip()
                current_match['player2'] = players[1].strip()
            elif line in ("0", "1"):
                points.append(int(line))
            else:
                raise ValueError("Invalid point value")
        if current_match:
            current_match['points'] = points
            self.matches.append(current_match)

    def calculate_results(self) -> None:
        for match in self.matches:
            self._calculate_match_result(match)

    def _calculate_match_result(self, match: Dict[str, Any]) -> None:
        player1_points, player2_points = 0, 0
        player1_games, player2_games = 0, 0
        player1_sets, player2_sets = 0, 0

        for point in match['points']:
            if point == 0:
                player1_points += 1
            else:
                player2_points += 1

            if player1_points >= 4 and (player1_points - player2_points) >= 2:
                player1_games += 1
                player1_points, player2_points = 0, 0
            elif player2_points >= 4 and (player2_points - player1_points) >= 2:
                player2_games += 1
                player2_points, player1_points = 0, 0

            if player1_games == 6:
                player1_sets += 1
                player1_games, player2_games = 0, 0
            elif player2_games == 6:
                player2_sets += 1
                player2_games, player1_games = 0, 0

        match['result'] = (player1_sets, player2_sets)
        if player1_sets > player2_sets:
            match['winner'] = match['player1']
            match['loser'] = match['player2']
        elif player2_sets > player1_sets:
            match['winner'] = match['player2']
            match['loser'] = match['player1']
        else:
            match['winner'] = "Unfinished"
            match['loser'] = "Unfinished"

    def get_match(self, match_id: str) -> Dict[str, Any]:
        for match in self.matches:
            if match['id'] == match_id:
                return match
        return None

