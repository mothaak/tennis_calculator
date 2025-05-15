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

The main components of the solution are:

1. `MatchProcessor`: This class is responsible for processing the input data and calculating the results of the matches. It takes the list of points as input and determines the winner, loser, and the set scores for each match.

2. `QueryProcessor`: This class handles user queries and provides the requested information based on the calculated results. It supports two types of queries: querying the result of a specific match and querying the games won/lost by a player over the entire tournament.

3. `tennis_calculator_app.py`: This is the main entry point of the application. It reads the input file, processes the matches using the `MatchProcessor`, and handles user queries using the `QueryProcessor`.

The solution also includes a comprehensive test suite to ensure the correctness of the implemented functionality. The tests cover various scenarios and edge cases to validate the behavior of the `MatchProcessor` and `QueryProcessor` classes.

## Setup

### Prerequisites

Ensure you have Python 3 installed. You can download it from https://www.python.org/.

### Directory Structure

Ensure your directory structure looks like this:

```
tennis_calculator/
    __init__.py
    match_processor.py
    query_processor.py
    tennis_calculator_app.py
    tests/
        test_data/
            full_tournament.txt
        __init__.py
        test_match_processor.py
        test_query_processor.py
        test_integration.py
        test_input.txt
```

### Running the Application

To run the application with a specific input file, use the following command:

```
python3 tennis_calculator_app.py <input_file>
```

# Example:

```
python3 tennis_calculator_app.py tests/test_data/full_tournament.txt
```

### Running the Tests

To run the tests, use the following commands from your terminal:

#### Unit Tests

```
python3 -m unittest tests/test_match_processor.py
python3 -m unittest tests/test_query_processor.py
```

#### Integration Tests

```
python3 -m unittest tests/test_integration.py
```

#### All Tests

To run all tests at once 
```
python3 -m unittest discover -s tests
```

These commands will execute the tests and provide the results in the terminal.

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
