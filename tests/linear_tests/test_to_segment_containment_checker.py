from ground.linear import to_segment_containment_checker


def test_basic() -> None:
    assert callable(to_segment_containment_checker())
