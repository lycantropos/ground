from typing import Tuple

from hypothesis import given

from ground.base import Context
from ground.hints import Point
from tests.hints import PointsPair
from tests.utils import is_coordinate
from . import strategies


@given(strategies.contexts_with_segments_endpoints_and_points)
def test_basic(context_with_segment_endpoints_and_point
               : Tuple[Context, PointsPair, Point]) -> None:
    (context, segment_endpoints,
     point) = context_with_segment_endpoints_and_point
    start, end = segment_endpoints

    result = context.segment_point_squared_distance(start, end, point)

    assert is_coordinate(result)


@given(strategies.contexts_with_rational_segments_endpoints_and_points)
def test_endpoints_symmetry(context_with_segment_endpoints_and_point
                            : Tuple[Context, PointsPair, Point]) -> None:
    (context, segment_endpoints,
     point) = context_with_segment_endpoints_and_point
    start, end = segment_endpoints

    result = context.segment_point_squared_distance(start, end, point)

    assert result == context.segment_point_squared_distance(end, start, point)


@given(strategies.contexts_with_rational_segments_endpoints)
def test_self(context_with_segment_endpoints: Tuple[Context, PointsPair]
              ) -> None:
    context, segment_endpoints = context_with_segment_endpoints
    start, end = segment_endpoints

    assert (context.segment_point_squared_distance(start, end, start)
            == context.segment_point_squared_distance(start, end, end)
            == 0)
