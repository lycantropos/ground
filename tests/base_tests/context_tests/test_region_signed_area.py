from typing import Tuple

from hypothesis import given

from ground.base import Context
from ground.hints import Contour
from tests.utils import (context_to_output_coordinate_cls,
                         reverse_contour_coordinates,
                         reverse_contour,
                         rotate_contour)
from . import strategies


@given(strategies.contexts_with_contours)
def test_basic(context_with_contours: Tuple[Context, Contour]) -> None:
    context, contour = context_with_contours

    result = context.region_signed_area(contour)

    assert isinstance(result, context_to_output_coordinate_cls(context))


@given(strategies.contexts_with_rational_contours)
def test_reversals(context_with_contours: Tuple[Context, Contour]
                   ) -> None:
    context, contour = context_with_contours

    result = context.region_signed_area(contour)

    assert result == -context.region_signed_area(reverse_contour(
            contour))
    assert result == -context.region_signed_area(reverse_contour_coordinates(
            contour))


@given(strategies.contexts_with_rational_contours, strategies.indices)
def test_rotations(context_with_contours: Tuple[Context, Contour],
                   offset: int) -> None:
    context, contour = context_with_contours

    result = context.region_signed_area(contour)

    assert (result
            == context.region_signed_area(rotate_contour(contour, offset)))
