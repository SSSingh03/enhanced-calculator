import os

from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.logger import AutoSaveObserver


def _config(tmp_path):
    return CalculatorConfig(
        log_dir=str(tmp_path / "logs"),
        history_dir=str(tmp_path / "history"),
        max_history_size=100,
        auto_save=True,
        precision=6,
        max_input_value=1_000_000_000.0,
        default_encoding="utf-8",
        log_file="calculator.log",
        history_file="history.csv",
    )


def test_autosave_creates_csv(tmp_path):
    config = _config(tmp_path)
    calc = Calculator(config)

    autosave = AutoSaveObserver(config, calc)
    calc.register_observer(autosave)

    calc.calculate("add", 2, 3)

    csv_path = tmp_path / "history" / "history.csv"
    assert csv_path.exists()