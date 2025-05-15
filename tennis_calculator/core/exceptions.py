"""Tennis calculator exceptions."""


class TennisCalculatorException(Exception):
    """Base exception for tennis calculator."""

    pass


class InvalidMatchDataException(TennisCalculatorException):
    """Raised when match data is invalid."""

    pass


class InvalidMatchFormatException(TennisCalculatorException):
    """Raised when match format is invalid."""

    pass


class InvalidQueryException(TennisCalculatorException):
    """Raised when query format is invalid."""

    pass


class MatchNotFoundException(TennisCalculatorException):
    """Raised when match is not found."""

    pass


class PlayerNotFoundException(TennisCalculatorException):
    """Raised when player is not found."""

    pass


class DuplicateMatchException(TennisCalculatorException):
    """Raised when trying to add a duplicate match."""

    pass


class MatchCompletedException(TennisCalculatorException):
    """Raised when trying to record points after match completion."""

    pass


class InvalidPlayerNumberException(TennisCalculatorException):
    """Raised when player number is invalid."""
