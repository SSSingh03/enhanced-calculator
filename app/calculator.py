"""
calculator.py

Core Calculator service for the enhanced calculator application.

Responsibilities:
- Execute operations (via OperationFactory)
- Store results in History
- Support undo/redo using the Memento pattern
- Notify observers (Observer pattern) after each calculation
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
    Calculator orchestrates:

    - Factory Pattern (OperationFactory)
    - Memento Pattern (undo/redo)
    - Observer Pattern (logging, autosave)
    """

    def __init__(self, config: CalculatorConfig) -> None:
        self._config = config
        self._history = History(max_size=config.max_history_size)

        # Stacks for Memento pattern
        self._undo_stack: List[CalculatorMemento] = []
        self._redo_stack: List[CalculatorMemento] = []

        # Observers for Observer pattern
        self._observers = []

    # -------------------------
    # Observer Pattern Methods
    # -------------------------

    def register_observer(self, observer) -> None:
        """
        Register an observer to be notified when a new calculation is created.

        Observer must implement:
            update(calculation: Calculation) -> None
        """
        self._observers.append(observer)

    def _notify_observers(self, calculation: Calculation) -> None:
        """Notify all registered observers."""
        for observer in self._observers:
            observer.update(calculation)

    # -------------------------
    # Public API
    # -------------------------

    @property
    def history(self) -> List[Calculation]:
        """Return a copy of calculation history."""
        return self._history.all()

    def calculate(self, operation_name: str, a: float, b: float) -> Calculation:
        """
        Perform an operation and store result in history.

        Memento Rule:
        - Snapshot BEFORE changing state
        - Clear redo stack on new action
        """

        # Save state for undo
        self._undo_stack.append(self._snapshot())
        self._redo_stack.clear()

        op = OperationFactory.create(operation_name)
        result = op.execute(a, b)

        # Apply configured precision
        result = round(result, self._config.precision)

        calc = Calculation(operation=op.name, a=a, b=b, result=result)
        self._history.add(calc)

        # Notify observers
        self._notify_observers(calc)

        return calc

    def undo(self) -> None:
        """
        Undo the most recent calculation.
        """
        if not self._undo_stack:
            raise HistoryError("Nothing to undo.")

        # Save current state to redo stack
        self._redo_stack.append(self._snapshot())

        # Restore previous state
        memento = self._undo_stack.pop()
        self._restore(memento)

    def redo(self) -> None:
        """
        Redo the last undone calculation.
        """
        if not self._redo_stack:
            raise HistoryError("Nothing to redo.")

        # Save current state to undo stack
        self._undo_stack.append(self._snapshot())

        # Restore next state
        memento = self._redo_stack.pop()
        self._restore(memento)

    def clear_history(self) -> None:
        """
        Clear calculation history.
        Snapshot first so user can undo.
        """
        self._undo_stack.append(self._snapshot())
        self._redo_stack.clear()
        self._history.clear()

    # -------------------------
    # Internal Helpers
    # -------------------------

    def _snapshot(self) -> CalculatorMemento:
        """Create snapshot of current state."""
        return CalculatorMemento(history_snapshot=self._history.all())

    def _restore(self, memento: CalculatorMemento) -> None:
        """Restore calculator state from memento."""
        self._history.clear()
        for calc in memento.history_snapshot:
            self._history.add(calc)