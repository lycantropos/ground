from fractions import Fraction
from typing import (Callable,
                    Sequence,
                    Tuple,
                    Type)

from ground.core.hints import (Coordinate,
                               Point)


def centroid(point_cls: Type[Point],
             vertices: Sequence[Point],
             inverse: Callable[[int], Fraction] = Fraction(1).__truediv__
             ) -> Point:
    x_numerator, y_numerator, double_area = centroid_components(vertices)
    inverted_divisor = inverse(3 * double_area)
    return point_cls(x_numerator * inverted_divisor,
                     y_numerator * inverted_divisor)


def centroid_components(vertices: Sequence[Point]
                        ) -> Tuple[Coordinate, Coordinate, Coordinate]:
    double_area = x_numerator = y_numerator = 0
    prev_vertex = vertices[-1]
    prev_x, prev_y = prev_vertex.x, prev_vertex.y
    for vertex in vertices:
        x, y = vertex.x, vertex.y
        area_component = prev_x * y - prev_y * x
        double_area += area_component
        x_numerator += (prev_x + x) * area_component
        y_numerator += (prev_y + y) * area_component
        prev_x, prev_y = x, y
    return x_numerator, y_numerator, double_area