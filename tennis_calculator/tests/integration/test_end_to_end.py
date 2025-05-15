"""verifies end to end functionality"""

import pytest
from tennis_calculator.core.processors.match_processor import MatchProcessor
from tennis_calculator.core.processors.query_processor import QueryProcessor


def test_full_tournament_flow():
    """Test full tournament flow from match processing to querying."""
    # Setup processors
    match_processor = MatchProcessor()
    query_processor = QueryProcessor(match_processor)

    # Process matches
    match_data = [
        "Match: 01",
        "Player One vs Player Two",
        # First set - Player One wins 6-0
        "0",
        "0",
        "0",
        "0",  # Game 1
        "0",
        "0",
        "0",
        "0",  # Game 2
        "0",
        "0",
        "0",
        "0",  # Game 3
        "0",
        "0",
        "0",
        "0",  # Game 4
        "0",
        "0",
        "0",
        "0",  # Game 5
        "0",
        "0",
        "0",
        "0",  # Game 6
        # Second set - Player One wins 6-0
        "0",
        "0",
        "0",
        "0",  # Game 1
        "0",
        "0",
        "0",
        "0",  # Game 2
        "0",
        "0",
        "0",
        "0",  # Game 3
        "0",
        "0",
        "0",
        "0",  # Game 4
        "0",
        "0",
        "0",
        "0",  # Game 5
        "0",
        "0",
        "0",
        "0",  # Game 6
    ]
    match_processor.process_matches(match_data)

    # Query match scores
    score_query = "Score Match 01"
    result = query_processor.handle_query(score_query)
    assert "Player One defeated Player Two" in result
    assert "2 sets to 0" in result

    # Query player games
    games_query = "Games Player Player Two"
    result = query_processor.handle_query(games_query)
    won, lost = map(int, result.split())
    assert won == 0
    assert lost == 12


def test_tournament_edge_cases():
    """Test tournament edge cases."""
    match_processor = MatchProcessor()
    query_processor = QueryProcessor(match_processor)

    # Invalid match data
    with pytest.raises(Exception):
        match_processor.process_matches(["Invalid data"])

    # Invalid query
    with pytest.raises(Exception):
        query_processor.handle_query("Invalid query")


def test_process_and_query_match(processors, sample_match_data):
    """Test processing a match and querying its result."""
    match_processor, query_processor = processors

    # Process match with complete set
    complete_match_data = [
        "Match: 01",
        "Player One vs Player Two",
        # First set - Player One wins 6-0
        "0",
        "0",
        "0",
        "0",  # Game 1
        "0",
        "0",
        "0",
        "0",  # Game 2
        "0",
        "0",
        "0",
        "0",  # Game 3
        "0",
        "0",
        "0",
        "0",  # Game 4
        "0",
        "0",
        "0",
        "0",  # Game 5
        "0",
        "0",
        "0",
        "0",  # Game 6
        # Second set - Player One wins 6-0
        "0",
        "0",
        "0",
        "0",  # Game 1
        "0",
        "0",
        "0",
        "0",  # Game 2
        "0",
        "0",
        "0",
        "0",  # Game 3
        "0",
        "0",
        "0",
        "0",  # Game 4
        "0",
        "0",
        "0",
        "0",  # Game 5
        "0",
        "0",
        "0",
        "0",  # Game 6
    ]
    match_processor.process_matches(complete_match_data)

    # Query match score
    score_query = "Score Match 01"
    result = query_processor.handle_query(score_query)
    assert "Player One defeated Player Two" in result
    assert "2 sets to 0" in result

    # Query player games
    games_query = "Games Player Player One"
    result = query_processor.handle_query(games_query)
    won, lost = map(int, result.split())
    assert won == 12
    assert lost == 0


def test_process_invalid_match():
    """verifies invalid match data handling"""
    match_processor = MatchProcessor()
    with pytest.raises(Exception):
        match_processor.process_matches(["Invalid match data"])


def test_full_tournament_file():
    """Test processing the full tournament file and verifying all requirements."""
    match_processor = MatchProcessor()
    query_processor = QueryProcessor(match_processor)

    # Read and process full tournament file
    with open("tennis_calculator/tests/test_data/full_tournament.txt", "r") as file:
        match_data = file.readlines()
    match_processor.process_matches(match_data)

    # Test Match 02 score (Person C defeated Person A)
    result = query_processor.handle_query("Score Match 02")
    assert "Person C defeated Person A" in result
    assert "2 sets to 0" in result

    # Test Person A's games
    result = query_processor.handle_query("Games Player Person A")
    won, lost = map(int, result.split())
    assert won == 17  # Verify exact number from example
    assert lost == 12  # Verify exact number from example

    # Verify Match 01 (Person A vs Person B)
    result = query_processor.handle_query("Score Match 01")
    assert "Person A" in result
    assert "Person B" in result

    # Verify game completion resets
    match = match_processor.get_match("02")
    assert match.current_set is None  # Match should be completed
    assert match.winner is not None  # Should have a winner
    assert (
        match.sets_score.player_one + match.sets_score.player_two == 2
    )  # Match ended in straight sets

    # Verify set completion (first to 6 games wins)
    for completed_set in match.completed_sets:
        max_games = max(completed_set.games.player_one, completed_set.games.player_two)
        assert max_games >= 6  # Winner must have at least 6 games
        assert (
            completed_set.winner is not None
        )  # Each completed set should have a winner
