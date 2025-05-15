# test_integration.py
import unittest
from unittest.mock import patch
import os
from io import StringIO
from tennis_calculator_app import main

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.input_file_path = os.path.join(os.path.dirname(__file__), 'test_data/full_tournament.txt')

    @patch('os.path.isfile', return_value=False)
    def test_main_invalid_file(self, mock_isfile):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main('invalid_file.txt')
            self.assertIn("Error: The input file must be a readable .txt file.", fake_out.getvalue())

    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getsize', return_value=0)
    def test_main_empty_file(self, mock_getsize, mock_isfile):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main('empty_file.txt')
            self.assertIn("Error: The input file is empty.", fake_out.getvalue())

    def test_main_successful_processing(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('builtins.input', side_effect=['exit']):
                main(self.input_file_path, test_mode=True)
                output = fake_out.getvalue()
                self.assertNotIn("######## Welcome to the Tennis Calculator! ########", output)  # Assuming changes in main to handle this

    def test_query_score_match(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('builtins.input', side_effect=['Score Match 01', 'exit']):
                main(self.input_file_path, test_mode=True)
                output = fake_out.getvalue()
                expected_output = "Person A defeated Person B \n2 sets to 0\n"
                self.assertIn(expected_output, output)

    def test_query_games_player(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('builtins.input', side_effect=['Games Player Person A', 'exit']):
                main(self.input_file_path, test_mode=True)
                output = fake_out.getvalue()
                self.assertIn("23 17", output)
                

if __name__ == "__main__":
    unittest.main()