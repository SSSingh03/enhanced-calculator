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
from app.exceptions import HistoryError, CalculatorError, ValidationError
from app.history import History
from app.operations import OperationFactory
from app.logger import LoggingObserver, AutoSaveObserver


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
        """Undo the most recent calculation."""
        if not self._undo_stack:
            raise HistoryError("Nothing to undo.")

        # Save current state to redo stack
        self._redo_stack.append(self._snapshot())

        # Restore previous state
        memento = self._undo_stack.pop()
        self._restore(memento)

    def redo(self) -> None:
        """Redo the last undone calculation."""
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


def _print_help() -> None:  # pragma: no cover
    print(
        """
Available commands:
  add, subtract, multiply, divide, power, root, modulus, int_divide, percent, abs_diff <a> <b>
  history
  clear
  undo
  redo
  help
  exit

Notes:
  - All operations take exactly two numbers.
  - undo/redo work on calculation history.
"""
    )


def run_repl() -> None:  # pragma: no cover
    """
    Run the interactive calculator REPL.

    Interactive REPL code is excluded from coverage because it relies on user input.
    Core logic is tested via unit tests for Calculator, operations, and persistence.
    """
    try:
        config = CalculatorConfig.from_env()
    except ValidationError as e:
        print(f"Configuration error: {e}")
        return

    calc = Calculator(config)

    # Register observers
    calc.register_observer(LoggingObserver(config))
    calc.register_observer(AutoSaveObserver(config, calc))

    print("Enhanced Calculator REPL. Type 'help' for commands, 'exit' to quit.")

    while True:
        try:
            raw = input("> ").strip()
            if not raw:
                continue

            parts = raw.split()
            command = parts[0].lower()

            if command == "exit":
                print("Goodbye!")
                return

            if command == "help":
                _print_help()
                continue

            if command == "history":
                if not calc.history:
                    print("(history is empty)")
                else:
                    for i, c in enumerate(calc.history, start=1):
                        print(
                            f"{i}. {c.operation} {c.a} {c.b} = {c.result} ({c.timestamp.isoformat()})"
                        )
                continue

            if command == "clear":
                calc.clear_history()
                print("History cleared.")
                continue

            if command == "undo":
                calc.undo()
                print("Undid last action.")
                continue

            if command == "redo":
                calc.redo()
                print("Redid last undone action.")
                continue

            # Otherwise assume it's an operation that needs two args
            if len(parts) != 3:
                print("Error: operations require exactly two numbers: <command> <a> <b>")
                continue

            a = float(parts[1])
            b = float(parts[2])

            result_calc = calc.calculate(command, a, b)
            print(result_calc.result)

        except ValueError:
            print("Error: please enter valid numbers. Example: add 2 3")
        except CalculatorError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            return