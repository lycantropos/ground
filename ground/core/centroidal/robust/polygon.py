from fractions import Fraction
from typing import (Callable,
                    Sequence,
                    Tuple,
                    Type)

from ground.core.hints import (Contour,
                               Expansion,
                               Point)
from ground.core.shewchuk import sum_expansions
from .region import centroid_components as region_centroid_components


def centroid(point_cls: Type[Point],
             border: Contour,
             holes: Sequence[Contour],
             inverse: Callable[[int], Fraction] = Fraction(1).__truediv__
             ) -> Point:
    x_numerator, y_numerator, double_area = centroid_components(border, holes)
    inverted_denominator = inverse(3 * double_area[-1])
    return point_cls(x_numerator[-1] * inverted_denominator,
                     y_numerator[-1] * inverted_denominator)


def centroid_components(border: Contour,
                        holes: Sequence[Contour]
                        ) -> Tuple[Expansion, Expansion, Expansion]:
    x_numerator, y_numerator, double_area = region_centroid_components(
            border.vertices)
    for hole in holes:
        (hole_x_numerator, hole_y_numerator,
         hole_double_area) = region_centroid_components(hole.vertices)
        x_numerator, y_numerator, double_area = (
            sum_expansions(x_numerator, hole_x_numerator),
            sum_expansions(y_numerator, hole_y_numerator),
            sum_expansions(double_area, hole_double_area))
    return x_numerator, y_numerator, double_area
