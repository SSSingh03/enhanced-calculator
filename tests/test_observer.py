from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.logger import AutoSaveObserver, LoggingObserver


def _config(tmp_path, auto_save: bool = True) -> CalculatorConfig:
    return CalculatorConfig(
        log_dir=str(tmp_path / "logs"),
        history_dir=str(tmp_path / "history"),
        max_history_size=100,
        auto_save=auto_save,
        precision=6,
        max_input_value=1_000_000_000.0,
        default_encoding="utf-8",
        log_file="calculator.log",
        history_file="history.csv",
    )


def test_autosave_creates_csv(tmp_path):
    config = _config(tmp_path, auto_save=True)
    calc = Calculator(config)

    autosave = AutoSaveObserver(config, calc)
    calc.register_observer(autosave)

    calc.calculate("add", 2, 3)

    csv_path = tmp_path / "history" / "history.csv"
    assert csv_path.exists()


def test_logging_observer_update_does_not_error(tmp_path):
    config = _config(tmp_path, auto_save=True)
    calc = Calculator(config)

    log_obs = LoggingObserver(config)
    calc.register_observer(log_obs)

    calc.calculate("add", 2, 3)


def test_autosave_disabled_does_not_create_csv(tmp_path):
    config = _config(tmp_path, auto_save=False)
    calc = Calculator(config)

    autosave = AutoSaveObserver(config, calc)
    calc.register_observer(autosave)

    calc.calculate("add", 2, 3)

    csv_path = tmp_path / "history" / "history.csv"
    assert not csv_path.exists()