from typing import Tuple

from hypothesis import given

from ground.base import Context
from ground.hints import Point
from tests.hints import PointsPair
from tests.utils import is_coordinate
from . import strategies


@given(strategies.contexts_with_points_pairs)
def test_basic(context_with_points_pair: Tuple[Context, PointsPair]) -> None:
    context, points_pair = context_with_points_pair
    first_point, second_point = points_pair

    result = context.points_squared_distance(first_point, second_point)

    assert is_coordinate(result)


@given(strategies.contexts_with_rational_points_pairs)
def test_symmetry(context_with_points_pair: Tuple[Context, PointsPair]
                  ) -> None:
    context, points_pair = context_with_points_pair
    first_point, second_point = points_pair

    result = context.points_squared_distance(first_point, second_point)

    assert result == context.points_squared_distance(second_point, first_point)


@given(strategies.contexts_with_points)
def test_self(context_with_point: Tuple[Context, Point]) -> None:
    context, point = context_with_point

    assert context.points_squared_distance(point, point) == 0
