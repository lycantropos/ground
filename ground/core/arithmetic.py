from fractions import Fraction

from .hints import Coordinate


def robust_divide(dividend: Coordinate, divisor: Coordinate) -> Coordinate:
    return (dividend / Fraction(divisor)
            if isinstance(divisor, int)
            else dividend / divisor)
