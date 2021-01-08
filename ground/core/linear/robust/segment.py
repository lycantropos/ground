from fractions import Fraction
from typing import Type

from ground.core.hints import QuaternaryPointFunction
from ground.core.linear.plain import segment as plain_segment
from ground.core.vector.plain.cross import multiply as plain_cross_product
from ground.hints import Point

contains_point = plain_segment.contains_point


def intersect(cross_product: QuaternaryPointFunction,
              point_cls: Type[Point],
              first_start: Point,
              first_end: Point,
              second_start: Point,
              second_end: Point) -> Point:
    if contains_point(cross_product, first_start, first_end, second_start):
        return second_start
    elif contains_point(cross_product, first_start, first_end, second_end):
        return second_end
    elif contains_point(cross_product, second_start, second_end, first_start):
        return first_start
    elif contains_point(cross_product, second_start, second_end, first_end):
        return first_end
    else:
        def to_exact_point(point: Point) -> Point:
            return point_cls(Fraction(point.x), Fraction(point.y))

        first_start, first_end, second_start, second_end = (
            to_exact_point(first_start), to_exact_point(first_end),
            to_exact_point(second_start), to_exact_point(second_end))
        scale = (plain_cross_product(first_start, second_start, second_start,
                                     second_end)
                 / plain_cross_product(first_start, first_end, second_start,
                                       second_end))
        return point_cls(first_start.x + (first_end.x - first_start.x) * scale,
                         first_start.y + (first_end.y - first_start.y) * scale)


relate = plain_segment.relate
