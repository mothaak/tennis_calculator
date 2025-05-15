# Tennis Calculator

The Tennis Calculator takes a set of scores as inputs and produces useful statistics based on those scores.

This calculator uses a simplified version of scoring where whoever gets to 6 games first wins the set.

## Overview

The Tennis Calculator takes inputs in the form of a list of points of a tennis match.

Given this list of points, it will calculate the "games", "sets" and "matches" results.

From there it can be queried about various statistics around the input matches it received.

## Assumptions
 * The input data is assumed to follow the specified format, but the application can handle some formatting inconsistencies and errors gracefully.
 * The maximum number of sets in a match is 3 (best of 3 sets).
 * The calculator focuses on the specific variation of tennis scoring rules described in the requirements, including the tie-break rule.

## Solution Explanation

The solution follows a modular design with clear separation of concerns:

### Core Components

1. Models:
   - `Game`: Handles individual game scoring with deuce and advantage rules
   - `Set`: Manages set scoring and game transitions
   - `Match`: Coordinates sets and overall match state
   - `Tournament`: Manages multiple matches and player statistics
   - `Points`: Tracks point scoring for players

2. Processors:
   - `MatchProcessor`: Processes match input data and manages tournament state
   - `QueryProcessor`: Handles query parsing and result generation

3. Parsers:
   - `MatchParser`: Parses input data into structured match format

4. Rules:
   - Centralized scoring rules and constants
   - Configurable game, set, and match parameters

### Error Handling

- Custom exceptions for various error scenarios
- Graceful handling of invalid inputs
- Comprehensive validation at each level

### Design Principles

- Clear separation of concerns between models and processors
- Immutable state transitions
- Robust error handling
- Comprehensive test coverage

The solution includes extensive test suites:
- Unit tests for all components
- Integration tests for end-to-end scenarios
- Edge case handling verification

## Setup

### Prerequisites

Ensure you have Python 3.6+ installed. You can download it from https://www.python.org/.

### Installation

1. Clone the repository
2. Install dependencies and package in development mode:

```bash
pip3 install -r requirements.txt
pip3 install -e .
```

### Directory Structure

The project structure:

```
.
├── README.md
├── setup.py
├── setup.cfg
├── requirements.txt
├── .flake8
├── runtime.txt
└── tennis_calculator/
    ├── __init__.py
    ├── core/
    │   ├── processors/
    │   │   ├── match_processor.py
    │   │   └── query_processor.py
    │   ├── models/
    │   │   ├── game.py
    │   │   ├── match.py
    │   │   ├── points.py
    │   │   ├── set.py
    │   │   └── tournament.py
    │   ├── parsers/
    │   │   └── match_parser.py
    │   ├── rules.py
    │   └── exceptions.py
    └── tests/
        ├── integration/
        │   └── test_end_to_end.py
        ├── unit/
        │   └── core/
        │       ├── models/
        │       ├── parsers/
        │       └── processors/
        └── test_data/
            ├── test_input.txt
            └── full_tournament.txt
```

### Running the Application

Run the application by specifying the input file:

```bash
python3 -m tennis_calculator.tennis_calculator_app <input_file>
```

### Running the Tests

Run all tests with pytest:

```bash
python3 -m pytest tennis_calculator/tests/ -v
```

For test coverage report:

```bash
python3 -m pytest tennis_calculator/tests/ --cov=tennis_calculator
```

### Code Quality

Run flake8 for code quality checks:

```bash
flake8 .
```

## Input

The input will have some header lines, and then a list of points. 
For example, the following would result in 2 games to "Person A":

```
Match: 01
Person A vs Person B
0
1
0
1
0
0
0
0
0
0
```

The first row is a match ID, the second row shows who is playing against whom.
After that are a series of points, where 0 is a point for the first person listed, and 1 is for the last person.

# Example:

input_data = 
```
Match: 01
Person A vs Person B
0
1
0
1
0
0
0
0
0
0
```

# The corresponding score:
 | Point | Score    |
 |-------|----------|
 | 0     | 15 - 0   |
| 1     | 15 - 15  |
 | 0     | 30 - 15  |
 | 1     | 30 - 30  |
| 0     | 40 - 30  |
 | 0     | Game     |
 | 0     | 15 - 0   |
 | 0     | 30 - 0   |
 | 0     | 40 - 0   |
 | 0     | Game     |

## Queries

 Query match result:
 Query scores for a particular match
Prints who defeated whom, and the result of the sets for the match (winning player score first).

query = 
```
Score Match 01
```
expected_output = 
```
Person A defeated Person B
2 sets to 0
```

Query games for player:
 Prints a summary of games won vs lost for a particular player over the tournament

query = 
```
Games Player Person A
```
expected_output = 
```
23 17
```

## Sample Output

 Running the application against the 'tests/test_data/full_tournament.txt' file results in the following:

```
$ python3 tennis_calculator_app.py tests/test_data/full_tournament.txt << EOF
Score Match 02
Games Player Person A
EOF

Person C defeated Person A
2 sets to 1

23 17
```

## Scoring Rules

 Details of tennis scoring can be found online. See here for reference:  
 https://en.wikipedia.org/wiki/Tennis_scoring_system

 The variation used for this application is a best of 3 sets match, with first to 6 games wins a set.

## Details are as follows:
 * A tennis match is split up into points, games, and sets.
 * Winning a game requires a person to win 4 points, but they must be ahead by at least 2 points (deuce, advantage, game)
 * The first player to win 6 games wins a set.
   * Players do NOT need to be ahead by 2 to win a set (6-5 finishes a set)
   * There is nothing special about that final game in a set. All games are the same.
 * Best of 3 sets (first to 2 sets wins).


## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Author
Developed by Moditha Akalanka.

### Code Quality and Linting

The project uses Flake8 for code quality and style checking. The configuration is in `.flake8` file.

To run Flake8:
```bash
flake8 .
```

## Cyclomatic Complexity

We use [radon](https://pypi.org/project/radon/) to measure complexity:

```bash
pip install radon
radon cc -s tennis_calculator
```