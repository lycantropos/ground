from typing import Tuple

from hypothesis import given

from ground.base import Context
from tests.hints import (PointsPair,
                         PointsQuadruplet)
from tests.utils import is_coordinate
from . import strategies


@given(strategies.contexts_with_segments_pairs_endpoints)
def test_basic(context_with_segments_pair_endpoints
               : Tuple[Context, PointsQuadruplet]) -> None:
    context, segments_pair_endpoints = context_with_segments_pair_endpoints
    first_start, first_end, second_start, second_end = segments_pair_endpoints

    result = context.segments_squared_distance(first_start, first_end,
                                               second_start, second_end)

    assert is_coordinate(result)


@given(strategies.contexts_with_rational_segments_pairs_endpoints)
def test_endpoints_symmetry(context_with_segments_pair_endpoints
                            : Tuple[Context, PointsQuadruplet]) -> None:
    context, segments_pair_endpoints = context_with_segments_pair_endpoints
    first_start, first_end, second_start, second_end = segments_pair_endpoints

    result = context.segments_squared_distance(first_start, first_end,
                                               second_start, second_end)

    assert (result
            == context.segments_squared_distance(first_end, first_start,
                                                 second_start, second_end)
            == context.segments_squared_distance(first_end, first_start,
                                                 second_end, second_start)
            == context.segments_squared_distance(first_start, first_end,
                                                 second_end, second_start))


@given(strategies.contexts_with_segments_pairs_endpoints)
def test_segments_symmetry(context_with_segments_pair_endpoints
                           : Tuple[Context, PointsQuadruplet]) -> None:
    context, segments_pair_endpoints = context_with_segments_pair_endpoints
    first_start, first_end, second_start, second_end = segments_pair_endpoints

    result = context.segments_squared_distance(first_start, first_end,
                                               second_start, second_end)

    assert result == context.segments_squared_distance(
            second_start, second_end, first_start, first_end)


@given(strategies.contexts_with_segments_endpoints)
def test_self(context_with_segment_endpoints: Tuple[Context, PointsPair]
              ) -> None:
    context, segment_endpoints = context_with_segment_endpoints
    start, end = segment_endpoints

    assert context.segments_squared_distance(start, end, start, end) == 0