# test_query_processor.py
import unittest
from unittest.mock import patch
from match_processor import MatchProcessor
from query_processor import QueryProcessor
import os

class TestQueryProcessor(unittest.TestCase):
    def setUp(self):
        self.match_processor = MatchProcessor()
        self.query_processor = QueryProcessor(self.match_processor)
        file_path = os.path.join(os.path.dirname(__file__), 'test_data/full_tournament.txt')
        with open(file_path, 'r') as file:
            lines = file.readlines()
        self.match_processor.process_matches(lines)
        self.match_processor.calculate_results()

    def test_score_match_01(self):
        result = self.query_processor.handle_query("Score Match 01")
        self.assertEqual(result, "Person A defeated Person B \n2 sets to 0")

    def test_score_match_02(self):
        result = self.query_processor.handle_query("Score Match 02")
        self.assertEqual(result, "Person C defeated Person A \n2 sets to 1")

    def test_games_player_person_a(self):
        result = self.query_processor.handle_query("Games Player Person A")
        self.assertEqual(result, "23 17")

    def test_games_player_person_b(self):
        result = self.query_processor.handle_query("Games Player Person B")
        self.assertEqual(result, "0 12")

    def test_games_player_person_c(self):
        result = self.query_processor.handle_query("Games Player Person C")
        self.assertEqual(result, "17 11")

    def test_invalid_query(self):
        result = self.query_processor.handle_query("Invalid Query")
        self.assertEqual(result, "Invalid query")

    def test_score_match_not_found(self):
        result = self.query_processor.handle_query("Score Match 99")
        self.assertEqual(result, "Match 99 not found")

    def test_games_player_not_found(self):
        result = self.query_processor.handle_query("Games Player Person X")
        self.assertEqual(result, "Player Person X not found")

if __name__ == "__main__":
    unittest.main()