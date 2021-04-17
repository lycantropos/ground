from itertools import permutations
from typing import (Sequence,
                    Tuple)

from hypothesis import given

from ground.base import Context
from ground.hints import Point
from tests.utils import (is_box,
                         permute,
                         reverse_box_coordinates,
                         reverse_points,
                         reverse_points_coordinates)
from . import strategies


@given(strategies.contexts_with_points_sequences)
def test_basic(context_with_points: Tuple[Context, Sequence[Point]]) -> None:
    context, points = context_with_points

    result = context.points_box(points)

    assert is_box(result)


@given(strategies.contexts_with_points_sequences)
def test_reversals(context_with_points: Tuple[Context, Sequence[Point]]
                   ) -> None:
    context, points = context_with_points

    result = context.points_box(points)

    assert result == context.points_box(reverse_points(points))
    assert result == reverse_box_coordinates(context.points_box(
            reverse_points_coordinates(points)))


@given(strategies.contexts_with_points_sequences)
def test_permutations(context_with_points: Tuple[Context, Sequence[Point]]
                      ) -> None:
    context, points = context_with_points

    result = context.points_box(points)

    assert all(context.points_box(permute(points, permutation))
               == result
               for permutation in permutations(range(len(points))))
