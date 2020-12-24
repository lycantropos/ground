from fractions import Fraction

from ground.hints import Coordinate


def to_sign(value: Coordinate) -> int:
    return (1 if value > 0 else -1) if value else 0


def robust_inverse(value: Coordinate) -> Coordinate:
    return Fraction(1, value) if isinstance(value, int) else 1 / value
