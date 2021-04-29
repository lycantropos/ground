from typing import Tuple

from hypothesis import given

from ground.base import Context
from ground.hints import Segment
from tests.utils import (is_coordinate,
                         reverse_segment,
                         reverse_segment_coordinates)
from . import strategies


@given(strategies.contexts_with_segments_pairs)
def test_basic(context_with_segments_pair
               : Tuple[Context, Tuple[Segment, Segment]]) -> None:
    context, (first, second) = context_with_segments_pair

    result = context.segments_squared_distance(first, second)

    assert is_coordinate(result)


@given(strategies.contexts_with_segments_pairs)
def test_reversals(context_with_segments_pair
                   : Tuple[Context, Tuple[Segment, Segment]]) -> None:
    context, (first, second) = context_with_segments_pair

    result = context.segments_squared_distance(first, second)

    assert (result
            == context.segments_squared_distance(reverse_segment(first),
                                                 second)
            == context.segments_squared_distance(first,
                                                 reverse_segment(second)))
    assert result == context.segments_squared_distance(
            reverse_segment_coordinates(first),
            reverse_segment_coordinates(second))


@given(strategies.contexts_with_segments_pairs)
def test_commutativity(context_with_segments_pair
                       : Tuple[Context, Tuple[Segment, Segment]]) -> None:
    context, (first, second) = context_with_segments_pair

    result = context.segments_squared_distance(first, second)

    assert result == context.segments_squared_distance(second, first)


@given(strategies.contexts_with_segments)
def test_self(context_with_segment: Tuple[Context, Segment]
              ) -> None:
    context, segment = context_with_segment

    assert context.segments_squared_distance(segment, segment) == 0
