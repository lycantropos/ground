from hypothesis import given
from symba.base import Expression

from ground.base import Context
from ground.hints import Multisegment
from tests.hints import ScalarT
from tests.utils import reverse_multisegment, reverse_multisegment_coordinates

from . import strategies


@given(strategies.contexts_with_multisegments)
def test_basic(
    context_with_multisegment: tuple[Context[ScalarT], Multisegment[ScalarT]],
) -> None:
    context, multisegment = context_with_multisegment

    result = context.multisegment_length(multisegment)

    assert isinstance(result, Expression)


@given(strategies.contexts_with_multisegments)
def test_value(
    context_with_multisegment: tuple[Context[ScalarT], Multisegment[ScalarT]],
) -> None:
    context, multisegment = context_with_multisegment

    result = context.multisegment_length(multisegment)

    assert all(
        result > context.segment_length(segment)
        for segment in multisegment.segments
    )


@given(strategies.contexts_with_rational_multisegments)
def test_reversals(
    context_with_multisegment: tuple[Context[ScalarT], Multisegment[ScalarT]],
) -> None:
    context, multisegment = context_with_multisegment

    result = context.multisegment_length(multisegment)

    assert result == context.multisegment_length(
        reverse_multisegment(multisegment)
    )
    assert result == context.multisegment_length(
        reverse_multisegment_coordinates(multisegment)
    )
