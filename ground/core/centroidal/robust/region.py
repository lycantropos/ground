from fractions import Fraction
from typing import (Sequence,
                    Tuple,
                    Type)

from ground.core.hints import (Contour,
                               Expansion,
                               Point)
from ground.core.shewchuk import (scale_expansion,
                                  sum_expansions,
                                  to_cross_product)


def centroid(contour: Contour,
             point_cls: Type[Point],
             third: Fraction = Fraction(1, 3)) -> Point:
    x_numerator, y_numerator, double_area = centroid_components(
            contour.vertices)
    inverted_denominator = third / double_area[-1]
    return point_cls(x_numerator[-1] * inverted_denominator,
                     y_numerator[-1] * inverted_denominator)


def centroid_components(vertices: Sequence[Point]
                        ) -> Tuple[Expansion, Expansion, Expansion]:
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
    return x_numerator, y_numerator, double_area
