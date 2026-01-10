from collections.abc import Sequence

from ground._core.hints import (
    Multipolygon,
    Point,
    Polygon,
    ScalarFactory,
    ScalarT,
)

from .polygon import centroid_components as polygon_centroid_components


def centroid(
    multipolygon: Multipolygon[ScalarT],
    coordinate_factory: ScalarFactory[ScalarT],
    point_cls: type[Point[ScalarT]],
    /,
) -> Point[ScalarT]:
    x_numerator, y_numerator, double_area = centroid_components(
        multipolygon.polygons, coordinate_factory
    )
    divisor = coordinate_factory(3) * double_area
    return point_cls(x_numerator / divisor, y_numerator / divisor)


def centroid_components(
    polygons: Sequence[Polygon[ScalarT]],
    coordinate_factory: ScalarFactory[ScalarT],
) -> tuple[ScalarT, ScalarT, ScalarT]:
    iterator = iter(polygons)
    polygon = next(iterator)
    x_numerator, y_numerator, double_area = polygon_centroid_components(
        polygon.border, polygon.holes, coordinate_factory
    )
    for polygon in iterator:
        (polygon_x_numerator, polygon_y_numerator, polygon_double_area) = (
            polygon_centroid_components(
                polygon.border, polygon.holes, coordinate_factory
            )
        )
        x_numerator += polygon_x_numerator
        y_numerator += polygon_y_numerator
        double_area += polygon_double_area
    return x_numerator, y_numerator, double_area
