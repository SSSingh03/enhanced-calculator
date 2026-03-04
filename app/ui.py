"""
ui.py

Small UI helpers for the REPL (command-line interface).

This module keeps presentation concerns (colors / formatting) separate from the
calculator core logic. That separation is a professional practice:
- Core logic stays testable and reusable.
- UI can change without breaking business logic.
"""

from __future__ import annotations

from dataclasses import dataclass

from colorama import Fore, Style, init


# Initialize colorama once so ANSI colors work on Windows too.
# autoreset=True avoids "leaking" colors into later prints.
init(autoreset=True)


@dataclass(frozen=True)
class UIColors:
    """Central place to define how we color different message types."""
    ok: str = Fore.GREEN
    warn: str = Fore.YELLOW
    error: str = Fore.RED
    info: str = Fore.CYAN
    reset: str = Style.RESET_ALL


COLORS = UIColors()


def fmt_ok(message: str) -> str:
    return f"{COLORS.ok}{message}{COLORS.reset}"


def fmt_warn(message: str) -> str:
    return f"{COLORS.warn}{message}{COLORS.reset}"


def fmt_error(message: str) -> str:
    return f"{COLORS.error}{message}{COLORS.reset}"


def fmt_info(message: str) -> str:
    return f"{COLORS.info}{message}{COLORS.reset}"