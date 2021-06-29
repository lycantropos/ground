from typing import Type

from ground.core.hints import (Point,
                               QuaternaryPointFunction,
                               TernaryPointFunction)
from ground.core.primitive import to_rational_point
from ground.core.vector.plain import cross


def intersect(first_start: Point,
              first_end: Point,
              second_start: Point,
              second_end: Point,
              point_cls: Type[Point],
              containment_checker: TernaryPointFunction[bool],
              cross_product: QuaternaryPointFunction = cross.multiply
              ) -> Point:
    if containment_checker(first_start, first_end, second_start):
        return second_start
    elif containment_checker(first_start, first_end, second_end):
        return second_end
    elif containment_checker(second_start, second_end, first_start):
        return first_start
    elif containment_checker(second_start, second_end, first_end):
        return first_end
    else:
        first_start, first_end = (to_rational_point(first_start, point_cls),
                                  to_rational_point(first_end, point_cls))
        second_start, second_end = (to_rational_point(second_start, point_cls),
                                    to_rational_point(second_end, point_cls))
        scale = (cross_product(first_start, second_start, second_start,
                               second_end)
                 / cross_product(first_start, first_end, second_start,
                                 second_end))
        return point_cls(first_start.x + (first_end.x - first_start.x) * scale,
                         first_start.y + (first_end.y - first_start.y) * scale)
