from ground.linear import to_connected_segments_intersector


def test_basic() -> None:
    assert callable(to_connected_segments_intersector())
