from hypothesis import given

from ground.context import Context
from ground.hints import Contour
from tests.hints import ScalarT
from tests.utils import (
    is_point,
    reverse_contour,
    reverse_contour_coordinates,
    reverse_point_coordinates,
    rotate_contour,
)

from . import strategies


@given(strategies.contexts_with_contours)
def test_basic(
    context_with_contour: tuple[Context[ScalarT], Contour[ScalarT]],
) -> None:
    context, contour = context_with_contour

    result = context.region_centroid(contour)

    assert is_point(result)


@given(strategies.contexts_with_rational_contours)
def test_reversals(
    context_with_contour: tuple[Context[ScalarT], Contour[ScalarT]],
) -> None:
    context, contour = context_with_contour

    result = context.region_centroid(contour)

    assert result == context.region_centroid(reverse_contour(contour))
    assert reverse_point_coordinates(result) == context.region_centroid(
        reverse_contour_coordinates(contour)
    )


@given(strategies.contexts_with_rational_contours, strategies.indices)
def test_rotations(
    context_with_contour: tuple[Context[ScalarT], Contour[ScalarT]],
    offset: int,
) -> None:
    context, contour = context_with_contour

    result = context.region_centroid(contour)

    assert result == context.region_centroid(rotate_contour(contour, offset))
