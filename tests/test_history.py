import pytest
from app.history import History
from app.calculation import Calculation
from app.exceptions import ValidationError


def test_history_add_and_length():
    history = History(max_size=5)
    c = Calculation("add", 2, 3, 5)

    history.add(c)

    assert len(history) == 1
    assert history.all()[0] == c


def test_history_respects_max_size():
    history = History(max_size=2)

    c1 = Calculation("add", 1, 1, 2)
    c2 = Calculation("add", 2, 2, 4)
    c3 = Calculation("add", 3, 3, 6)

    history.add(c1)
    history.add(c2)
    history.add(c3)

    assert len(history) == 2
    assert history.all()[0] == c2
    assert history.all()[1] == c3


def test_history_clear():
    history = History(max_size=3)
    history.add(Calculation("add", 1, 1, 2))
    history.clear()

    assert len(history) == 0


def test_invalid_max_size():
    with pytest.raises(ValidationError):
        History(max_size=0)