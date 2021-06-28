from typing import (Callable,
                    Type)

from cfractions import Fraction
from shewchuk import Expansion

from ground.core.hints import (Multipoint,
                               Point)


def centroid(multipoint: Multipoint,
             point_cls: Type[Point],
             inverse: Callable[[int], Fraction] = Fraction(1).__truediv__
             ) -> Point:
    result_x = result_y = Expansion()
    for point in multipoint.points:
        result_x += point.x
        result_y += point.y
    inverted_points_count = inverse(len(multipoint.points))
    return point_cls(result_x * inverted_points_count,
                     result_y * inverted_points_count)
