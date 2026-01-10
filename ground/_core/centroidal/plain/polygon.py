from collections.abc import Sequence

from ground._core.hints import Contour, Point, Polygon, ScalarFactory, ScalarT

from .region import centroid_components as region_centroid_components


def centroid(
    polygon: Polygon[ScalarT],
    coordinate_factory: ScalarFactory[ScalarT],
    point_cls: type[Point[ScalarT]],
    /,
) -> Point[ScalarT]:
    x_numerator, y_numerator, double_area = centroid_components(
        polygon.border, polygon.holes, coordinate_factory
    )
    divisor = coordinate_factory(3) * double_area
    return point_cls(x_numerator / divisor, y_numerator / divisor)


def centroid_components(
    border: Contour[ScalarT],
    holes: Sequence[Contour[ScalarT]],
    coordinate_factory: ScalarFactory[ScalarT],
    /,
) -> tuple[ScalarT, ScalarT, ScalarT]:
    x_numerator, y_numerator, double_area = region_centroid_components(
        border.vertices, coordinate_factory
    )
    for hole in holes:
        (hole_x_numerator, hole_y_numerator, hole_double_area) = (
            region_centroid_components(hole.vertices, coordinate_factory)
        )
        x_numerator += hole_x_numerator
        y_numerator += hole_y_numerator
        double_area += hole_double_area
    return x_numerator, y_numerator, double_area
