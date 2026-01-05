from hypothesis import given

from ground.base import Context
from ground.hints import Point
from tests.hints import PointsPair, ScalarT

from . import strategies


@given(strategies.contexts_with_points_pairs)
def test_basic(
    context_with_points_pair: tuple[Context[ScalarT], PointsPair[ScalarT]],
) -> None:
    context, points_pair = context_with_points_pair
    first_point, second_point = points_pair

    result = context.points_squared_distance(first_point, second_point)

    assert context.coordinate_checker(result)


@given(strategies.contexts_with_rational_points_pairs)
def test_symmetry(
    context_with_points_pair: tuple[Context[ScalarT], PointsPair[ScalarT]],
) -> None:
    context, points_pair = context_with_points_pair
    first_point, second_point = points_pair

    result = context.points_squared_distance(first_point, second_point)

    assert result == context.points_squared_distance(second_point, first_point)


@given(strategies.contexts_with_points)
def test_self(
    context_with_point: tuple[Context[ScalarT], Point[ScalarT]],
) -> None:
    context, point = context_with_point

    assert context.points_squared_distance(point, point) == context.zero
