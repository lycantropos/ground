from collections import abc
from typing import (Sequence,
                    Tuple)

from hypothesis import given

from ground.base import Context
from ground.hints import Point
from tests.utils import (equivalence,
                         is_point,
                         permute,
                         to_contour_vertices_orientation)
from . import strategies


@given(strategies.contexts_with_points_lists)
def test_basic(context_with_points: Tuple[Context, Sequence[Point]]) -> None:
    context, points = context_with_points

    result = context.points_convex_hull(points)

    assert isinstance(result, abc.Sequence)
    assert all(map(is_point, result))


@given(strategies.contexts_with_points_lists, strategies.indices)
def test_permutations(context_with_points: Tuple[Context, Sequence[Point]],
                      index: int) -> None:
    context, points = context_with_points

    result = context.points_convex_hull(points)

    assert result == context.points_convex_hull(permute(points, index))


@given(strategies.contexts_with_empty_lists)
def test_basic(context_with_points: Tuple[Context, Sequence[Point]]
               ) -> None:
    context, points = context_with_points

    result = context.points_convex_hull(points)

    assert len(result) == 0


@given(strategies.contexts_with_non_empty_points_lists)
def test_step(context_with_points: Tuple[Context, Sequence[Point]]) -> None:
    context, points = context_with_points
    point, *rest_points = points

    result = context.points_convex_hull(rest_points)
    next_result = context.points_convex_hull(points)

    result_orientation = to_contour_vertices_orientation(result, context)
    assert equivalence(
            point in result
            or (len(result) > 1
                and any(context.segment_contains_point(
                            context.segment_cls(result[index - 1],
                                                result[index]), point)
                        for index in range(len(result))))
            or (len(result) > 2
                and all(context.angle_orientation(result[index - 1],
                                                  result[index], point)
                        is result_orientation
                        for index in range(len(result)))),
            result == next_result)
