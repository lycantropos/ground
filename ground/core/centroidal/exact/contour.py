from fractions import Fraction
from typing import (Callable,
                    Sequence,
                    Type)

from ground.core.hints import (Coordinate,
                               Point)


def centroid(point_cls: Type[Point],
             vertices: Sequence[Point],
             sqrt: Callable[[Coordinate], Coordinate]) -> Point:
    accumulated_x = accumulated_y = accumulated_length = 0
    vertex = vertices[-1]
    start_x, start_y = Fraction(vertex.x), Fraction(vertex.y)
    for vertex in vertices:
        end_x, end_y = Fraction(vertex.x), Fraction(vertex.y)
        length = sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2)
        accumulated_x += (start_x + end_x) * length
        accumulated_y += (start_y + end_y) * length
        accumulated_length += length
        start_x, start_y = end_x, end_y
    inverted_divisor = 1 / (2 * accumulated_length)
    return point_cls(accumulated_x * inverted_divisor,
                     accumulated_y * inverted_divisor)
