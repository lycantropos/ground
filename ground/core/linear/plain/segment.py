from typing import Type

from ground.core.arithmetic import robust_divide
from ground.core.enums import Relation
from ground.core.hints import (Point,
                               QuaternaryPointFunction)


def contains_point(start: Point,
                   end: Point,
                   point: Point,
                   cross_product: QuaternaryPointFunction) -> bool:
    return (point == start or point == end
            or (bounding_box_contains_point(start, end, point)
                and not cross_product(start, end, start, point)))


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
        scale = robust_divide(cross_product(first_start, second_start,
                                            second_start, second_end),
                              cross_product(first_start, first_end,
                                            second_start, second_end))
        return point_cls(first_start.x + (first_end.x - first_start.x) * scale,
                         first_start.y + (first_end.y - first_start.y) * scale)


def relate(test_start: Point,
           test_end: Point,
           goal_start: Point,
           goal_end: Point,
           cross_product: QuaternaryPointFunction) -> Relation:
    if test_start > test_end:
        test_start, test_end = test_end, test_start
    if goal_start > goal_end:
        goal_start, goal_end = goal_end, goal_start
    starts_equal = test_start == goal_start
    ends_equal = test_end == goal_end
    if starts_equal and ends_equal:
        return Relation.EQUAL
    test_start_cross_product = cross_product(goal_end, goal_start, goal_end,
                                             test_start)
    test_end_cross_product = cross_product(goal_end, goal_start, goal_end,
                                           test_end)
    if test_start_cross_product and test_end_cross_product:
        if (test_start_cross_product > 0) is (test_end_cross_product > 0):
            return Relation.DISJOINT
        else:
            goal_start_cross_product = cross_product(test_start, test_end,
                                                     test_start, goal_start)
            goal_end_cross_product = cross_product(test_start, test_end,
                                                   test_start, goal_end)
            if goal_start_cross_product and goal_end_cross_product:
                return (Relation.DISJOINT
                        if ((goal_start_cross_product > 0)
                            is (goal_end_cross_product > 0))
                        else Relation.CROSS)
            elif goal_start_cross_product:
                return (Relation.TOUCH
                        if test_start < goal_end < test_end
                        else Relation.DISJOINT)
            elif goal_end_cross_product:
                return (Relation.TOUCH
                        if test_start < goal_start < test_end
                        else Relation.DISJOINT)
    elif test_start_cross_product:
        return (Relation.TOUCH
                if goal_start <= test_end <= goal_end
                else Relation.DISJOINT)
    elif test_end_cross_product:
        return (Relation.TOUCH
                if goal_start <= test_start <= goal_end
                else Relation.DISJOINT)
    elif starts_equal:
        return (Relation.COMPONENT
                if test_end < goal_end
                else Relation.COMPOSITE)
    elif ends_equal:
        return (Relation.COMPOSITE
                if test_start < goal_start
                else Relation.COMPONENT)
    elif test_start == goal_end or test_end == goal_start:
        return Relation.TOUCH
    elif goal_start < test_start < goal_end:
        return (Relation.COMPONENT
                if test_end < goal_end
                else Relation.OVERLAP)
    elif test_start < goal_start < test_end:
        return (Relation.COMPOSITE
                if goal_end < test_end
                else Relation.OVERLAP)
    else:
        return Relation.DISJOINT


def bounding_box_contains_point(start: Point, end: Point, point: Point
                                ) -> bool:
    start_x, start_y, end_x, end_y = start.x, start.y, end.x, end.y
    min_x, max_x = (start_x, end_x) if start_x < end_x else (end_x, start_x)
    min_y, max_y = (start_y, end_y) if start_y < end_y else (end_y, start_y)
    return min_x <= point.x <= max_x and min_y <= point.y <= max_y
