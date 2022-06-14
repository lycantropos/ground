from typing import Tuple

from hypothesis import given

from ground.base import (Context,
                         Relation)
from ground.hints import Segment
from tests.utils import (ASYMMETRIC_LINEAR_RELATIONS,
                         LINEAR_RELATIONS,
                         SYMMETRIC_LINEAR_RELATIONS,
                         equivalence,
                         reverse_segment,
                         reverse_segment_coordinates)
from . import strategies


@given(strategies.contexts_with_segments_pairs)
def test_basic(context_with_segments_pair
               : Tuple[Context, Tuple[Segment, Segment]]) -> None:
    context, (first, second) = context_with_segments_pair

    result = context.segments_relation(first, second)

    assert isinstance(result, Relation)
    assert result in LINEAR_RELATIONS


@given(strategies.contexts_with_rational_segments_pairs)
def test_reversals(context_with_segments_pair
                   : Tuple[Context, Tuple[Segment, Segment]]) -> None:
    context, (first, second) = context_with_segments_pair

    result = context.segments_relation(first, second)

    assert (result is context.segments_relation(reverse_segment(first), second)
            is context.segments_relation(first, reverse_segment(second)))
    assert result is context.segments_relation(
            reverse_segment_coordinates(first),
            reverse_segment_coordinates(second))


@given(strategies.contexts_with_rational_segments_pairs)
def test_commutativity(context_with_segments_pair
                       : Tuple[Context, Tuple[Segment, Segment]]) -> None:
    context, (first, second) = context_with_segments_pair

    result = context.segments_relation(first, second)

    complement = context.segments_relation(second, first)
    assert equivalence(result is complement,
                       result in SYMMETRIC_LINEAR_RELATIONS)
    assert equivalence(result is not complement,
                       result.complement is complement
                       and result in ASYMMETRIC_LINEAR_RELATIONS
                       and complement in ASYMMETRIC_LINEAR_RELATIONS)


@given(strategies.contexts_with_segments)
def test_self(context_with_segment: Tuple[Context, Segment]
              ) -> None:
    context, segment = context_with_segment

    result = context.segments_relation(segment, segment)

    assert result is Relation.EQUAL
