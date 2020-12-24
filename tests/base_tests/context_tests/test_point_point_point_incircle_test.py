from itertools import permutations

from hypothesis import given

from ground.base import Context
from tests.hints import (PointsQuadruplet,
                         PointsTriplet)
from tests.utils import (is_even_permutation,
                         permute,
                         to_sign)
from . import strategies


@given(strategies.contexts, strategies.points_quadruplets)
def test_basic(context: Context,
               points_quadruplet: PointsQuadruplet) -> None:
    first_point, second_point, third_point, fourth_point = points_quadruplet

    result = context.point_point_point_incircle_test(first_point, second_point,
                                                     third_point,
                                                     fourth_point)

    coordinate_cls = type(first_point.x)
    assert isinstance(result, coordinate_cls)


@given(strategies.contexts, strategies.points_triplets)
def test_degenerate_cases(context: Context,
                          points_triplet: PointsTriplet) -> None:
    first_point, second_point, third_point = points_triplet

    assert all(
            not context.point_point_point_incircle_test(
                    first_point, second_point, third_point, point)
            for point in points_triplet)


@given(strategies.contexts, strategies.points_quadruplets)
def test_permutations(context: Context,
                      points_quadruplet: PointsQuadruplet) -> None:
    first_point, second_point, third_point, fourth_point = points_quadruplet

    result = context.point_point_point_incircle_test(first_point, second_point,
                                                     third_point, fourth_point)

    result_sign = to_sign(result)
    assert all(to_sign(
            context.point_point_point_incircle_test(*permute(points_quadruplet,
                                                             permutation)))
               == (result_sign
                   if is_even_permutation(permutation)
                   else -result_sign)
               for permutation in permutations(range(len(points_quadruplet))))