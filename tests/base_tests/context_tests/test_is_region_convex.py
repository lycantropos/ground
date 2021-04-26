from typing import (Sequence,
                    Tuple)

from hypothesis import given

from ground.base import Context
from ground.hints import Point
from tests.utils import (reverse_sequence,
                         rotate_sequence)
from . import strategies


@given(strategies.contexts_with_vertices)
def test_basic(context_with_vertices: Tuple[Context, Sequence[Point]]) -> None:
    context, vertices = context_with_vertices

    result = context.is_region_convex(vertices)

    assert isinstance(result, bool)


@given(strategies.contexts_with_rational_vertices)
def test_reversals(context_with_vertices: Tuple[Context, Sequence[Point]]
                   ) -> None:
    context, vertices = context_with_vertices

    result = context.is_region_convex(vertices)

    assert result is context.is_region_convex(reverse_sequence(vertices))


@given(strategies.contexts_with_rational_vertices, strategies.indices)
def test_rotations(context_with_vertices: Tuple[Context, Sequence[Point]],
                   offset: int) -> None:
    context, vertices = context_with_vertices

    result = context.is_region_convex(vertices)

    assert result is context.is_region_convex(rotate_sequence(vertices,
                                                              offset))
