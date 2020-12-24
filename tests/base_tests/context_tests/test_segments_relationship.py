from hypothesis import given

from ground.base import (Context,
                         SegmentsRelationship)
from tests.hints import (PointsPair,
                         PointsQuadruplet)
from . import strategies


@given(strategies.contexts, strategies.segments_pairs_endpoints)
def test_basic(context: Context, 
               segments_pair_endpoints: PointsQuadruplet) -> None:
    first_start, first_end, second_start, second_end = segments_pair_endpoints

    result = context.segments_relationship(first_start, first_end,
                                           second_start, second_end)

    assert isinstance(result, SegmentsRelationship)


@given(strategies.contexts, strategies.segments_pairs_endpoints)
def test_permutations(context: Context,
                      segments_pair_endpoints: PointsQuadruplet) -> None:
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


@given(strategies.contexts, strategies.segments_endpoints)
def test_self(context: Context, segment_endpoints: PointsPair) -> None:
    start, end = segment_endpoints

    result = context.segments_relationship(start, end, start, end)

    assert result is SegmentsRelationship.OVERLAP
