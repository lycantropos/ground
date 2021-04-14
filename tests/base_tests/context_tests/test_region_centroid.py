from typing import (Sequence,
                    Tuple)

from hypothesis import given

from ground.base import Context
from ground.hints import Point
from tests.utils import (is_point,
                         rotate_sequence)
from . import strategies


@given(strategies.contexts_with_vertices)
def test_basic(context_with_vertices: Tuple[Context, Sequence[Point]]) -> None:
    context, vertices = context_with_vertices

    result = context.region_centroid(vertices)

    assert is_point(result)


@given(strategies.contexts_with_rational_vertices)
def test_rotations(context_with_vertices: Tuple[Context, Sequence[Point]]
                   ) -> None:
    context, vertices = context_with_vertices

    result = context.region_centroid(vertices)

    assert all(context.region_centroid(rotate_sequence(vertices, offset))
               == result
               for offset in range(len(vertices)))
