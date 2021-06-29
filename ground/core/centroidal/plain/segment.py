from typing import Type

from cfractions import Fraction

from ground.core.hints import (Point,
                               Segment)


def centroid(segment: Segment, point_cls: Type[Point],
             *,
             _half: Fraction = Fraction(1, 2)) -> Point:
    return point_cls(_half * (segment.start.x + segment.end.x),
                     _half * (segment.start.y + segment.end.y))
