"""
calculator.py

Core Calculator service for the application.

Responsibilities:
- Execute operations (via OperationFactory)
- Record each calculation into History
- Support undo/redo using the Memento pattern
"""

from __future__ import annotations

from typing import List

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.calculator_memento import CalculatorMemento
from app.exceptions import HistoryError
from app.history import History
from app.operations import OperationFactory


class Calculator:
    """
    Calculator orchestrates operations, history management, and undo/redo.

    Design patterns used:
    - Factory: OperationFactory creates the correct Operation instance
    - Memento: CalculatorMemento snapshots history state for undo/redo
    """

    def __init__(self, config: CalculatorConfig) -> None:
        self._config = config
        self._history = History(max_size=config.max_history_size)

        # Memento stacks
        self._undo_stack: List[CalculatorMemento] = []
        self._redo_stack: List[CalculatorMemento] = []

    @property
    def history(self) -> List[Calculation]:
        """Return a copy of current history (for display/testing)."""
        return self._history.all()

    def _snapshot(self) -> CalculatorMemento:
        """Create an immutable snapshot of current calculator history."""
        return CalculatorMemento(history_snapshot=self._history.all())

    def calculate(self, operation_name: str, a: float, b: float) -> Calculation:
        """
        Perform an operation, store it in history, and return the Calculation record.

        Memento rule:
        - Save a snapshot BEFORE mutating history so undo can restore it.
        - Clear redo stack on any new action.
        """
        # Save state for undo
        self._undo_stack.append(self._snapshot())
        self._redo_stack.clear()

        op = OperationFactory.create(operation_name)
        result = op.execute(a, b)

        # Apply precision if configured (rounding for consistent output)
        result = round(result, self._config.precision)

        calc = Calculation(operation=op.name, a=a, b=b, result=result)
        self._history.add(calc)
        return calc

    def undo(self) -> None:
        """
        Undo the most recent calculation by restoring the last snapshot.

        Memento rule:
        - Move current state to redo stack
        - Restore state from undo stack
        """
        if not self._undo_stack:
            raise HistoryError("Nothing to undo.")

        # Save current state for redo
        self._redo_stack.append(self._snapshot())

        # Restore previous state
        memento = self._undo_stack.pop()
        self._restore(memento)

    def redo(self) -> None:
        """
        Redo the last undone calculation by restoring the last redo snapshot.

        Memento rule:
        - Move current state to undo stack
        - Restore state from redo stack
        """
        if not self._redo_stack:
            raise HistoryError("Nothing to redo.")

        # Save current state for undo
        self._undo_stack.append(self._snapshot())

        # Restore next state
        memento = self._redo_stack.pop()
        self._restore(memento)

    def clear_history(self) -> None:
        """
        Clear history. This is a user action, so it should affect undo/redo.

        We snapshot first so user can undo the clear if desired.
        """
        self._undo_stack.append(self._snapshot())
        self._redo_stack.clear()
        self._history.clear()

    def _restore(self, memento: CalculatorMemento) -> None:
        """Restore history from a memento snapshot."""
        # Rebuild history (respect max size)
        self._history.clear()
        for calc in memento.history_snapshot:
            self._history.add(calc)