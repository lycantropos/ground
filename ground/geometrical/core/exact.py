from fractions import Fraction

from reprit.base import generate_repr

from ground.hints import Coordinate
from .plain import (Contour,
                    Multipoint,
                    Multipolygon,
                    Multisegment,
                    Polygon,
                    Segment)


class Point:
    __slots__ = '_x', '_y'

    def __init__(self, x: Coordinate, y: Coordinate) -> None:
        self._x, self._y = Fraction(x), Fraction(y)

    __repr__ = generate_repr(__init__)

    @property
    def x(self) -> Coordinate:
        return self._x

    @property
    def y(self) -> Coordinate:
        return self._y


Contour = Contour
Multipoint = Multipoint
Multisegment = Multisegment
Multipolygon = Multipolygon
Polygon = Polygon
Segment = Segment
