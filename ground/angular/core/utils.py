from ground.hints import Coordinate


def to_sign(value: Coordinate) -> int:
    return (1 if value > 0 else -1) if value else 0
