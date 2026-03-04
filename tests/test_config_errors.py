import pytest

from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError


def test_from_env_invalid_int_raises(monkeypatch) -> None:
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "not_an_int")
    with pytest.raises(ValidationError):
        CalculatorConfig.from_env()


def test_from_env_invalid_float_raises(monkeypatch) -> None:
    monkeypatch.setenv("CALCULATOR_MAX_INPUT_VALUE", "not_a_float")
    with pytest.raises(ValidationError):
        CalculatorConfig.from_env()


def test_from_env_empty_required_value_raises(monkeypatch) -> None:
    monkeypatch.setenv("CALCULATOR_LOG_DIR", "")
    with pytest.raises(ValidationError):
        CalculatorConfig.from_env()