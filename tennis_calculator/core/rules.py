"""Tennis scoring rules and constants."""

# Player identifiers
PLAYER_ONE = 1
PLAYER_TWO = 2

# Point values in input file (0 for player one, 1 for player two)
POINT_VALUE_PLAYER_ONE = 0
POINT_VALUE_PLAYER_TWO = 1

# Point scoring names
POINT_NAMES = {0: "0", 1: "15", 2: "30", 3: "40"}

# Game rules
POINTS_TO_WIN_GAME = 4
POINTS_LEAD_TO_WIN = 2
POINTS_FOR_DEUCE = 3

# Set rules
GAMES_TO_WIN_SET = 6
GAMES_FOR_TIEBREAK = 6
GAMES_IN_TIEBREAK_WIN = 7
GAMES_IN_TIEBREAK_LOSS = 6
POINTS_TO_WIN_TIEBREAK = 7

# Match rules
SETS_TO_WIN_MATCH = 2
POINTS_PER_GAME = 4
GAMES_PER_SET = 6

# Display strings
DEUCE = "Deuce"
ADVANTAGE = "Advantage"
GAME = "Game"
MATCH_NOT_STARTED = "Match not started"
