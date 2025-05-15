import unittest
from match_processor import MatchProcessor

class TestMatchProcessor(unittest.TestCase):
    def setUp(self):
        self.match_processor = MatchProcessor()

    def read_tournament_file(self, filename='tests/test_data/full_tournament.txt'):
        with open(filename) as f:
            return f.readlines()

    def test_full_tournament_processing(self):
        lines = self.read_tournament_file()
        self.match_processor.process_matches(lines)
        self.assertEqual(len(self.match_processor.matches), 2)

    def test_calculate_results(self):
        lines = self.read_tournament_file()
        self.match_processor.process_matches(lines)
        self.match_processor.calculate_results()
        match1 = self.match_processor.matches[0]
        match2 = self.match_processor.matches[1]
        self.assertEqual(match1['result'], (2, 0))
        self.assertEqual(match1['winner'], 'Person A')
        self.assertEqual(match1['loser'], 'Person B')
        self.assertEqual(match2['result'], (1, 2))  # Corrected expected result
        self.assertEqual(match2['winner'], 'Person C')
        self.assertEqual(match2['loser'], 'Person A')

    def test_invalid_point_value(self):
        lines = [
            "Match: 01",
            "Person A vs Person B",
            "0", "0", "0", "0",  # Game 1, Player A wins
            "2",  # Invalid point value (not 0 or 1)
            "0", "0", "0", "0",  # Game 2, Player A wins
        ]
        with self.assertRaises(ValueError):
            self.match_processor.process_matches(lines)

if __name__ == "__main__":
    unittest.main()
