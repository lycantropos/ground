from hypothesis import given

from ground.context import Context
from ground.hints import Contour
from tests.hints import ScalarT
from tests.utils import (
    reverse_contour,
    reverse_contour_coordinates,
    reverse_geometry_coordinates,
)

from . import strategies


@given(strategies.contexts_with_contours_and_scalars_pairs)
def test_basic(
    context_with_contour_and_factors: tuple[
        Context[ScalarT], Contour[ScalarT], ScalarT, ScalarT
    ],
) -> None:
    context, contour, factor_x, factor_y = context_with_contour_and_factors

    result = context.scale_contour(contour, factor_x, factor_y)

    assert isinstance(
        result,
        (context.contour_cls, context.multipoint_cls, context.segment_cls),
    )


@given(strategies.contexts_with_contours_and_scalars_pairs)
def test_reversals(
    context_with_contour_and_factors: tuple[
        Context[ScalarT], Contour[ScalarT], ScalarT, ScalarT
    ],
) -> None:
    context, contour, factor_x, factor_y = context_with_contour_and_factors

    result = context.scale_contour(contour, factor_x, factor_y)

    assert not isinstance(result, context.contour_cls) or reverse_contour(
        result
    ) == context.scale_contour(reverse_contour(contour), factor_x, factor_y)
    assert reverse_geometry_coordinates(result) == context.scale_contour(
        reverse_contour_coordinates(contour), factor_y, factor_x
    )
