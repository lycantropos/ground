from typing import (Sequence,
                    Tuple)

from hypothesis import given

from ground.base import Context
from ground.hints import Contour
from tests.utils import (is_point,
                         rotate_sequence)
from . import strategies


@given(strategies.contexts_with_borders_and_holes_sequences)
def test_basic(context_with_border_and_holes
               : Tuple[Context, Contour, Sequence[Contour]]) -> None:
    context, border, holes = context_with_border_and_holes

    result = context.polygon_centroid(border, holes)

    assert is_point(result)


@given(strategies.contexts_with_rational_borders_and_holes_sequences)
def test_holes_rotations(context_with_border_and_holes
                         : Tuple[Context, Contour, Sequence[Contour]]
                         ) -> None:
    context, border, holes = context_with_border_and_holes

    result = context.polygon_centroid(border, holes)

    assert all(context.polygon_centroid(border, rotate_sequence(holes, offset))
               == result
               for offset in range(len(holes)))
