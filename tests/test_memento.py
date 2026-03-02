from app.calculation import Calculation
from app.calculator_memento import CalculatorMemento


def test_memento_stores_history_snapshot():
    c1 = Calculation("add", 1, 2, 3)
    c2 = Calculation("multiply", 2, 3, 6)

    snapshot = [c1, c2]
    m = CalculatorMemento(history_snapshot=list(snapshot))

    assert m.history_snapshot == snapshot