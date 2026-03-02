"""
Unit tests for the Calculation model.

These tests ensure Calculation instances can be safely serialized to/from
dicts for CSV persistence (pandas) and history loading.
"""

from datetime import datetime, timezone

import pytest

from app.calculation import Calculation


def test_calculation_fields_and_timestamp() -> None:
    c = Calculation(operation="add", a=2, b=3, result=5)

    assert c.operation == "add"
    assert c.a == 2
    assert c.b == 3
    assert c.result == 5

    # Timestamp should be auto-created by the Calculation class
    assert isinstance(c.timestamp, datetime)


def test_to_dict_contains_expected_keys() -> None:
    ts = datetime(2025, 1, 1, tzinfo=timezone.utc)
    c = Calculation(operation="multiply", a=4, b=5, result=20, timestamp=ts)

    data = c.to_dict()

    assert data["operation"] == "multiply"
    assert data["a"] == 4
    assert data["b"] == 5
    assert data["result"] == 20
    assert data["timestamp"] == ts.isoformat()


def test_from_dict_round_trip() -> None:
    original = Calculation(operation="subtract", a=10, b=7, result=3)
    rebuilt = Calculation.from_dict(original.to_dict())

    assert rebuilt.operation == original.operation
    assert rebuilt.a == original.a
    assert rebuilt.b == original.b
    assert rebuilt.result == original.result
    assert rebuilt.timestamp == original.timestamp


def test_from_dict_missing_key_raises() -> None:
    bad_row = {"operation": "add", "a": 1, "b": 2, "result": 3}  # missing timestamp
    with pytest.raises(ValueError):
        Calculation.from_dict(bad_row)