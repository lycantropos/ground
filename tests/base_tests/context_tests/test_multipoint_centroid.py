from itertools import permutations
from typing import Sequence, Tuple

from hypothesis import given

from ground.base import Context
from ground.hints import Point
from tests.utils import (is_point,
                         permute)
from . import strategies


@given(strategies.contexts_with_points)
def test_basic(context_with_points: Tuple[Context, Sequence[Point]]) -> None:
    context, points = context_with_points

    result = context.multipoint_centroid(points)

    assert is_point(result)


@given(strategies.contexts_with_rational_points)
def test_permutations(context_with_points: Tuple[Context, Sequence[Point]]
                      ) -> None:
    context, points = context_with_points

    result = context.multipoint_centroid(points)

    assert all(context.multipoint_centroid(permute(points, permutation))
               == result
               for permutation in permutations(range(len(points))))
