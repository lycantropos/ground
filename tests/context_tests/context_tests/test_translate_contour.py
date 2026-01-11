from hypothesis import given

from ground.context import Context
from ground.hints import Contour
from tests.hints import ScalarT
from tests.utils import reverse_contour, reverse_contour_coordinates

from . import strategies


@given(strategies.contexts_with_contours_and_scalars_pairs)
def test_basic(
    context_with_contour_and_steps: tuple[
        Context[ScalarT], Contour[ScalarT], ScalarT, ScalarT
    ],
) -> None:
    context, contour, step_x, step_y = context_with_contour_and_steps

    result = context.translate_contour(contour, step_x, step_y)

    assert isinstance(result, context.contour_cls)


@given(strategies.contexts_with_rational_contours_and_scalars_pairs)
def test_round_trip(
    context_with_contour_and_steps: tuple[
        Context[ScalarT], Contour[ScalarT], ScalarT, ScalarT
    ],
) -> None:
    context, contour, step_x, step_y = context_with_contour_and_steps

    result = context.translate_contour(contour, step_x, step_y)

    assert context.translate_contour(
        result, -step_x, -step_y
    ) == context.translate_contour(contour, context.zero, context.zero)


@given(strategies.contexts_with_contours_and_scalars_pairs)
def test_reversals(
    context_with_contour_and_steps: tuple[
        Context[ScalarT], Contour[ScalarT], ScalarT, ScalarT
    ],
) -> None:
    context, contour, step_x, step_y = context_with_contour_and_steps

    result = context.translate_contour(contour, step_x, step_y)

    assert reverse_contour(result) == context.translate_contour(
        reverse_contour(contour), step_x, step_y
    )
    assert reverse_contour_coordinates(result) == context.translate_contour(
        reverse_contour_coordinates(contour), step_y, step_x
    )
