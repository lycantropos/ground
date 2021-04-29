from typing import Tuple

from hypothesis import given

from ground.base import Context
from ground.hints import Contour
from tests.utils import (is_point,
                         reverse_contour_coordinates, reverse_contour_vertices,
                         reverse_point_coordinates, rotate_contour)
from . import strategies


@given(strategies.contexts_with_contours)
def test_basic(context_with_contour: Tuple[Context, Contour]) -> None:
    context, contour = context_with_contour

    result = context.contour_centroid(contour)

    assert is_point(result)


@given(strategies.contexts_with_rational_contours)
def test_reversals(context_with_contour: Tuple[Context, Contour]
                   ) -> None:
    context, contour = context_with_contour

    result = context.contour_centroid(contour)

    assert result == context.contour_centroid(reverse_contour_vertices(
            contour))
    assert reverse_point_coordinates(result) == context.contour_centroid(
            reverse_contour_coordinates(contour))


@given(strategies.contexts_with_rational_contours, strategies.indices)
def test_rotations(context_with_contour: Tuple[Context, Contour],
                   offset: int) -> None:
    context, contour = context_with_contour

    result = context.contour_centroid(contour)

    assert result == context.contour_centroid(rotate_contour(contour, offset))
