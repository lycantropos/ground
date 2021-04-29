from typing import (Callable,
                    Type)

from ground.core.hints import (Contour,
                               Point,
                               Scalar)
from ground.core.primitive import rationalize


def centroid(contour: Contour,
             point_cls: Type[Point],
             sqrt: Callable[[Scalar], Scalar]) -> Point:
    vertices = contour.vertices
    accumulated_x = accumulated_y = accumulated_length = 0
    vertex = vertices[-1]
    start_x, start_y = rationalize(vertex.x), rationalize(vertex.y)
    for vertex in vertices:
        end_x, end_y = rationalize(vertex.x), rationalize(vertex.y)
        length = sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2)
        accumulated_x += (start_x + end_x) * length
        accumulated_y += (start_y + end_y) * length
        accumulated_length += length
        start_x, start_y = end_x, end_y
    inverted_divisor = 1 / (2 * accumulated_length)
    return point_cls(accumulated_x * inverted_divisor,
                     accumulated_y * inverted_divisor)
