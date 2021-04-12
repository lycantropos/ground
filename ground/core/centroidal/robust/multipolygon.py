from fractions import Fraction
from typing import (Callable,
                    Sequence,
                    Tuple,
                    Type)

from ground.core.hints import (Expansion,
                               Point,
                               Polygon)
from ground.core.shewchuk import sum_expansions
from .polygon import centroid_components as polygon_centroid_components


def centroid(point_cls: Type[Point],
             polygons: Sequence[Polygon],
             inverse: Callable[[int], Fraction] = Fraction(1).__truediv__
             ) -> Point:
    x_numerator, y_numerator, double_area = centroid_components(polygons)
    inverted_denominator = inverse(3 * double_area[-1])
    return point_cls(x_numerator[-1] * inverted_denominator,
                     y_numerator[-1] * inverted_denominator)


def centroid_components(polygons: Sequence[Polygon]
                        ) -> Tuple[Expansion, Expansion, Expansion]:
    iterator = iter(polygons)
    polygon = next(iterator)
    x_numerator, y_numerator, double_area = polygon_centroid_components(
            polygon.border, polygon.holes)
    for polygon in iterator:
        (polygon_x_numerator, polygon_y_numerator,
         polygon_double_area) = polygon_centroid_components(polygon.border,
                                                            polygon.holes)
        x_numerator, y_numerator, double_area = (
            sum_expansions(x_numerator, polygon_x_numerator),
            sum_expansions(y_numerator, polygon_y_numerator),
            sum_expansions(double_area, polygon_double_area))
    return x_numerator, y_numerator, double_area
