from typing import (Sequence,
                    Tuple)

from hypothesis import given

from ground.base import Context
from ground.hints import Point
from tests.utils import (is_point,
                         permute,
                         reverse_sequence)
from . import strategies


@given(strategies.contexts_with_points_sequences)
def test_basic(context_with_points: Tuple[Context, Sequence[Point]]) -> None:
    context, points = context_with_points

    result = context.multipoint_centroid(points)

    assert is_point(result)


@given(strategies.contexts_with_rational_points_sequences)
def test_reversals(context_with_points: Tuple[Context, Sequence[Point]]
                   ) -> None:
    context, points = context_with_points

    result = context.multipoint_centroid(points)

    assert result == context.multipoint_centroid(reverse_sequence(points))


@given(strategies.contexts_with_rational_points_sequences, strategies.indices)
def test_permutations(context_with_points: Tuple[Context, Sequence[Point]],
                      index: int) -> None:
    context, points = context_with_points

    result = context.multipoint_centroid(points)

    assert result == context.multipoint_centroid(permute(points, index))
