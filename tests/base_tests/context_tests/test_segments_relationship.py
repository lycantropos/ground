from typing import Tuple

from hypothesis import given

from ground.base import (Context,
                         SegmentsRelationship)
from tests.hints import (PointsPair,
                         PointsQuadruplet)
from . import strategies


@given(strategies.contexts_with_segments_pairs_endpoints)
def test_basic(context_with_segments_pair_endpoints
               : Tuple[Context, PointsQuadruplet]) -> None:
    context, segments_pair_endpoints = context_with_segments_pair_endpoints

    first_start, first_end, second_start, second_end = segments_pair_endpoints

    result = context.segments_relationship(first_start, first_end,
                                           second_start, second_end)

    assert isinstance(result, SegmentsRelationship)


@given(strategies.contexts_with_segments_pairs_endpoints)
def test_permutations(context_with_segments_pair_endpoints
                      : Tuple[Context, PointsQuadruplet]) -> None:
    context, segments_pair_endpoints = context_with_segments_pair_endpoints
    first_start, first_end, second_start, second_end = segments_pair_endpoints

    result = context.segments_relationship(first_start, first_end,
                                           second_start, second_end)

    assert result is context.segments_relationship(second_start, second_end,
                                                   first_start, first_end)
    assert (result is context.segments_relationship(first_end, first_start,
                                                    second_start, second_end)
            is context.segments_relationship(first_end, first_start,
                                             second_end, second_start)
            is context.segments_relationship(first_start, first_end,
                                             second_end, second_start))


@given(strategies.contexts_with_segments_endpoints)
def test_self(context_with_segment_endpoints: Tuple[Context, PointsPair]
              ) -> None:
    context, segment_endpoints = context_with_segment_endpoints
    start, end = segment_endpoints

    result = context.segments_relationship(start, end, start, end)

    assert result is SegmentsRelationship.OVERLAP
