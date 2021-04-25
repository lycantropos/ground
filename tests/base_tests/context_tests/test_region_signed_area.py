from typing import (Sequence,
                    Tuple)

from hypothesis import given

from ground.base import Context
from ground.hints import Point
from tests.utils import (context_to_output_coordinate_cls,
                         reverse_sequence,
                         rotate_sequence)
from . import strategies


@given(strategies.contexts_with_vertices)
def test_basic(context_with_vertices: Tuple[Context, Sequence[Point]]) -> None:
    context, vertices = context_with_vertices

    result = context.region_signed_area(vertices)

    assert isinstance(result, context_to_output_coordinate_cls(context))


@given(strategies.contexts_with_rational_vertices)
def test_reversals(context_with_vertices: Tuple[Context, Sequence[Point]]
                   ) -> None:
    context, vertices = context_with_vertices

    result = context.region_signed_area(vertices)

    assert result == -context.region_signed_area(reverse_sequence(vertices))


@given(strategies.contexts_with_rational_vertices, strategies.indices)
def test_rotations(context_with_vertices: Tuple[Context, Sequence[Point]],
                   offset: int) -> None:
    context, vertices = context_with_vertices

    result = context.region_signed_area(vertices)

    assert (result
            == context.region_signed_area(rotate_sequence(vertices, offset)))
