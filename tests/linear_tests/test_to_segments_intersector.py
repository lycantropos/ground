from ground.linear import to_segments_intersector


def test_basic() -> None:
    assert callable(to_segments_intersector())
