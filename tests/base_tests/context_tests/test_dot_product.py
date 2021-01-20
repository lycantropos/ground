from itertools import (permutations,
                       product)
from typing import Tuple

from hypothesis import given

from ground.base import Context
from tests.hints import (PointsPair,
                         PointsQuadruplet)
from tests.utils import (context_to_output_coordinate_cls,
                         equivalence,
                         is_even_permutation,
                         permute,
                         to_perpendicular_point,
                         to_sign)
from . import strategies


@given(strategies.contexts_with_points_quadruplets)
def test_basic(context_with_points_quadruplet: Tuple[Context, PointsQuadruplet]
               ) -> None:
    context, points_quadruplet = context_with_points_quadruplet
    first_start, first_end, second_start, second_end = points_quadruplet

    result = context.dot_product(first_start, first_end, second_start,
                                 second_end)

    assert isinstance(result, context_to_output_coordinate_cls(context))


@given(strategies.contexts_with_points_pairs)
def test_perpendicular_endpoints(context_with_points_pair
                                 : Tuple[Context, PointsPair]) -> None:
    context, points_pair = context_with_points_pair
    first_start, first_end = points_pair

    assert not context.dot_product(first_start, first_end,
                                   to_perpendicular_point(first_start),
                                   to_perpendicular_point(first_end))


@given(strategies.contexts_with_points_quadruplets)
def test_segments_permutation(context_with_points_quadruplet
                              : Tuple[Context, PointsQuadruplet]) -> None:
    context, points_quadruplet = context_with_points_quadruplet
    first_start, first_end, second_start, second_end = points_quadruplet

    result = context.dot_product(first_start, first_end, second_start,
                                 second_end)

    assert result == context.dot_product(second_start, second_end, first_start,
                                         first_end)


@given(strategies.contexts_with_points_quadruplets)
def test_endpoints_permutations(context_with_points_quadruplet
                                : Tuple[Context, PointsQuadruplet]) -> None:
    context, points_quadruplet = context_with_points_quadruplet
    first_start, first_end, second_start, second_end = points_quadruplet

    result = context.dot_product(first_start, first_end, second_start,
                                 second_end)

    result_sign = to_sign(result)
    first_endpoints = first_start, first_end
    second_endpoints = second_start, second_end
    assert all(to_sign(context.dot_product(*permute(first_endpoints,
                                                    first_permutation),
                                           *permute(second_endpoints,
                                                    second_permutation)))
               == (result_sign
                   if equivalence(is_even_permutation(first_permutation),
                                  is_even_permutation(second_permutation))
                   else -result_sign)
               for first_permutation, second_permutation
               in product(permutations(range(len(first_endpoints))),
                          permutations(range(len(second_endpoints)))))
