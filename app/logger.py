"""
logger.py

Implements observers for:
- Logging calculations
- Automatically saving history to CSV
"""

import logging
import os
import pandas as pd

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig


class LoggingObserver:
    """
    Logs each calculation to a file.
    """

    def __init__(self, config: CalculatorConfig) -> None:
        os.makedirs(config.log_dir, exist_ok=True)

        log_path = os.path.join(config.log_dir, config.log_file)

        logging.basicConfig(
            filename=log_path,
            level=logging.INFO,
            format="%(asctime)s - %(message)s",
        )

    def update(self, calculation: Calculation) -> None:
        logging.info(
            f"{calculation.operation} {calculation.a} {calculation.b} = {calculation.result}"
        )


class AutoSaveObserver:
    """
    Saves calculation history to CSV after each new calculation.
    """

    def __init__(self, config: CalculatorConfig, calculator) -> None:
        self._config = config
        self._calculator = calculator

        os.makedirs(config.history_dir, exist_ok=True)

    def update(self, calculation: Calculation) -> None:
        if not self._config.auto_save:
            return

        history_data = [c.to_dict() for c in self._calculator.history]
        df = pd.DataFrame(history_data)

        file_path = os.path.join(
            self._config.history_dir,
            self._config.history_file,
        )

        df.to_csv(file_path, index=False)