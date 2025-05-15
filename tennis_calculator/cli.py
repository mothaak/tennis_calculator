#!/usr/bin/env python3
"""Main entry point for tennis calculator application."""

import sys
import os
import argparse
import pickle
from tennis_calculator.core.processors.match_processor import MatchProcessor
from tennis_calculator.core.processors.query_processor import QueryProcessor
from tennis_calculator.core.exceptions import TennisCalculatorException


def main():
    parser = argparse.ArgumentParser(description="Tennis Calculator CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    process_parser = subparsers.add_parser(
        "process", help="Process match input from file"
    )
    process_parser.add_argument(
        "--input", "-i", required=True, help="Path to input file containing match data"
    )

    query_parser = subparsers.add_parser("query", help="Query processed matches")
    query_parser.add_argument(
        "subcommand", choices=["score", "games"], help="Query type: score or games"
    )
    query_parser.add_argument("--id", help="Match ID for score query")
    query_parser.add_argument("--player", help="Player name for games query")

    args = parser.parse_args()

    tournament_file = ".tournament_data"
    match_processor = None

    try:
        if os.path.exists(tournament_file):
            with open(tournament_file, "rb") as f:
                match_processor = pickle.load(f)
        else:
            match_processor = MatchProcessor()

        query_processor = QueryProcessor(match_processor)

        if args.command == "process":
            with open(args.input, "r") as f:
                lines = [line.strip() for line in f if line.strip()]
            match_processor.process_matches(lines)
            with open(tournament_file, "wb") as f:
                pickle.dump(match_processor, f)
            print("Matches processed successfully.")

        elif args.command == "query":
            if args.subcommand == "score":
                if not args.id:
                    parser.error("--id is required for score query")
                result = query_processor.handle_query(f"Score Match {args.id}")
                print(result)
            else:
                if not args.player:
                    parser.error("--player is required for games query")
                result = query_processor.handle_query(f"Games Player {args.player}")
                print(result)

    except TennisCalculatorException as ex:
        print(f"Error: {ex}", file=sys.stderr)
        sys.exit(1)


def validate_input_file(input_file_path: str) -> None:
    """Validates the input file exists and is a valid .txt file.

    Args:
        input_file_path: Path to the input file.

    Raises:
        TennisCalculatorException: If the input file is invalid.
    """
    if not os.path.exists(input_file_path):
        raise TennisCalculatorException("Input file does not exist")
    if not os.path.isfile(input_file_path):
        raise TennisCalculatorException("Input path is not a file")
    if not input_file_path.endswith(".txt"):
        raise TennisCalculatorException("Input file must be a .txt file")
    if os.path.getsize(input_file_path) == 0:
        raise TennisCalculatorException("Input file is empty")


def print_welcome_message() -> None:
    """Prints the welcome message with instructions."""
    print("\n######## Welcome to the Tennis Calculator! ########\n")
    print("Instructions:")
    print("1. To query match result, type: Score Match <id>")
    print("   Example: Score Match 01")
    print("2. To query games for a player, type: Games Player <Player Name>")
    print("   Example: Games Player Person A")
    print("3. To exit the application, type: exit\n")


def handle_queries(query_processor: QueryProcessor, test_mode: bool) -> None:
    """Handles user queries in either interactive or script mode.

    Args:
        query_processor: The query processor to use.
        test_mode: Whether the script is running in test mode or not.
    """
    try:
        # In test mode always use interactive mode to leverage patched input
        if test_mode or sys.stdin.isatty():
            handle_interactive_mode(query_processor)
        else:
            handle_script_mode(query_processor)
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)


def handle_interactive_mode(query_processor: QueryProcessor) -> None:
    """Handles queries in interactive mode.

    Args:
        query_processor: The query processor to use.
    """
    while True:
        query = input("Enter your query (or type 'exit' to quit): ").strip()
        if not _execute_interactive_query(query_processor, query):
            break


def handle_script_mode(query_processor: QueryProcessor) -> None:
    """Handles queries in script mode.

    Args:
        query_processor: The query processor to use.
    """
    for raw_query in sys.stdin:
        if not _execute_script_query(query_processor, raw_query):
            break


def _execute_interactive_query(query_processor: QueryProcessor, query: str) -> bool:
    if not query:
        return True
    if query.lower() == "exit":
        return False
    try:
        print(query_processor.handle_query(query))
    except TennisCalculatorException as exception:
        print(f"Error: {str(exception)}")
    except Exception as exception:
        print(f"An unexpected error occurred: {str(exception)}")
    return True


def _execute_script_query(query_processor: QueryProcessor, raw_query: str) -> bool:
    query = raw_query.strip()
    if not query:
        return True
    if query.lower() == "exit":
        return False
    try:
        print(query_processor.handle_query(query))
    except TennisCalculatorException as exception:
        print(f"Error: {str(exception)}")
        sys.exit(1)
    except Exception as exception:
        print(f"An unexpected error occurred: {str(exception)}")
        sys.exit(1)
    return True


if __name__ == "__main__":
    main()
