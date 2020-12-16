from ground.angular import to_classifier


def test_basic() -> None:
    assert callable(to_classifier())
