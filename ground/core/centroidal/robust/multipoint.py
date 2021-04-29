from fractions import Fraction
from typing import (Callable,
                    Type)

from ground.core.hints import (Multipoint,
                               Point)
from ground.core.shewchuk import add_to_expansion


def centroid(multipoint: Multipoint,
             point_cls: Type[Point],
             inverse: Callable[[int], Fraction] = Fraction(1).__truediv__
             ) -> Point:
    result_x = result_y = (0,)
    for point in multipoint.points:
        result_x, result_y = (add_to_expansion(result_x, point.x),
                              add_to_expansion(result_y, point.y))
    inverted_points_count = inverse(len(multipoint.points))
    return point_cls(result_x[-1] * inverted_points_count,
                     result_y[-1] * inverted_points_count)
