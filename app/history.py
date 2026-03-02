"""
history.py

Manages calculation history for the calculator application.

This class is responsible for:
- Storing Calculation objects
- Enforcing maximum history size
- Providing access to history
"""

from typing import List
from app.calculation import Calculation
from app.exceptions import ValidationError


class History:
    """
    Maintains a bounded list of Calculation objects.
    """

    def __init__(self, max_size: int) -> None:
        if max_size <= 0:
            raise ValidationError("History max_size must be greater than 0.")

        self._max_size = max_size
        self._items: List[Calculation] = []

    def add(self, calculation: Calculation) -> None:
        """
        Add a new calculation to history.
        If history exceeds max_size, remove the oldest entry.
        """
        self._items.append(calculation)

        if len(self._items) > self._max_size:
            self._items.pop(0)  # remove oldest (FIFO behavior)

    def clear(self) -> None:
        """Clear all history."""
        self._items.clear()

    def all(self) -> List[Calculation]:
        """Return a copy of the history list."""
        return list(self._items)

    def __len__(self) -> int:
        return len(self._items)