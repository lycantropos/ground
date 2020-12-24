from typing import Type

from ground.core.hints import UnaryCoordinateOperation
from ground.core.shewchuk import (scale_expansion,
                                  sum_expansions,
                                  to_cross_product)
from ground.hints import (Contour,
                          Point)


def centroid(inverse: UnaryCoordinateOperation,
             point_cls: Type[Point],
             contour: Contour) -> Point:
    double_area = x_numerator = y_numerator = (0,)
    vertices = contour.vertices
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
