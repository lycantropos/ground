from fractions import Fraction
from typing import (Callable,
                    Sequence,
                    Type)

from ground.core.hints import Point
from ground.core.primitive import rationalize


def centroid(points: Sequence[Point],
             point_cls: Type[Point],
             inverse: Callable[[int], Fraction] = Fraction(1).__truediv__
             ) -> Point:
    result_x = result_y = 0
    for point in points:
        result_x += rationalize(point.x)
        result_y += rationalize(point.y)
    inverted_points_count = inverse(len(points))
    return point_cls(result_x * inverted_points_count,
                     result_y * inverted_points_count)
