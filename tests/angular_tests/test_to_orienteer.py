from ground.angular import to_orienteer


def test_basic() -> None:
    assert callable(to_orienteer())
