from fractions import Fraction
from typing import (Callable,
                    Type)

from ground.core.shewchuk import add_to_expansion
from ground.hints import (Multipoint,
                          Point)


def centroid(point_cls: Type[Point],
             multipoint: Multipoint,
             inverse: Callable[[int], Fraction] = Fraction(1).__truediv__
             ) -> Point:
    result_x = result_y = (0,)
    for point in multipoint.points:
        result_x = add_to_expansion(result_x, point.x)
        result_y = add_to_expansion(result_y, point.y)
    inverted_points_count = inverse(len(multipoint.points))
    return point_cls(result_x[-1] * inverted_points_count,
                     result_y[-1] * inverted_points_count)
