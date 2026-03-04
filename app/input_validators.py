"""
input_validators.py

Utility functions for validating user input in the REPL.

Separating validation logic into its own module improves
maintainability and keeps the REPL code cleaner.
"""

from app.exceptions import ValidationError


def validate_two_numbers(parts: list[str]) -> tuple[float, float]:
    """
    Validate that a command contains exactly two numeric arguments.

    Example:
        add 2 3

    Returns:
        tuple[float, float]: Parsed numeric values.

    Raises:
        ValidationError: If the input is invalid.
    """

    if len(parts) != 3:
        raise ValidationError("Operations require exactly two numbers: <command> <a> <b>")

    try:
        a = float(parts[1])
        b = float(parts[2])
    except ValueError:
        raise ValidationError("Arguments must be valid numbers.")

    return a, b