from fractions import Fraction
from numbers import (Rational,
                     Real)
from typing import Type

from .hints import (Coordinate,
                    Point)


def to_rational_point(point: Point[Real],
                      point_cls: Type[Point]) -> Point[Rational]:
    return point_cls(rationalize(point.x), rationalize(point.y))


def rationalize(value: Coordinate) -> Coordinate:
    try:
        return Fraction(value)
    except TypeError:
        return value
