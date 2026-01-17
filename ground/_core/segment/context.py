from collections.abc import Callable
from typing import Any, Generic, TypeAlias

from reprit import serializers
from reprit.base import generate_repr
from typing_extensions import Self

from ground._core.enums import Orientation, Relation
from ground._core.hints import HasRepr, Point, ScalarT, TernaryPointFunction

from . import plain

CollisionDetector: TypeAlias = Callable[
    [
        Point[ScalarT],
        Point[ScalarT],
        Point[ScalarT],
        Point[ScalarT],
        TernaryPointFunction[ScalarT, ScalarT],
    ],
    bool,
]
ContainmentChecker: TypeAlias = Callable[
    [
        Point[ScalarT],
        Point[ScalarT],
        Point[ScalarT],
        TernaryPointFunction[ScalarT, Orientation],
    ],
    bool,
]
Intersector: TypeAlias = Callable[
    [
        Point[ScalarT],
        Point[ScalarT],
        Point[ScalarT],
        Point[ScalarT],
        type[Point[ScalarT]],
        TernaryPointFunction[ScalarT, bool],
    ],
    Point[ScalarT],
]
Relater: TypeAlias = Callable[
    [
        Point[ScalarT],
        Point[ScalarT],
        Point[ScalarT],
        Point[ScalarT],
        TernaryPointFunction[ScalarT, Orientation],
    ],
    Relation,
]


class Context(HasRepr, Generic[ScalarT]):
    @staticmethod
    def collision_detector(
        first_start: Point[ScalarT],
        first_end: Point[ScalarT],
        second_start: Point[ScalarT],
        second_end: Point[ScalarT],
        orienteer: TernaryPointFunction[ScalarT, Orientation],
        /,
    ) -> bool:
        second_start_orientation = orienteer(
            first_start, first_end, second_start
        )
        if (
            second_start_orientation is Orientation.COLLINEAR
            and _bounding_box_contains_point(
                first_start, first_end, second_end
            )
        ):
            return True
        second_end_orientation = orienteer(first_start, first_end, second_end)
        if (
            second_end_orientation is Orientation.COLLINEAR
            and _bounding_box_contains_point(
                first_start, first_end, second_end
            )
        ):
            return True
        first_start_orientation = orienteer(
            second_start, second_end, first_start
        )
        if (
            first_start_orientation is Orientation.COLLINEAR
            and _bounding_box_contains_point(
                second_start, second_end, first_end
            )
        ):
            return True
        first_end_orientation = orienteer(second_start, second_end, first_end)
        return (
            first_end_orientation is Orientation.COLLINEAR
            and _bounding_box_contains_point(
                second_start, second_end, first_end
            )
        ) or (
            second_start_orientation is not second_end_orientation
            and first_start_orientation is not first_end_orientation
        )

    @staticmethod
    def containment_checker(
        start: Point[ScalarT],
        end: Point[ScalarT],
        point: Point[ScalarT],
        orienteer: TernaryPointFunction[ScalarT, Orientation],
        /,
    ) -> bool:
        return point in (start, end) or (
            _bounding_box_contains_point(start, end, point)
            and orienteer(start, end, point) is Orientation.COLLINEAR
        )

    @staticmethod
    def relater(
        test_start: Point[ScalarT],
        test_end: Point[ScalarT],
        goal_start: Point[ScalarT],
        goal_end: Point[ScalarT],
        orienteer: TernaryPointFunction[ScalarT, Orientation],
        /,
    ) -> Relation:
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
        if (
            test_start_orientation
            is not Orientation.COLLINEAR
            is not test_end_orientation
        ):
            if test_start_orientation is test_end_orientation:
                return Relation.DISJOINT
            goal_start_orientation = orienteer(
                test_start, test_end, goal_start
            )
            goal_end_orientation = orienteer(test_start, test_end, goal_end)
            if (
                goal_start_orientation
                is not Orientation.COLLINEAR
                is not goal_end_orientation
            ):
                return (
                    Relation.DISJOINT
                    if goal_start_orientation is goal_end_orientation
                    else Relation.CROSS
                )
            if goal_start_orientation is not Orientation.COLLINEAR:
                return (
                    Relation.TOUCH
                    if test_start < goal_end < test_end
                    else Relation.DISJOINT
                )
            return (
                Relation.TOUCH
                if test_start < goal_start < test_end
                else Relation.DISJOINT
            )
        if test_start_orientation is not Orientation.COLLINEAR:
            return (
                Relation.TOUCH
                if goal_start <= test_end <= goal_end
                else Relation.DISJOINT
            )
        if test_end_orientation is not Orientation.COLLINEAR:
            return (
                Relation.TOUCH
                if goal_start <= test_start <= goal_end
                else Relation.DISJOINT
            )
        if starts_equal:
            return (
                Relation.COMPONENT
                if test_end < goal_end
                else Relation.COMPOSITE
            )
        if ends_equal:
            return (
                Relation.COMPOSITE
                if test_start < goal_start
                else Relation.COMPONENT
            )
        if test_start == goal_end or test_end == goal_start:
            return Relation.TOUCH
        if goal_start < test_start < goal_end:
            return (
                Relation.COMPONENT if test_end < goal_end else Relation.OVERLAP
            )
        if test_start < goal_start < test_end:
            return (
                Relation.COMPOSITE if goal_end < test_end else Relation.OVERLAP
            )
        return Relation.DISJOINT

    @property
    def intersector(self, /) -> Intersector[ScalarT]:
        return self._intersector

    _intersector: Intersector[ScalarT]

    __slots__ = ('_intersector',)

    def __new__(cls, /, *, intersector: Intersector[ScalarT]) -> Self:
        self = super().__new__(cls)
        self._intersector = intersector
        return self

    __repr__ = generate_repr(
        __new__,
        argument_serializer=serializers.complex_,
        with_module_name=True,
    )


plain_context: Context[Any] = Context(intersector=plain.intersect)


def _bounding_box_contains_point(
    start: Point[ScalarT], end: Point[ScalarT], point: Point[ScalarT], /
) -> bool:
    start_x, start_y, end_x, end_y = start.x, start.y, end.x, end.y
    min_x, max_x = (start_x, end_x) if start_x < end_x else (end_x, start_x)
    min_y, max_y = (start_y, end_y) if start_y < end_y else (end_y, start_y)
    result = min_x <= point.x <= max_x and min_y <= point.y <= max_y
    assert isinstance(result, bool), result
    return result
