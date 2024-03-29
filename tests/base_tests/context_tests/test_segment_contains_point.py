from typing import Tuple

from hypothesis import given

from ground.base import Context
from ground.hints import (Point,
                          Segment)
from tests.utils import (reverse_point_coordinates,
                         reverse_segment,
                         reverse_segment_coordinates)
from . import strategies


@given(strategies.contexts_with_segments_and_points)
def test_basic(context_with_segment_and_point: Tuple[Context, Segment, Point]
               ) -> None:
    context, segment, point = context_with_segment_and_point

    result = context.segment_contains_point(segment, point)

    assert isinstance(result, bool)


@given(strategies.contexts_with_rational_segments_and_points)
def test_reversals(context_with_segment_and_point
                   : Tuple[Context, Segment, Point]) -> None:
    context, segment, point = context_with_segment_and_point

    result = context.segment_contains_point(segment, point)

    assert result is context.segment_contains_point(
            reverse_segment(segment), point)
    assert result is context.segment_contains_point(
            reverse_segment_coordinates(segment),
            reverse_point_coordinates(point))


@given(strategies.contexts_with_rational_segments)
def test_self(context_with_segment: Tuple[Context, Segment]
              ) -> None:
    context, segment = context_with_segment

    assert (context.segment_contains_point(segment, segment.start)
            and context.segment_contains_point(segment, segment.end))
