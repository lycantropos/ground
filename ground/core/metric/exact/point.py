from fractions import Fraction

from ground.core.hints import (Coordinate,
                               Point)


def point_squared_distance(first: Point, second: Point) -> Coordinate:
    return ((Fraction(first.x) - Fraction(second.x)) ** 2
            + (Fraction(first.y) - Fraction(second.y)) ** 2)
