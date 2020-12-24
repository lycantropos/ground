from typing import Tuple

from hypothesis import given

from ground.base import (Context,
                         SegmentsRelationship)
from tests.hints import (PointsPair,
                         PointsQuadruplet)
from tests.utils import (is_point,
                         reverse_point_coordinates)
from . import strategies


@given(strategies.contexts_with_segments_pairs_endpoints)
def test_basic(context_with_segments_pair_endpoints
               : Tuple[Context, PointsQuadruplet]) -> None:
    context, segments_pair_endpoints = context_with_segments_pair_endpoints
    first_start, first_end, second_start, second_end = segments_pair_endpoints

    result = context.segments_intersections(first_start, first_end,
                                            second_start, second_end)

    assert isinstance(result, tuple)
    assert all(is_point(element) for element in result)
    assert len(result) <= 2


@given(strategies.contexts_with_segments_pairs_endpoints)
def test_commutativity(context_with_segments_pair_endpoints
                       : Tuple[Context, PointsQuadruplet]) -> None:
    context, segments_pair_endpoints = context_with_segments_pair_endpoints
    first_start, first_end, second_start, second_end = segments_pair_endpoints

    result = context.segments_intersections(first_start, first_end,
                                            second_start, second_end)

    assert result == context.segments_intersections(second_start, second_end,
                                                    first_start, first_end)


@given(strategies.contexts_with_segments_endpoints)
def test_self(context_with_segment_endpoints: Tuple[Context, PointsPair]
              ) -> None:
    context, segment_endpoints = context_with_segment_endpoints
    start, end = segment_endpoints

    result = context.segments_intersections(start, end, start, end)

    assert (result == context.segments_intersections(start, end, end, start)
            == tuple(sorted(segment_endpoints)))


@given(strategies.contexts_with_segments_pairs_endpoints)
def test_connection_with_segments_relationship(
        context_with_segments_pair_endpoints: Tuple[Context, PointsQuadruplet]
) -> None:
    context, segments_pair_endpoints = context_with_segments_pair_endpoints
    first_start, first_end, second_start, second_end = segments_pair_endpoints

    result = context.segments_intersections(first_start, first_end,
                                            second_start, second_end)

    relationship = context.segments_relationship(first_start, first_end,
                                                 second_start, second_end)
    assert (len(result)
            == (0
                if relationship is SegmentsRelationship.NONE
                else (2
                      if relationship is SegmentsRelationship.OVERLAP
                      else 1)))


@given(strategies.contexts_with_segments_pairs_endpoints)
def test_reversed_coordinates(context_with_segments_pair_endpoints
                              : Tuple[Context, PointsQuadruplet]) -> None:
    context, segments_pair_endpoints = context_with_segments_pair_endpoints
    first_start, first_end, second_start, second_end = segments_pair_endpoints

    result = context.segments_intersections(first_start, first_end,
                                            second_start, second_end)

    assert (tuple(sorted(map(reverse_point_coordinates, result)))
            == context.segments_intersections(
                    reverse_point_coordinates(first_start),
                    reverse_point_coordinates(first_end),
                    reverse_point_coordinates(second_start),
                    reverse_point_coordinates(second_end)))
