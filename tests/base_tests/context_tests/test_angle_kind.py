from typing import Tuple

from hypothesis import given

from ground.base import (Context,
                         Kind)
from tests.hints import (PointsPair,
                         PointsTriplet)
from . import strategies


@given(strategies.contexts_with_points_triplets)
def test_basic(context_with_points_triplet: Tuple[Context, PointsTriplet]
               ) -> None:
    context, points_triplet = context_with_points_triplet
    vertex, first_ray_point, second_ray_point = points_triplet

    result = context.angle_kind(vertex, first_ray_point, second_ray_point)

    assert isinstance(result, Kind)


@given(strategies.contexts_with_points_pairs)
def test_same_endpoints(context_with_points_pair: Tuple[Context, PointsPair]
                        ) -> None:
    context, points_pair = context_with_points_pair
    start, end = points_pair

    assert context.angle_kind(end, start, start) is (Kind.RIGHT
                                                     if start == end
                                                     else Kind.ACUTE)
    assert context.angle_kind(start, end, start) is Kind.RIGHT


@given(strategies.contexts_with_points_triplets)
def test_endpoints_permutations(context_with_points_triplet
                                : Tuple[Context, PointsTriplet]) -> None:
    context, points_triplet = context_with_points_triplet
    vertex, first_ray_point, second_ray_point = points_triplet

    result = context.angle_kind(vertex, first_ray_point, second_ray_point)

    assert result is context.angle_kind(vertex, second_ray_point,
                                        first_ray_point)
