from fractions import Fraction
from typing import (Callable,
                    Sequence,
                    Type)

from ground.hints import Point


def centroid(point_cls: Type[Point],
             points: Sequence[Point],
             inverse: Callable[[int], Fraction] = Fraction(1).__truediv__
             ) -> Point:
    result_x = result_y = 0
    for point in points:
        result_x += Fraction(point.x)
        result_y += Fraction(point.y)
    inverted_points_count = inverse(len(points))
    return point_cls(result_x * inverted_points_count,
                     result_y * inverted_points_count)
