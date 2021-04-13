from fractions import Fraction
from numbers import (Rational,
                     Real)
from typing import Type

from .hints import Point


def to_rational_point(point: Point[Real],
                      point_cls: Type[Point]) -> Point[Rational]:
    return point_cls(Fraction(point.x), Fraction(point.y))
