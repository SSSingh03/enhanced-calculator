"""
calculator_config.py

Loads calculator configuration from environment variables (.env) and provides
a validated, typed configuration object for the application.
"""

from dataclasses import dataclass
import os
from dotenv import load_dotenv

from app.exceptions import ValidationError


@dataclass(frozen=True)
class CalculatorConfig:
    """
    Typed configuration for the calculator application.

    frozen=True makes this immutable (safer): once loaded,
    config values can't accidentally be changed mid-run.
    """

    log_dir: str
    history_dir: str
    max_history_size: int
    auto_save: bool
    precision: int
    max_input_value: float
    default_encoding: str
    log_file: str
    history_file: str

    @classmethod
    def from_env(cls) -> "CalculatorConfig":
        """
        Load config from .env / environment variables,
        apply defaults, parse types, and validate values.
        """
        load_dotenv()

        log_dir = _get_env("CALCULATOR_LOG_DIR", "logs")
        history_dir = _get_env("CALCULATOR_HISTORY_DIR", "history")
        log_file = _get_env("CALCULATOR_LOG_FILE", "calculator.log")
        history_file = _get_env("CALCULATOR_HISTORY_FILE", "history.csv")

        max_history_size = _parse_int(
            _get_env("CALCULATOR_MAX_HISTORY_SIZE", "100"),
            "CALCULATOR_MAX_HISTORY_SIZE",
        )
        precision = _parse_int(
            _get_env("CALCULATOR_PRECISION", "6"),
            "CALCULATOR_PRECISION",
        )
        max_input_value = _parse_float(
            _get_env("CALCULATOR_MAX_INPUT_VALUE", "1000000000"),
            "CALCULATOR_MAX_INPUT_VALUE",
        )
        default_encoding = _get_env("CALCULATOR_DEFAULT_ENCODING", "utf-8")
        auto_save = _parse_bool(_get_env("CALCULATOR_AUTO_SAVE", "true"))

        _validate_positive(max_history_size, "CALCULATOR_MAX_HISTORY_SIZE")
        _validate_non_negative(precision, "CALCULATOR_PRECISION")

        if max_input_value <= 0:
            raise ValidationError(
                f"CALCULATOR_MAX_INPUT_VALUE must be > 0. Got: {max_input_value}"
            )

        return cls(
            log_dir=log_dir,
            history_dir=history_dir,
            max_history_size=max_history_size,
            auto_save=auto_save,
            precision=precision,
            max_input_value=max_input_value,
            default_encoding=default_encoding,
            log_file=log_file,
            history_file=history_file,
        )


def _parse_bool(value: str) -> bool:
    """
    Convert common string representations to boolean.

    Accepts true/false, 1/0, yes/no, y/n, on/off (case-insensitive).
    Raises ValidationError for invalid inputs.
    """
    normalized = value.strip().lower()

    if normalized in {"true", "1", "yes", "y", "on"}:
        return True
    if normalized in {"false", "0", "no", "n", "off"}:
        return False

    raise ValidationError(f"Invalid boolean value: '{value}'")


def _parse_int(value: str, name: str) -> int:
    """Convert a string to an integer, raising ValidationError if it fails."""
    try:
        return int(value)
    except ValueError:
        raise ValidationError(f"Invalid integer value for {name}: '{value}'")


def _parse_float(value: str, name: str) -> float:
    """Convert a string to a float, raising ValidationError if it fails."""
    try:
        return float(value)
    except ValueError:
        raise ValidationError(f"Invalid float value for {name}: '{value}'")


def _get_env(name: str, default: str | None = None) -> str:
    """
    Read an environment variable with a default.

    Returns a string.
    Raises ValidationError if missing and no default provided.
    """
    value = os.getenv(name, default)

    if value is None or value == "":
        raise ValidationError(f"Missing required environment variable: {name}")

    return value


def _validate_positive(value: int, name: str) -> None:
    """Ensure a numeric config value is positive."""
    if value <= 0:
        raise ValidationError(f"{name} must be > 0. Got: {value}")


def _validate_non_negative(value: int, name: str) -> None:
    """Ensure a numeric config value is non-negative."""
    if value < 0:
        raise ValidationError(f"{name} must be >= 0. Got: {value}")