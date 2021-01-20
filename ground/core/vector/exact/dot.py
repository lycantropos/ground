from fractions import Fraction

from ground.hints import (Coordinate,
                          Point)


def multiply(first_start: Point,
             first_end: Point,
             second_start: Point,
             second_end: Point) -> Coordinate:
    return ((Fraction(first_end.x) - Fraction(first_start.x))
            * (Fraction(second_end.x) - Fraction(second_start.x))
            + (Fraction(first_end.y) - Fraction(first_start.y))
            * (Fraction(second_end.y) - Fraction(second_start.y)))
