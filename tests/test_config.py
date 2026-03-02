import os 
import pytest 

from app.calculator_config import CalculatorConfig, ValidationError
from app.exceptions import ValidationError

def test_from_env_uses_defaults_when_not_set(monkeypatch) -> None:
    # Ensure variables are absent so defaults are used

    keys = [
        "CALCULATOR_LOG_DIR",
        "CALCULATOR_HISTORY_DIR",
        "CALCULATOR_MAX_HISTORY_SIZE",
        "CALCULATOR_AUTO_SAVE",
        "CALCULATOR_PRECISION",
        "CALCULATOR_MAX_INPUT_VALUE",
        "CALCULATOR_DEFAULT_ENCODING",
        "CALCULATOR_LOG_FILE",
        "CALCULATOR_HISTORY_FILE",
    ]
    for k in keys:
        monkeypatch.delenv(k, raising=False)

    cfg  = CalculatorConfig.from_env()

    assert cfg.log_dir == "logs"
    assert cfg.history_dir == "history"
    assert cfg.max_history_size == 100
    assert cfg.auto_save is True
    assert cfg.precision == 6
    assert cfg.max_input_value == 1_000_000_000.0
    assert cfg.default_encoding == "utf-8"
    assert cfg.log_file == "calculator.log"
    assert cfg.history_file == "history.csv"

def test_from_env_invalid_bool_raises(monkeypatch) -> None:
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "maybe")

    with pytest.raises(ValidationError):
        CalculatorConfig.from_env()