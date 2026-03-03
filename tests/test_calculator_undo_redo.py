import pytest

from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.exceptions import HistoryError


def _config() -> CalculatorConfig:
    # Small history size is fine for tests; precision 6 matches defaults
    return CalculatorConfig(
        log_dir="logs",
        history_dir="history",
        max_history_size=100,
        auto_save=True,
        precision=6,
        max_input_value=1_000_000_000.0,
        default_encoding="utf-8",
        log_file="calculator.log",
        history_file="history.csv",
    )


def test_calculate_adds_to_history():
    calc = Calculator(_config())
    calc.calculate("add", 2, 3)

    assert len(calc.history) == 1
    assert calc.history[0].operation == "add"
    assert calc.history[0].result == 5


def test_undo_removes_last_calculation():
    calc = Calculator(_config())
    calc.calculate("add", 2, 3)
    calc.calculate("multiply", 2, 4)

    assert len(calc.history) == 2

    calc.undo()
    assert len(calc.history) == 1
    assert calc.history[0].operation == "add"


def test_redo_restores_last_undone_calculation():
    calc = Calculator(_config())
    calc.calculate("add", 2, 3)
    calc.calculate("multiply", 2, 4)

    calc.undo()
    assert len(calc.history) == 1

    calc.redo()
    assert len(calc.history) == 2
    assert calc.history[1].operation == "multiply"


def test_undo_empty_raises():
    calc = Calculator(_config())
    with pytest.raises(HistoryError):
        calc.undo()


def test_redo_empty_raises():
    calc = Calculator(_config())
    with pytest.raises(HistoryError):
        calc.redo()


def test_new_calculation_clears_redo_stack():
    calc = Calculator(_config())
    calc.calculate("add", 2, 3)
    calc.calculate("multiply", 2, 4)

    calc.undo()
    # redo is now possible, but a new calculation should clear redo history
    calc.calculate("subtract", 10, 1)

    with pytest.raises(HistoryError):
        calc.redo()