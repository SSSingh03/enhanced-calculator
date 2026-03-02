from app.operations import Add


def test_add() -> None:
    op = Add()
    assert op.execute(2, 3) == 5