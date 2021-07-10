from typing import (Callable,
                    Type)

from reprit import serializers
from reprit.base import generate_repr

from ground.core.enums import (Orientation,
                               Relation)
from ground.core.hints import (Point,
                               TernaryPointFunction)
from . import (exact,
               plain)

CollisionDetector = Callable[[Point, Point, Point, Point,
                              TernaryPointFunction], bool]
ContainmentChecker = Callable[[Point, Point, Point,
                               TernaryPointFunction[Orientation]], bool]
Intersector = Callable[[Point, Point, Point, Point, Type[Point],
                        TernaryPointFunction[bool]], Point]
Relater = Callable[[Point, Point, Point, Point,
                    TernaryPointFunction[Orientation]], Relation]


class Context:
    @staticmethod
    def collision_detector(first_start: Point,
                           first_end: Point,
                           second_start: Point,
                           second_end: Point,
                           orienteer: TernaryPointFunction[Orientation]
                           ) -> bool:
        second_start_orientation = orienteer(first_start, first_end,
                                             second_start)
        if (second_start_orientation is Orientation.COLLINEAR
                and _bounding_box_contains_point(first_start, first_end,
                                                 second_end)):
            return True
        second_end_orientation = orienteer(first_start, first_end, second_end)
        if (second_end_orientation is Orientation.COLLINEAR
                and _bounding_box_contains_point(first_start, first_end,
                                                 second_end)):
            return True
        first_start_orientation = orienteer(second_start, second_end,
                                            first_start)
        if (first_start_orientation is Orientation.COLLINEAR
                and _bounding_box_contains_point(second_start, second_end,
                                                 first_end)):
            return True
        first_end_orientation = orienteer(second_start, second_end, first_end)
        return (first_end_orientation is Orientation.COLLINEAR
                and _bounding_box_contains_point(second_start, second_end,
                                                 first_end)
                or (second_start_orientation is not second_end_orientation
                    and first_start_orientation is not first_end_orientation))

    @staticmethod
    def containment_checker(start: Point,
                            end: Point,
                            point: Point,
                            orienteer: TernaryPointFunction[Orientation]
                            ) -> bool:
        return (point == start or point == end
                or (_bounding_box_contains_point(start, end, point)
                    and orienteer(start, end, point) is Orientation.COLLINEAR))

    @staticmethod
    def relater(test_start: Point,
                test_end: Point,
                goal_start: Point,
                goal_end: Point,
                orienteer: TernaryPointFunction[Orientation]) -> Relation:
        if test_start > test_end:
            test_start, test_end = test_end, test_start
        if goal_start > goal_end:
            goal_start, goal_end = goal_end, goal_start
        starts_equal = test_start == goal_start
        ends_equal = test_end == goal_end
        if starts_equal and ends_equal:
            return Relation.EQUAL
        test_start_orientation = orienteer(goal_end, goal_start, test_start)
        test_end_orientation = orienteer(goal_end, goal_start, test_end)
        if (test_start_orientation
                is not Orientation.COLLINEAR
                is not test_end_orientation):
            if (test_start_orientation > 0) is (test_end_orientation > 0):
                return Relation.DISJOINT
            else:
                goal_start_orientation = orienteer(test_start, test_end,
                                                   goal_start)
                goal_end_orientation = orienteer(test_start, test_end,
                                                 goal_end)
                if (goal_start_orientation
                        is not Orientation.COLLINEAR
                        is not goal_end_orientation):
                    return (Relation.DISJOINT
                            if ((goal_start_orientation > 0)
                                is (goal_end_orientation > 0))
                            else Relation.CROSS)
                elif goal_start_orientation is not Orientation.COLLINEAR:
                    return (Relation.TOUCH
                            if test_start < goal_end < test_end
                            else Relation.DISJOINT)
                elif goal_end_orientation is not Orientation.COLLINEAR:
                    return (Relation.TOUCH
                            if test_start < goal_start < test_end
                            else Relation.DISJOINT)
        elif test_start_orientation is not Orientation.COLLINEAR:
            return (Relation.TOUCH
                    if goal_start <= test_end <= goal_end
                    else Relation.DISJOINT)
        elif test_end_orientation is not Orientation.COLLINEAR:
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

    @property
    def intersector(self) -> Intersector:
        return self._intersector

    __slots__ = '_intersector',

    def __init__(self, intersector: Intersector) -> None:
        self._intersector = intersector

    __repr__ = generate_repr(__init__,
                             argument_serializer=serializers.complex_,
                             with_module_name=True)


exact_context = Context(exact.intersect)
plain_context = Context(plain.intersect)


def _bounding_box_contains_point(start: Point, end: Point, point: Point
                                 ) -> bool:
    start_x, start_y, end_x, end_y = start.x, start.y, end.x, end.y
    min_x, max_x = (start_x, end_x) if start_x < end_x else (end_x, start_x)
    min_y, max_y = (start_y, end_y) if start_y < end_y else (end_y, start_y)
    return min_x <= point.x <= max_x and min_y <= point.y <= max_y
