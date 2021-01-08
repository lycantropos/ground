from fractions import Fraction
from typing import Type

from ground.core.enums import Relation
from ground.core.hints import QuaternaryPointFunction
from ground.hints import Point


def contains_point(cross_product: QuaternaryPointFunction,
                   start: Point,
                   end: Point,
                   point: Point) -> bool:
    return (point == start or point == end
            or (_bounding_box_contains(start, end, point)
                and not cross_product(start, end, start, point)))


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
        scale = (cross_product(first_start, second_start, second_start,
                               second_end)
                 * (Fraction(1)
                    / cross_product(first_start, first_end, second_start,
                                    second_end)))
        return point_cls(first_start.x + (first_end.x - first_start.x) * scale,
                         first_start.y + (first_end.y - first_start.y) * scale)


def relate(cross_product: QuaternaryPointFunction,
           first_start: Point,
           first_end: Point,
           second_start: Point,
           second_end: Point) -> Relation:
    if first_start > first_end:
        first_start, first_end = first_end, first_start
    if second_start > second_end:
        second_start, second_end = second_end, second_start
    starts_equal = first_start == second_start
    ends_equal = first_end == second_end
    if starts_equal and ends_equal:
        return Relation.EQUAL
    first_start_cross_product = cross_product(second_end, second_start,
                                              second_end, first_start)
    first_end_cross_product = cross_product(second_end, second_start,
                                            second_end, first_end)
    if first_start_cross_product and first_end_cross_product:
        if (first_start_cross_product > 0) is (first_end_cross_product > 0):
            return Relation.DISJOINT
        else:
            second_start_cross_product = cross_product(first_start, first_end,
                                                       first_start,
                                                       second_start)
            second_end_cross_product = cross_product(first_start, first_end,
                                                     first_start, second_end)
            if second_start_cross_product and second_end_cross_product:
                return (Relation.DISJOINT
                        if ((second_start_cross_product > 0)
                            is (second_end_cross_product > 0))
                        else Relation.CROSS)
            elif second_start_cross_product:
                return (Relation.TOUCH
                        if first_start < second_end < first_end
                        else Relation.DISJOINT)
            elif second_end_cross_product:
                return (Relation.TOUCH
                        if first_start < second_start < first_end
                        else Relation.DISJOINT)
    elif first_start_cross_product:
        return (Relation.TOUCH
                if second_start <= first_end <= second_end
                else Relation.DISJOINT)
    elif first_end_cross_product:
        return (Relation.TOUCH
                if second_start <= first_start <= second_end
                else Relation.DISJOINT)
    elif starts_equal:
        return (Relation.COMPOSITE
                if first_end < second_end
                else Relation.COMPONENT)
    elif ends_equal:
        return (Relation.COMPOSITE
                if first_start < second_start
                else Relation.COMPONENT)
    elif first_start == second_end or first_end == second_start:
        return Relation.TOUCH
    elif (second_start < first_start < second_end
          or first_start < second_start < first_end):
        return Relation.OVERLAP
    else:
        return Relation.DISJOINT


def _bounding_box_contains(start: Point, end: Point, point: Point) -> bool:
    start_x, start_y = start.x, start.y
    end_x, end_y = end.x, end.y
    x_min, x_max = (start_x, end_x) if start_x < end_x else (end_x, start_x)
    y_min, y_max = (start_y, end_y) if start_y < end_y else (end_y, start_y)
    return x_min <= point.x <= x_max and y_min <= point.y <= y_max
