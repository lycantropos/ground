from typing import (Sequence,
                    Tuple,
                    Type)

from ground.core.hints import (Contour,
                               Point,
                               Scalar)
from ground.core.primitive import rationalize


def centroid(contour: Contour, point_cls: Type[Point]) -> Point:
    x_numerator, y_numerator, double_area = centroid_components(
            contour.vertices)
    inverted_divisor = 1 / (3 * double_area)
    return point_cls(x_numerator * inverted_divisor,
                     y_numerator * inverted_divisor)


def centroid_components(vertices: Sequence[Point]
                        ) -> Tuple[Scalar, Scalar, Scalar]:
    double_area = x_numerator = y_numerator = 0
    prev_vertex = vertices[-1]
    prev_x, prev_y = rationalize(prev_vertex.x), rationalize(prev_vertex.y)
    for vertex in vertices:
        x, y = rationalize(vertex.x), rationalize(vertex.y)
        area_component = prev_x * y - prev_y * x
        double_area += area_component
        x_numerator += (prev_x + x) * area_component
        y_numerator += (prev_y + y) * area_component
        prev_x, prev_y = x, y
    return x_numerator, y_numerator, double_area
