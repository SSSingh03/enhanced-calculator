"""
exceptions.py

This module defines custom exceptions for the enhanced calculator application.

Creating a dedicated exceptions module allows us to handle specific error cases in a more organized and meaningful way. Each exception can provide additional context about the error, making it easier for developers to debug and users to understand what went wrong.
"""

class CalculatorError(Exception):
    """ Base class for exceptions in the enhanced calculator. This allows the REPL layer to catch any calculator-specific error in a single except block without crashing the program """
    pass


class OperationError(CalculatorError):
    """Raised when an arithmetic operation fails, such as division by zero or invalid input types. """
    pass


class ValidationError(CalculatorError):
    """Raised when input validation fails, such as when a user provides an invalid expression or unsupported operation. """
    pass


class HistoryError(CalculatorError):
    """Raised when there is an issue with the calculation history or undo/redo functionality, such as trying to undo when there are no previous operations. """
    pass
   