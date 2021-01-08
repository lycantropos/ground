from typing import Tuple

from hypothesis import given

from ground.base import Context
from tests.hints import PointsQuadruplet
from tests.utils import is_point
from . import strategies


@given(strategies.contexts_with_crossing_or_touching_segments_pairs_endpoints)
def test_basic(context_with_segments_pair_endpoints
               : Tuple[Context, PointsQuadruplet]) -> None:
    context, segments_pair_endpoints = context_with_segments_pair_endpoints
    first_start, first_end, second_start, second_end = segments_pair_endpoints

    result = context.segments_intersection(first_start, first_end,
                                           second_start, second_end)

    assert is_point(result)


@given(strategies.contexts_with_crossing_or_touching_segments_pairs_endpoints)
def test_endpoints_permutation(context_with_segments_pair_endpoints
                               : Tuple[Context, PointsQuadruplet]) -> None:
    context, segments_pair_endpoints = context_with_segments_pair_endpoints
    first_start, first_end, second_start, second_end = segments_pair_endpoints

    result = context.segments_intersection(first_start, first_end,
                                           second_start, second_end)

    assert (result == context.segments_intersection(first_end, first_start,
                                                    second_start, second_end)
            == context.segments_intersection(first_end, first_start,
                                             second_end, second_start)
            == context.segments_intersection(first_start, first_end,
                                             second_end, second_start))


@given(strategies.contexts_with_crossing_or_touching_segments_pairs_endpoints)
def test_segments_permutation(context_with_segments_pair_endpoints
                              : Tuple[Context, PointsQuadruplet]) -> None:
    context, segments_pair_endpoints = context_with_segments_pair_endpoints
    first_start, first_end, second_start, second_end = segments_pair_endpoints

    result = context.segments_intersection(first_start, first_end,
                                           second_start, second_end)

    assert result == context.segments_intersection(second_start, second_end,
                                                   first_start, first_end)
