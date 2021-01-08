from typing import Tuple

from hypothesis import given

from ground.base import (Context,
                         Relation)
from tests.hints import (PointsPair,
                         PointsQuadruplet)
from tests.utils import (ASYMMETRIC_LINEAR_RELATIONS,
                         LINEAR_RELATIONS,
                         SYMMETRIC_LINEAR_RELATIONS,
                         equivalence)
from . import strategies


@given(strategies.contexts_with_segments_pairs_endpoints)
def test_basic(context_with_segments_pair_endpoints
               : Tuple[Context, PointsQuadruplet]) -> None:
    context, segments_pair_endpoints = context_with_segments_pair_endpoints
    first_start, first_end, second_start, second_end = segments_pair_endpoints

    result = context.segments_relation(first_start, first_end, second_start,
                                       second_end)

    assert isinstance(result, Relation)
    assert result in LINEAR_RELATIONS


@given(strategies.contexts_with_segments_pairs_endpoints)
def test_endpoints_permutation(context_with_segments_pair_endpoints
                               : Tuple[Context, PointsQuadruplet]) -> None:
    context, segments_pair_endpoints = context_with_segments_pair_endpoints
    first_start, first_end, second_start, second_end = segments_pair_endpoints

    result = context.segments_relation(first_start, first_end, second_start,
                                       second_end)

    assert (result is context.segments_relation(first_end, first_start,
                                                second_start, second_end)
            is context.segments_relation(first_end, first_start, second_end,
                                         second_start)
            is context.segments_relation(first_start, first_end, second_end,
                                         second_start))


@given(strategies.contexts_with_segments_pairs_endpoints)
def test_segments_permutation(context_with_segments_pair_endpoints
                              : Tuple[Context, PointsQuadruplet]) -> None:
    context, segments_pair_endpoints = context_with_segments_pair_endpoints
    first_start, first_end, second_start, second_end = segments_pair_endpoints

    result = context.segments_relation(first_start, first_end, second_start,
                                       second_end)

    complement = context.segments_relation(second_start, second_end,
                                           first_start, first_end)
    assert equivalence(result is complement,
                       result in SYMMETRIC_LINEAR_RELATIONS)
    assert equivalence(result is not complement,
                       result.complement is complement
                       and result in ASYMMETRIC_LINEAR_RELATIONS
                       and complement in ASYMMETRIC_LINEAR_RELATIONS)


@given(strategies.contexts_with_segments_endpoints)
def test_self(context_with_segment_endpoints: Tuple[Context, PointsPair]
              ) -> None:
    context, segment_endpoints = context_with_segment_endpoints
    start, end = segment_endpoints

    result = context.segments_relation(start, end, start, end)

    assert result is Relation.EQUAL
