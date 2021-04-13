from typing import Type

from ground.core.hints import (Point,
                               QuaternaryPointFunction)
from ground.core.linear.plain import segment as plain_segment
from ground.core.primitive import to_rational_point
from ground.core.vector.plain.cross import multiply as plain_cross_product

contains_point = plain_segment.contains_point


def intersect(first_start: Point,
              first_end: Point,
              second_start: Point,
              second_end: Point,
              cross_product: QuaternaryPointFunction,
              point_cls: Type[Point]) -> Point:
    if contains_point(first_start, first_end, second_start, cross_product):
        return second_start
    elif contains_point(first_start, first_end, second_end, cross_product):
        return second_end
    elif contains_point(second_start, second_end, first_start, cross_product):
        return first_start
    elif contains_point(second_start, second_end, first_end, cross_product):
        return first_end
    else:
        first_start, first_end = (to_rational_point(first_start, point_cls),
                                  to_rational_point(first_end, point_cls))
        second_start, second_end = (to_rational_point(second_start, point_cls),
                                    to_rational_point(second_end, point_cls))
        scale = (plain_cross_product(first_start, second_start, second_start,
                                     second_end)
                 / plain_cross_product(first_start, first_end, second_start,
                                       second_end))
        return point_cls(first_start.x + (first_end.x - first_start.x) * scale,
                         first_start.y + (first_end.y - first_start.y) * scale)


relate = plain_segment.relate
