from typing import Type

from shewchuk import Expansion

from ground.core.hints import (Point,
                               Segment)


def centroid(segment: Segment, point_cls: Type[Point]) -> Point:
    return point_cls(Expansion(segment.start.x, segment.end.x) / 2,
                     Expansion(segment.start.y, segment.end.y) / 2)
