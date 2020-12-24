from itertools import (permutations,
                       product)

from hypothesis import given

from ground.base import (Context,
                         Orientation)
from tests.hints import (PointsPair,
                         PointsTriplet)
from tests.utils import (is_even_permutation,
                         permute)
from . import strategies


@given(strategies.contexts, strategies.points_triplets)
def test_basic(context: Context,
               points_triplet: PointsTriplet) -> None:
    vertex, first_ray_point, second_ray_point = points_triplet

    result = context.orientation(vertex, first_ray_point, second_ray_point)

    assert isinstance(result, Orientation)


@given(strategies.contexts, strategies.points_pairs)
def test_same_endpoints(context: Context,
                        points_pair: PointsPair) -> None:
    assert all((context.orientation(vertex, first_ray_point, second_ray_point)
                is Orientation.COLLINEAR)
               for vertex, first_ray_point, second_ray_point
               in product(points_pair,
                          repeat=3))


@given(strategies.contexts, strategies.points_triplets)
def test_permutations(context: Context,
                      points_triplet: PointsTriplet) -> None:
    vertex, first_ray_point, second_ray_point = points_triplet

    result = context.orientation(vertex, first_ray_point, second_ray_point)

    assert all(context.orientation(*permute(points_triplet, permutation))
               is (result
                   if is_even_permutation(permutation)
                   else Orientation(-result))
               for permutation in permutations(range(len(points_triplet))))
