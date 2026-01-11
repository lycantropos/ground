from hypothesis import given

from ground.context import Context
from ground.hints import Point, Segment
from tests.hints import ScalarT
from tests.utils import (
    reverse_point_coordinates,
    reverse_segment,
    reverse_segment_coordinates,
    to_coordinate_checker,
)

from . import strategies


@given(strategies.contexts_with_segments_and_points)
def test_basic(
    context_with_segment_and_point: tuple[
        Context[ScalarT], Segment[ScalarT], Point[ScalarT]
    ],
) -> None:
    context, segment, point = context_with_segment_and_point

    result = context.segment_point_squared_distance(segment, point)

    assert to_coordinate_checker(context)(result)


@given(strategies.contexts_with_rational_segments_and_points)
def test_reversals(
    context_with_segment_and_point: tuple[
        Context[ScalarT], Segment[ScalarT], Point[ScalarT]
    ],
) -> None:
    context, segment, point = context_with_segment_and_point

    result = context.segment_point_squared_distance(segment, point)

    assert result == context.segment_point_squared_distance(
        reverse_segment(segment), point
    )
    assert result == context.segment_point_squared_distance(
        reverse_segment_coordinates(segment), reverse_point_coordinates(point)
    )


@given(strategies.contexts_with_rational_segments)
def test_self(
    context_with_segment: tuple[Context[ScalarT], Segment[ScalarT]],
) -> None:
    context, segment = context_with_segment

    assert (
        context.segment_point_squared_distance(segment, segment.start)
        == context.segment_point_squared_distance(segment, segment.end)
        == context.zero
    )
