from fractions import Fraction
from typing import (Sequence,
                    Type)

from ground.hints import Point


def centroid(point_cls: Type[Point],
             vertices: Sequence[Point]) -> Point:
    double_area = x_numerator = y_numerator = 0
    prev_vertex = vertices[-1]
    prev_x, prev_y = Fraction(prev_vertex.x), Fraction(prev_vertex.y)
    for vertex in vertices:
        x, y = Fraction(vertex.x), Fraction(vertex.y)
        area_component = prev_x * y - prev_y * x
        double_area += area_component
        x_numerator += (prev_x + x) * area_component
        y_numerator += (prev_y + y) * area_component
        prev_x, prev_y = x, y
    inverted_divisor = 1 / (3 * double_area)
    return point_cls(x_numerator * inverted_divisor,
                     y_numerator * inverted_divisor)
