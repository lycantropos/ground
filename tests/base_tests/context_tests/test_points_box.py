from typing import (Sequence,
                    Tuple)

from hypothesis import given

from ground.base import Context
from ground.hints import Point
from tests.utils import (is_box,
                         permute,
                         reverse_box_coordinates,
                         reverse_sequence,
                         reverse_points_coordinates)
from . import strategies


@given(strategies.contexts_with_non_empty_points_lists)
def test_basic(context_with_points: Tuple[Context, Sequence[Point]]) -> None:
    context, points = context_with_points

    result = context.points_box(points)

    assert is_box(result)


@given(strategies.contexts_with_non_empty_points_lists)
def test_reversals(context_with_points: Tuple[Context, Sequence[Point]]
                   ) -> None:
    context, points = context_with_points

    result = context.points_box(points)

    assert result == context.points_box(reverse_sequence(points))
    assert result == reverse_box_coordinates(context.points_box(
            reverse_points_coordinates(points)))


@given(strategies.contexts_with_non_empty_points_lists, strategies.indices)
def test_permutations(context_with_points: Tuple[Context, Sequence[Point]],
                      index: int) -> None:
    context, points = context_with_points

    result = context.points_box(points)

    assert result == context.points_box(permute(points, index))
