from fractions import Fraction
from typing import (Callable,
                    Type)

from ground.hints import (Multipoint,
                          Point)


def centroid(point_cls: Type[Point],
             multipoint: Multipoint,
             inverse: Callable[[int], Fraction] = Fraction(1).__truediv__
             ) -> Point:
    result_x = result_y = 0
    for point in multipoint.points:
        result_x += point.x
        result_y += point.y
    inverted_points_count = inverse(len(multipoint.points))
    return point_cls(result_x * inverted_points_count,
                     result_y * inverted_points_count)
