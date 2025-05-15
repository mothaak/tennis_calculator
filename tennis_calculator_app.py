#!/usr/bin/env python3

import sys
import os
from typing import List
from match_processor import MatchProcessor
from query_processor import QueryProcessor


def main(input_file_path: str, test_mode: bool = False) -> None:
    """
    Main function to process the input file and handle user queries.

    Args:
        input_file_path (str): Path to the input file.
        test_mode (bool): Whether the script is running in test mode or not.
    """
    if not os.path.isfile(input_file_path) or not input_file_path.endswith('.txt'):
        print("Error: The input file must be a readable .txt file.")
        return

    if os.path.getsize(input_file_path) == 0:
        print("Error: The input file is empty.")
        return

    match_processor = MatchProcessor()
    query_processor = QueryProcessor(match_processor)

    try:
        with open(input_file_path, 'r') as file:
            lines: List[str] = file.readlines()
            if not lines:
                print("Error: The input file is empty.")
                return
            match_processor.process_matches(lines)
            match_processor.calculate_results()
    except (IOError, OSError) as exception:
        print(f"Error: Unable to read the file. {exception}")
        return
    except Exception as exception:
        print(f"An unexpected error occurred: {exception}")
        return

    def print_welcome_message():
        print("\n######## Welcome to the Tennis Calculator! ########\n")
        print("Instructions:")
        print("1. To query match result, type: Score Match <id>")
        print("   Example: Score Match 01")
        print("2. To query games for a player, type: Games Player <Player Name>")
        print("   Example: Games Player Person A")
        print("3. To exit the application, type: exit\n")

    def handle_interactive_mode():
        while True:
            query = input("Enter your query (or type 'exit' to quit): ").strip()
            if query.lower() == 'exit':
                break
            result = query_processor.handle_query(query)
            print(result)

    def handle_script_mode():
        for query in sys.stdin:
            query = query.strip()
            if query.lower() == 'exit':
                break
            result = query_processor.handle_query(query)
            print(result)

    if not test_mode:
        print_welcome_message()
    if sys.stdin.isatty():
        handle_interactive_mode()
    else:
        handle_script_mode()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 tennis_calculator_app.py <input_file>")
    else:
        main(sys.argv[1])

