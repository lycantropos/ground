from collections.abc import Callable

from ground._core.hints import Contour, Point, ScalarFactory, ScalarT
from ground._core.primitive import square


def centroid(
    contour: Contour[ScalarT],
    coordinate_factory: ScalarFactory[ScalarT],
    point_cls: type[Point[ScalarT]],
    sqrt: Callable[[ScalarT], ScalarT],
    /,
) -> Point[ScalarT]:
    vertices = contour.vertices
    accumulated_x = accumulated_y = accumulated_length = coordinate_factory(0)
    vertex = vertices[-1]
    start_x, start_y = vertex.x, vertex.y
    for vertex in vertices:
        end_x, end_y = vertex.x, vertex.y
        length = sqrt(square(end_x - start_x) + square(end_y - start_y))
        accumulated_x += (start_x + end_x) * length
        accumulated_y += (start_y + end_y) * length
        accumulated_length += length
        start_x, start_y = end_x, end_y
    divisor = coordinate_factory(2) * accumulated_length
    return point_cls(accumulated_x / divisor, accumulated_y / divisor)
