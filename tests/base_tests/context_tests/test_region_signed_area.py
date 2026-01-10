from hypothesis import given

from ground.base import Context
from ground.hints import Contour
from tests.hints import ScalarT
from tests.utils import (
    reverse_contour,
    reverse_contour_coordinates,
    rotate_contour,
    to_coordinate_checker,
)

from . import strategies


@given(strategies.contexts_with_contours)
def test_basic(
    context_with_contours: tuple[Context[ScalarT], Contour[ScalarT]],
) -> None:
    context, contour = context_with_contours

    result = context.region_signed_area(contour)

    assert to_coordinate_checker(context)(result)


@given(strategies.contexts_with_rational_contours)
def test_reversals(
    context_with_contours: tuple[Context[ScalarT], Contour[ScalarT]],
) -> None:
    context, contour = context_with_contours

    result = context.region_signed_area(contour)

    assert result == -context.region_signed_area(reverse_contour(contour))
    assert result == -context.region_signed_area(
        reverse_contour_coordinates(contour)
    )


@given(strategies.contexts_with_rational_contours, strategies.indices)
def test_rotations(
    context_with_contours: tuple[Context[ScalarT], Contour[ScalarT]],
    offset: int,
) -> None:
    context, contour = context_with_contours

    result = context.region_signed_area(contour)

    assert result == context.region_signed_area(
        rotate_contour(contour, offset)
    )
