from collections import abc
from typing import Tuple

from hypothesis import given

from ground.base import Context
from ground.hints import Contour
from tests.utils import (is_segment,
                         rotate_contour,
                         rotate_sequence)
from . import strategies


@given(strategies.contexts_with_contours)
def test_basic(context_with_contour: Tuple[Context, Contour]) -> None:
    context, contour = context_with_contour

    result = context.contour_edges(contour)

    assert isinstance(result, abc.Sequence)
    assert len(result) == len(contour.vertices)
    assert all(is_segment(element) for element in result)


@given(strategies.contexts_with_rational_contours, strategies.indices)
def test_rotations(context_with_contour: Tuple[Context, Contour],
                   offset: int) -> None:
    context, contour = context_with_contour

    result = context.contour_edges(contour)

    assert (rotate_sequence(result, offset)
            == context.contour_edges(rotate_contour(contour, offset)))
