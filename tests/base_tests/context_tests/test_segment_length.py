from hypothesis import given
from symba.base import Expression

from ground.context import Context
from ground.hints import Segment
from tests.hints import ScalarT
from tests.utils import reverse_segment, reverse_segment_coordinates

from . import strategies


@given(strategies.contexts_with_segments)
def test_basic(
    context_with_segment: tuple[Context[ScalarT], Segment[ScalarT]],
) -> None:
    context, segment = context_with_segment

    result = context.segment_length(segment)

    assert isinstance(result, Expression)


@given(strategies.contexts_with_segments)
def test_value(
    context_with_segment: tuple[Context[ScalarT], Segment[ScalarT]],
) -> None:
    context, segment = context_with_segment

    result = context.segment_length(segment)

    assert result > context.zero


@given(strategies.contexts_with_rational_segments)
def test_reversals(
    context_with_segment: tuple[Context[ScalarT], Segment[ScalarT]],
) -> None:
    context, segment = context_with_segment

    result = context.segment_length(segment)

    assert result == context.segment_length(reverse_segment(segment))
    assert result == context.segment_length(
        reverse_segment_coordinates(segment)
    )
