from typing import (Sequence,
                    Tuple,
                    Type)

from ground.core.hints import (Contour,
                               Coordinate,
                               Point)
from .region import centroid_components as region_centroid_components


def centroid(border: Contour,
             holes: Sequence[Contour],
             point_cls: Type[Point]) -> Point:
    x_numerator, y_numerator, double_area = centroid_components(border, holes)
    inverted_denominator = 1 / (3 * double_area)
    return point_cls(x_numerator * inverted_denominator,
                     y_numerator * inverted_denominator)


def centroid_components(border: Contour,
                        holes: Sequence[Contour]
                        ) -> Tuple[Coordinate, Coordinate, Coordinate]:
    x_numerator, y_numerator, double_area = region_centroid_components(
            border.vertices)
    for hole in holes:
        (hole_x_numerator, hole_y_numerator,
         hole_double_area) = region_centroid_components(hole.vertices)
        x_numerator += hole_x_numerator
        y_numerator += hole_y_numerator
        double_area += hole_double_area
    return x_numerator, y_numerator, double_area
