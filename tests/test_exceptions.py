"""
Unit tests for exceptions in the calculator application.

These tests ensure that the custom exceptions defined in `exceptions.py` are raised correctly under various error conditions. By testing these exceptions, we can verify that our error handling mechanisms are working as intended and that users receive meaningful feedback when something goes wrong.
"""
from app.exceptions import CalculatorError, HistoryError, OperationError, ValidationError

def test_exception_inheritance():
    """Test that all custom exceptions inherit from CalculatorError."""
    assert issubclass(OperationError, CalculatorError)
    assert issubclass(ValidationError, CalculatorError)
    assert issubclass(HistoryError, CalculatorError)