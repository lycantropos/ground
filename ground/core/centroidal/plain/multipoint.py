from fractions import Fraction
from typing import Type

from ground.hints import (Multipoint,
                          Point)


def centroid(point_cls: Type[Point],
             multipoint: Multipoint) -> Point:
    result_x = result_y = 0
    for point in multipoint.points:
        result_x += point.x
        result_y += point.y
    inverted_points_count = Fraction(1, len(multipoint.points))
    return point_cls(result_x * inverted_points_count,
                     result_y * inverted_points_count)
