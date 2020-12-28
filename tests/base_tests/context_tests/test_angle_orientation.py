from itertools import (permutations,
                       product)
from typing import Tuple

from hypothesis import given

from ground.base import (Context,
                         Orientation)
from tests.hints import (PointsPair,
                         PointsTriplet)
from tests.utils import (is_even_permutation,
                         permute)
from . import strategies


@given(strategies.contexts_with_points_triplets)
def test_basic(context_with_points_triplet: Tuple[Context, PointsTriplet]
               ) -> None:
    context, points_triplet = context_with_points_triplet
    vertex, first_ray_point, second_ray_point = points_triplet

    result = context.angle_orientation(vertex, first_ray_point,
                                       second_ray_point)

    assert isinstance(result, Orientation)


@given(strategies.contexts_with_points_pairs)
def test_same_endpoints(context_with_points_pair: Tuple[Context, PointsPair]
                        ) -> None:
    context, points_pair = context_with_points_pair

    assert all((context.angle_orientation(vertex, first_ray_point,
                                          second_ray_point)
                is Orientation.COLLINEAR)
               for vertex, first_ray_point, second_ray_point
               in product(points_pair,
                          repeat=3))


@given(strategies.contexts_with_points_triplets)
def test_permutations(context_with_points_triplet
                      : Tuple[Context, PointsTriplet]) -> None:
    context, points_triplet = context_with_points_triplet
    vertex, first_ray_point, second_ray_point = points_triplet

    result = context.angle_orientation(vertex, first_ray_point,
                                       second_ray_point)

    assert all(context.angle_orientation(*permute(points_triplet, permutation))
               is (result
                   if is_even_permutation(permutation)
                   else Orientation(-result))
               for permutation in permutations(range(len(points_triplet))))
