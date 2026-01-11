from collections import abc
from collections.abc import Sequence

from hypothesis import given

from ground.context import Context
from ground.hints import Point
from tests.hints import ScalarT
from tests.utils import equivalence, permute, to_contour_vertices_orientation

from . import strategies


@given(strategies.contexts_with_points_lists)
def test_basic(
    context_with_points: tuple[Context[ScalarT], Sequence[Point[ScalarT]]],
) -> None:
    context, points = context_with_points

    result = context.points_convex_hull(points)

    assert isinstance(result, abc.Sequence)
    assert [
        element
        for element in result
        if not isinstance(element, context.point_cls)
    ] == []


@given(strategies.contexts_with_points_lists, strategies.indices)
def test_permutations(
    context_with_points: tuple[Context[ScalarT], Sequence[Point[ScalarT]]],
    index: int,
) -> None:
    context, points = context_with_points

    result = context.points_convex_hull(points)

    assert result == context.points_convex_hull(permute(points, index))


@given(strategies.contexts_with_empty_lists)
def test_empty_list(
    context_with_points: tuple[Context[ScalarT], Sequence[Point[ScalarT]]],
) -> None:
    context, points = context_with_points

    result = context.points_convex_hull(points)

    assert len(result) == 0


@given(strategies.contexts_with_non_empty_points_lists)
def test_step(
    context_with_points: tuple[Context[ScalarT], Sequence[Point[ScalarT]]],
) -> None:
    context, points = context_with_points
    point, *rest_points = points

    result = context.points_convex_hull(rest_points)
    next_result = context.points_convex_hull(points)

    result_orientation = to_contour_vertices_orientation(result, context)
    assert equivalence(
        point in result
        or (
            len(result) > 1
            and any(
                context.segment_contains_point(
                    context.segment_cls(result[index - 1], result[index]),
                    point,
                )
                for index in range(len(result))
            )
        )
        or (
            len(result) > 2
            and all(
                context.angle_orientation(
                    result[index - 1], result[index], point
                )
                is result_orientation
                for index in range(len(result))
            )
        ),
        result == next_result,
    )
