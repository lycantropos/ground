from fractions import Fraction
from typing import (Sequence,
                    Tuple,
                    Type)

from ground.core.hints import (Expansion,
                               Multipolygon,
                               Point,
                               Polygon)
from ground.core.shewchuk import sum_expansions
from .polygon import centroid_components as polygon_centroid_components


def centroid(multipolygon: Multipolygon,
             point_cls: Type[Point],
             third: Fraction = Fraction(1, 3)) -> Point:
    x_numerator, y_numerator, double_area = centroid_components(
            multipolygon.polygons)
    inverted_denominator = third / double_area[-1]
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
