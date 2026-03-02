"""
calculation.py

Defines the Calculation data model.

A Calculation represents one completed operation (e.g., add 2 3 = 5) and
is the atomic record we store in history, log, and persist to CSV.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict


@dataclass(frozen=True)
class Calculation:
    """
    Immutable record of a single calculation.

    Why immutable?
    - Once a calculation is created, it should not change.
    - This makes history/undo/redo safer and easier to reason about.
    """

    operation: str
    a: float
    b: float
    result: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert this Calculation into a dictionary suitable for:
        - pandas DataFrame creation
        - CSV serialization
        """
        return {
            "operation": self.operation,
            "a": self.a,
            "b": self.b,
            "result": self.result,
            # ISO 8601 string is portable and easy to parse later
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, row: Dict[str, Any]) -> Calculation:
        """
        Rebuild a Calculation from a dict (e.g., a row loaded from CSV).

        This supports history loading via pandas.
        """
        try:
            ts_raw = row["timestamp"]
            ts = datetime.fromisoformat(ts_raw) if isinstance(ts_raw, str) else ts_raw
            return cls(
                operation=str(row["operation"]),
                a=float(row["a"]),
                b=float(row["b"]),
                result=float(row["result"]),
                timestamp=ts,
            )
        except (KeyError, TypeError, ValueError) as e:
            # We'll later wrap this in a domain-specific exception if desired.
            raise ValueError(f"Malformed calculation row: {row}") from e