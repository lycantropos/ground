from typing import (Sequence,
                    Tuple,
                    Type)

from ground.core.hints import (Coordinate,
                               Point,
                               Polygon)
from .polygon import centroid_components as polygon_centroid_components


def centroid(point_cls: Type[Point],
             polygons: Sequence[Polygon]) -> Point:
    x_numerator, y_numerator, double_area = centroid_components(polygons)
    inverted_denominator = 1 / (3 * double_area)
    return point_cls(x_numerator * inverted_denominator,
                     y_numerator * inverted_denominator)


def centroid_components(polygons: Sequence[Polygon]
                        ) -> Tuple[Coordinate, Coordinate, Coordinate]:
    iterator = iter(polygons)
    polygon = next(iterator)
    x_numerator, y_numerator, double_area = polygon_centroid_components(
            polygon.border, polygon.holes)
    for polygon in iterator:
        (polygon_x_numerator, polygon_y_numerator,
         polygon_double_area) = polygon_centroid_components(polygon.border,
                                                            polygon.holes)
        x_numerator += polygon_x_numerator
        y_numerator += polygon_y_numerator
        double_area += polygon_double_area
    return x_numerator, y_numerator, double_area
