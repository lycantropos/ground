from hypothesis import given

from ground.base import (Context,
                         Kind)
from tests.hints import (PointsPair,
                         PointsTriplet)
from . import strategies


@given(strategies.contexts, strategies.points_triplets)
def test_basic(context: Context, points_triplet: PointsTriplet) -> None:
    vertex, first_ray_point, second_ray_point = points_triplet

    result = context.kind(vertex, first_ray_point, second_ray_point)

    assert isinstance(result, Kind)


@given(strategies.contexts, strategies.points_pairs)
def test_same_endpoints(context: Context, points_pair: PointsPair) -> None:
    start, end = points_pair

    assert context.kind(end, start, start) is (Kind.RIGHT
                                               if start == end
                                               else Kind.ACUTE)


@given(strategies.contexts, strategies.points_triplets)
def test_endpoints_permutations(context: Context,
                                points_triplet: PointsTriplet) -> None:
    vertex, first_ray_point, second_ray_point = points_triplet

    result = context.kind(vertex, first_ray_point, second_ray_point)

    assert result is context.kind(vertex, second_ray_point, first_ray_point)
