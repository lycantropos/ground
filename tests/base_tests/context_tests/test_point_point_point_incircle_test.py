from itertools import permutations
from typing import Tuple

from hypothesis import given

from ground.base import Context
from tests.hints import (PointsQuadruplet,
                         PointsTriplet)
from tests.utils import (context_to_output_coordinate_cls,
                         is_even_permutation,
                         permute,
                         to_sign)
from . import strategies


@given(strategies.contexts_with_points_quadruplets)
def test_basic(context_with_points_quadruplet: Tuple[Context, PointsQuadruplet]
               ) -> None:
    context, points_quadruplet = context_with_points_quadruplet
    first_point, second_point, third_point, fourth_point = points_quadruplet

    result = context.point_point_point_incircle_test(first_point, second_point,
                                                     third_point, fourth_point)

    assert isinstance(result, context_to_output_coordinate_cls(context))


@given(strategies.contexts_with_points_triplets)
def test_degenerate_cases(context_with_points_triplet
                          : Tuple[Context, PointsTriplet]) -> None:
    context, points_triplet = context_with_points_triplet
    first_point, second_point, third_point = points_triplet

    assert all(not context.point_point_point_incircle_test(first_point,
                                                           second_point,
                                                           third_point, point)
               for point in points_triplet)


@given(strategies.contexts_with_points_quadruplets)
def test_permutations(context_with_points_quadruplet
                      : Tuple[Context, PointsQuadruplet]) -> None:
    context, points_quadruplet = context_with_points_quadruplet
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
