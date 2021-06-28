from typing import (Sequence,
                    Tuple,
                    Type)

from cfractions import Fraction
from shewchuk import Expansion

from ground.core.hints import (Contour,
                               Point)
from ground.core.robust import to_cross_product


def centroid(contour: Contour,
             point_cls: Type[Point],
             third: Fraction = Fraction(1, 3)) -> Point:
    x_numerator, y_numerator, double_area = centroid_components(
            contour.vertices)
    inverted_denominator = third / double_area
    return point_cls(x_numerator * inverted_denominator,
                     y_numerator * inverted_denominator)


def centroid_components(vertices: Sequence[Point]
                        ) -> Tuple[Expansion, Expansion, Expansion]:
    double_area = x_numerator = y_numerator = Expansion()
    prev = vertices[-1]
    prev_x, prev_y = prev.x, prev.y
    for vertex in vertices:
        x, y = vertex.x, vertex.y
        area_component = to_cross_product(prev_x, prev_y, x, y)
        double_area = double_area + area_component
        x_numerator = x_numerator + area_component * (prev_x + x)
        y_numerator = y_numerator + area_component * (prev_y + y)
        prev_x, prev_y = x, y
    return x_numerator, y_numerator, double_area
