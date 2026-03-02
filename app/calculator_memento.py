"""
calculator_memento.py

Implements the Memento pattern for undo/redo.

A memento stores a snapshot of calculator state (calculation history) so
we can restore it later without exposing internal details.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from app.calculation import Calculation


@dataclass(frozen=True)
class CalculatorMemento:
    """
    Immutable snapshot of calculator state.

    For this project, the "state" we care about is the calculation history.
    """
    history_snapshot: List[Calculation]