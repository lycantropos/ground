from hypothesis import given

from ground.context import Context
from ground.hints import Segment
from tests.hints import ScalarT
from tests.utils import (
    reverse_point_coordinates,
    reverse_segment,
    reverse_segment_coordinates,
)

from . import strategies


@given(strategies.contexts_with_crossing_or_touching_segments_pairs)
def test_basic(
    context_with_segments_pair: tuple[
        Context[ScalarT], tuple[Segment[ScalarT], Segment[ScalarT]]
    ],
) -> None:
    context, (first, second) = context_with_segments_pair

    result = context.segments_intersection(first, second)

    assert isinstance(result, context.point_cls)


@given(strategies.contexts_with_rational_crossing_or_touching_segments_pairs)
def test_reversals(
    context_with_segments_pair: tuple[
        Context[ScalarT], tuple[Segment[ScalarT], Segment[ScalarT]]
    ],
) -> None:
    context, (first, second) = context_with_segments_pair

    result = context.segments_intersection(first, second)

    assert (
        result
        == context.segments_intersection(reverse_segment(first), second)
        == context.segments_intersection(first, reverse_segment(second))
        == context.segments_intersection(
            reverse_segment(first), reverse_segment(second)
        )
    )
    assert reverse_point_coordinates(result) == context.segments_intersection(
        reverse_segment_coordinates(first), reverse_segment_coordinates(second)
    )


@given(strategies.contexts_with_rational_crossing_or_touching_segments_pairs)
def test_commutativity(
    context_with_segments_pair_endpoints: tuple[
        Context[ScalarT], tuple[Segment[ScalarT], Segment[ScalarT]]
    ],
) -> None:
    context, (first, second) = context_with_segments_pair_endpoints

    result = context.segments_intersection(first, second)

    assert result == context.segments_intersection(second, first)
