from fractions import Fraction
from numbers import (Rational,
                     Real)
from typing import Type

from .hints import (Point,
                    Scalar)


def to_rational_point(point: Point[Real],
                      point_cls: Type[Point]) -> Point[Rational]:
    return point_cls(rationalize(point.x), rationalize(point.y))


def rationalize(value: Scalar) -> Scalar:
    try:
        return Fraction(value)
    except TypeError:
        return value
