from numbers import (Rational,
                     Real)
from typing import Type

from cfractions import Fraction

from .hints import (Point,
                    Scalar)


def rationalize(value: Scalar) -> Scalar:
    try:
        return Fraction(value)
    except TypeError:
        return value


def square(value: Scalar) -> Scalar:
    return value * value


def to_rational_point(point: Point[Real],
                      point_cls: Type[Point]) -> Point[Rational]:
    return point_cls(rationalize(point.x), rationalize(point.y))


def to_sign(value: Scalar) -> int:
    return 1 if value > 0 else (-1 if value else 0)
