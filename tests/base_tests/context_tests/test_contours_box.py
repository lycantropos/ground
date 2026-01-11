from collections.abc import Sequence

from hypothesis import given

from ground.context import Context
from ground.hints import Contour
from tests.hints import ScalarT
from tests.utils import (
    is_box,
    permute,
    reverse_box_coordinates,
    reverse_contours_coordinates,
    reverse_sequence,
)

from . import strategies


@given(strategies.contexts_with_contours_sequences)
def test_basic(
    context_with_contours: tuple[Context[ScalarT], Sequence[Contour[ScalarT]]],
) -> None:
    context, contours = context_with_contours

    result = context.contours_box(contours)

    assert is_box(result)


@given(strategies.contexts_with_contours_sequences)
def test_reversals(
    context_with_contours: tuple[Context[ScalarT], Sequence[Contour[ScalarT]]],
) -> None:
    context, contours = context_with_contours

    result = context.contours_box(contours)

    assert result == context.contours_box(reverse_sequence(contours))
    assert result == reverse_box_coordinates(
        context.contours_box(reverse_contours_coordinates(contours))
    )


@given(strategies.contexts_with_contours_sequences, strategies.indices)
def test_permutations(
    context_with_contours: tuple[Context[ScalarT], Sequence[Contour[ScalarT]]],
    index: int,
) -> None:
    context, contours = context_with_contours

    result = context.contours_box(contours)

    assert result == context.contours_box(permute(contours, index))
