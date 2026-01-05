from hypothesis import given
from symba.base import Expression

from ground.base import Context
from ground.hints import Contour
from tests.hints import ScalarT
from tests.utils import reverse_contour, reverse_contour_coordinates

from . import strategies


@given(strategies.contexts_with_contours)
def test_basic(
    context_with_contour: tuple[Context[ScalarT], Contour[ScalarT]],
) -> None:
    context, contour = context_with_contour

    result = context.contour_length(contour)

    assert isinstance(result, Expression)


@given(strategies.contexts_with_contours)
def test_value(
    context_with_contour: tuple[Context[ScalarT], Contour[ScalarT]],
) -> None:
    context, contour = context_with_contour

    result = context.contour_length(contour)

    assert result > context.zero


@given(strategies.contexts_with_rational_contours)
def test_reversals(
    context_with_contour: tuple[Context[ScalarT], Contour[ScalarT]],
) -> None:
    context, contour = context_with_contour

    result = context.contour_length(contour)

    assert result == context.contour_length(reverse_contour(contour))
    assert result == context.contour_length(
        reverse_contour_coordinates(contour)
    )
