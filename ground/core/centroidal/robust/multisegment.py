from typing import (Callable,
                    Type)

from shewchuk import Expansion

from ground.core.hints import (Multisegment,
                               Point,
                               Scalar)
from ground.core.robust import to_squared_points_distance


def centroid(multisegment: Multisegment,
             point_cls: Type[Point],
             sqrt: Callable[[Scalar], Scalar]) -> Point:
    accumulated_x = accumulated_y = accumulated_length = Expansion()
    for segment in multisegment.segments:
        start, end = segment.start, segment.end
        length = sqrt(to_squared_points_distance(end.x, end.y, start.x,
                                                 start.y))
        accumulated_x += (start.x + end.x) * length
        accumulated_y += (start.y + end.y) * length
        accumulated_length += length
    inverted_divisor = 1 / (2 * accumulated_length)
    return point_cls(accumulated_x * inverted_divisor,
                     accumulated_y * inverted_divisor)
