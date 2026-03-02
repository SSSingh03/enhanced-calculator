from app.operations import Add
from app.operations import Subtract, Multiply, Divide
from app.exceptions import OperationError
from app.operations import OperationFactory
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

def test_factory_creates_add():
    op = OperationFactory.create("add")
    assert op.execute(2, 3) == 5


def test_factory_invalid_operation():
    with pytest.raises(OperationError):
        OperationFactory.create("unknown")

@pytest.mark.parametrize(
    "operation_name,a,b,expected",
    [
        ("power", 2, 3, 8),
        ("root", 16, 2, 4),
        ("modulus", 10, 3, 1),
        ("int_divide", 10, 3, 3),
        ("percent", 50, 200, 25),
        ("abs_diff", 10, 4, 6),
    ],
)
def test_factory_operations(operation_name, a, b, expected):
    op = OperationFactory.create(operation_name)
    assert op.execute(a, b) == expected

def test_modulus_zero():
    with pytest.raises(OperationError):
        OperationFactory.create("modulus").execute(10, 0)


def test_int_divide_zero():
    with pytest.raises(OperationError):
        OperationFactory.create("int_divide").execute(10, 0)


def test_percent_zero():
    with pytest.raises(OperationError):
        OperationFactory.create("percent").execute(10, 0)