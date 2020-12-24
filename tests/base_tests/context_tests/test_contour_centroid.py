from typing import Tuple

from hypothesis import given

from ground.base import Context
from ground.hints import Contour
from tests.utils import (is_point,
                         rotate_contour)
from . import strategies


@given(strategies.contexts_with_contours)
def test_basic(context_with_contour: Tuple[Context, Contour]) -> None:
    context, contour = context_with_contour

    result = context.contour_centroid(contour)

    assert is_point(result)


@given(strategies.contexts_with_rational_contours)
def test_rotations(context_with_contour: Tuple[Context, Contour]) -> None:
    context, contour = context_with_contour

    result = context.contour_centroid(contour)

    assert all(context.contour_centroid(rotate_contour(contour, offset))
               == result
               for offset in range(len(contour.vertices)))
