from app.operations import Add
from app.operations import Subtract, Multiply, Divide
from app.exceptions import OperationError
import pytest

def test_add() -> None:
    op = Add()
    assert op.execute(2, 3) == 5

def test_subtract():
    assert Subtract().execute(5, 3) == 2


def test_multiply():
    assert Multiply().execute(4, 3) == 12


def test_divide():
    assert Divide().execute(10, 2) == 5


def test_divide_by_zero():
    with pytest.raises(OperationError):
        Divide().execute(10, 0)