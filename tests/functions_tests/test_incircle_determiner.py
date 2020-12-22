from itertools import permutations

from hypothesis import given

from tests.hints import (IncircleDeterminer,
                         PointsQuadruplet,
                         PointsTriplet)
from tests.utils import (is_even_permutation,
                         permute,
                         to_sign)
from . import strategies


@given(strategies.incircle_determiners, strategies.points_quadruplets)
def test_basic(incircle_determiner: IncircleDeterminer,
               points_quadruplet: PointsQuadruplet) -> None:
    first_point, second_point, third_point, fourth_point = points_quadruplet

    result = incircle_determiner(first_point, second_point, third_point,
                                 fourth_point)

    coordinate_cls = type(first_point.x)
    assert isinstance(result, coordinate_cls)


@given(strategies.incircle_determiners, strategies.points_triplets)
def test_degenerate_cases(incircle_determiner: IncircleDeterminer,
                          points_triplet: PointsTriplet) -> None:
    first_point, second_point, third_point = points_triplet

    assert all(not incircle_determiner(first_point, second_point, third_point,
                                       point)
               for point in points_triplet)


@given(strategies.incircle_determiners, strategies.rational_points_quadruplets)
def test_permutations(incircle_determiner: IncircleDeterminer,
                      points_quadruplet: PointsQuadruplet) -> None:
    first_point, second_point, third_point, fourth_point = points_quadruplet

    result = incircle_determiner(first_point, second_point, third_point,
                                 fourth_point)

    result_sign = to_sign(result)
    assert all(to_sign(incircle_determiner(*permute(points_quadruplet,
                                                    permutation)))
               == (result_sign
                   if is_even_permutation(permutation)
                   else -result_sign)
               for permutation in permutations(range(len(points_quadruplet))))
