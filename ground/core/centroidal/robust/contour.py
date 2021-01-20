from fractions import Fraction
from typing import (Callable,
                    Sequence,
                    Type)

from ground.core.shewchuk import (scale_expansion,
                                  sum_expansions,
                                  to_cross_product)
from ground.hints import Point


def centroid(point_cls: Type[Point],
             vertices: Sequence[Point],
             inverse: Callable[[int], Fraction] = Fraction(1).__truediv__
             ) -> Point:
    double_area = x_numerator = y_numerator = (0,)
    prev = vertices[-1]
    prev_x, prev_y = prev.x, prev.y
    for vertex in vertices:
        x, y = vertex.x, vertex.y
        area_component = to_cross_product(prev_x, prev_y, x, y)
        double_area = sum_expansions(double_area, area_component)
        x_numerator = sum_expansions(x_numerator,
                                     scale_expansion(area_component,
                                                     prev_x + x))
        y_numerator = sum_expansions(y_numerator,
                                     scale_expansion(area_component,
                                                     prev_y + y))
        prev_x, prev_y = x, y
    inverted_denominator = inverse(3 * double_area[-1])
    return point_cls(x_numerator[-1] * inverted_denominator,
                     y_numerator[-1] * inverted_denominator)
