class DetectiveError(Exception):
    """Base class for all game errors."""

class InvalidWarrantError(DetectiveError):
    """Player's regex is invalid or too long."""

class WarrantBudgetExceeded(DetectiveError):
    """Player used all searches."""

class WrongAccusationError(DetectiveError):
    """Player accused the wrong suspect."""