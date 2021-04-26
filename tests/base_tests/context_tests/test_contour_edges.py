from collections import abc
from typing import (Sequence,
                    Tuple)

from hypothesis import given

from ground.base import Context
from ground.hints import Point
from tests.utils import (is_segment,
                         rotate_sequence)
from . import strategies


@given(strategies.contexts_with_vertices)
def test_basic(context_with_vertices: Tuple[Context, Sequence[Point]]) -> None:
    context, vertices = context_with_vertices

    result = context.contour_edges(vertices)

    assert isinstance(result, abc.Sequence)
    assert len(result) == len(vertices)
    assert all(is_segment(element) for element in result)


@given(strategies.contexts_with_rational_vertices, strategies.indices)
def test_rotations(context_with_vertices: Tuple[Context, Sequence[Point]],
                   offset: int) -> None:
    context, vertices = context_with_vertices

    result = context.contour_edges(vertices)

    assert (rotate_sequence(result, offset)
            == context.contour_edges(rotate_sequence(vertices, offset)))
