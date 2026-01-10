from collections.abc import Sequence

from ground._core.hints import Contour, Point, ScalarFactory, ScalarT


def centroid(
    contour: Contour[ScalarT],
    coordinate_factory: ScalarFactory[ScalarT],
    point_cls: type[Point[ScalarT]],
    /,
) -> Point[ScalarT]:
    x_numerator, y_numerator, double_area = centroid_components(
        contour.vertices, coordinate_factory
    )
    divisor = coordinate_factory(3) * double_area
    return point_cls(x_numerator / divisor, y_numerator / divisor)


def centroid_components(
    vertices: Sequence[Point[ScalarT]],
    coordinate_factory: ScalarFactory[ScalarT],
) -> tuple[ScalarT, ScalarT, ScalarT]:
    double_area = x_numerator = y_numerator = coordinate_factory(0)
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
