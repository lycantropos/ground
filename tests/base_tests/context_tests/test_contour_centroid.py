from typing import (Sequence,
                    Tuple)

from hypothesis import given

from ground.base import Context
from tests.utils import (Point,
                         is_point,
                         reverse_sequence,
                         rotate_sequence)
from . import strategies


@given(strategies.contexts_with_vertices)
def test_basic(context_with_vertices: Tuple[Context, Sequence[Point]]) -> None:
    context, vertices = context_with_vertices

    result = context.contour_centroid(vertices)

    assert is_point(result)


@given(strategies.contexts_with_rational_vertices)
def test_reversals(context_with_vertices: Tuple[Context, Sequence[Point]]
                   ) -> None:
    context, vertices = context_with_vertices

    result = context.contour_centroid(vertices)

    assert result == context.contour_centroid(reverse_sequence(vertices))


@given(strategies.contexts_with_rational_vertices, strategies.indices)
def test_rotations(context_with_vertices: Tuple[Context, Sequence[Point]],
                   offset: int) -> None:
    context, vertices = context_with_vertices

    result = context.contour_centroid(vertices)

    assert result == context.contour_centroid(rotate_sequence(vertices,
                                                              offset))
