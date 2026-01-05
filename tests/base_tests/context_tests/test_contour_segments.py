from collections import abc

from hypothesis import given

from ground.base import Context
from ground.hints import Contour
from tests.hints import ScalarT
from tests.utils import is_segment, rotate_contour, rotate_sequence

from . import strategies


@given(strategies.contexts_with_contours)
def test_basic(
    context_with_contour: tuple[Context[ScalarT], Contour[ScalarT]],
) -> None:
    context, contour = context_with_contour

    result = context.contour_segments(contour)

    assert isinstance(result, abc.Sequence)
    assert len(result) == len(contour.vertices)
    assert all(is_segment(element) for element in result)


@given(strategies.contexts_with_rational_contours, strategies.indices)
def test_rotations(
    context_with_contour: tuple[Context[ScalarT], Contour[ScalarT]],
    offset: int,
) -> None:
    context, contour = context_with_contour

    result = context.contour_segments(contour)

    assert rotate_sequence(result, offset) == context.contour_segments(
        rotate_contour(contour, offset)
    )
