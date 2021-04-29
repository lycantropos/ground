from typing import Tuple

from hypothesis import given

from ground.base import Context
from ground.hints import Contour
from tests.utils import (reverse_contour_coordinates,
                         reverse_contour_vertices,
                         rotate_contour)
from . import strategies


@given(strategies.contexts_with_contours)
def test_basic(context_with_contour: Tuple[Context, Contour]) -> None:
    context, contour = context_with_contour

    result = context.is_region_convex(contour)

    assert isinstance(result, bool)


@given(strategies.contexts_with_rational_contours)
def test_reversals(context_with_contour: Tuple[Context, Contour]) -> None:
    context, contour = context_with_contour

    result = context.is_region_convex(contour)

    assert result is context.is_region_convex(
            reverse_contour_vertices(contour))
    assert result is context.is_region_convex(
            reverse_contour_coordinates(contour))


@given(strategies.contexts_with_rational_contours, strategies.indices)
def test_rotations(context_with_contour: Tuple[Context, Contour],
                   offset: int) -> None:
    context, contour = context_with_contour

    result = context.is_region_convex(contour)

    assert result is context.is_region_convex(rotate_contour(contour,
                                                             offset))
