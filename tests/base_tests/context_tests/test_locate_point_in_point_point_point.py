from typing import Tuple

from hypothesis import given

from ground.base import (Context,
                         Location)
from tests.hints import (PointsQuadruplet,
                         PointsTriplet)
from tests.utils import (is_even_permutation,
                         permute,
                         to_opposite_location)
from . import strategies


@given(strategies.contexts_with_points_quadruplets)
def test_basic(context_with_points_quadruplet: Tuple[Context, PointsQuadruplet]
               ) -> None:
    context, points_quadruplet = context_with_points_quadruplet
    first_point, second_point, third_point, fourth_point = points_quadruplet

    result = context.locate_point_in_point_point_point_circle(
            first_point, second_point, third_point, fourth_point)

    assert isinstance(result, Location)


@given(strategies.contexts_with_points_triplets)
def test_degenerate_cases(context_with_points_triplet
                          : Tuple[Context, PointsTriplet]) -> None:
    context, points_triplet = context_with_points_triplet
    first_point, second_point, third_point = points_triplet

    assert all(
            context.locate_point_in_point_point_point_circle(
                    first_point, second_point, third_point, point)
            is Location.BOUNDARY
            for point in points_triplet)


@given(strategies.contexts_with_points_quadruplets, strategies.indices)
def test_permutations(context_with_points_quadruplet: Tuple[Context,
                                                            PointsQuadruplet],
                      index: int) -> None:
    context, points_quadruplet = context_with_points_quadruplet
    first_point, second_point, third_point, fourth_point = points_quadruplet

    result = context.locate_point_in_point_point_point_circle(first_point,
                                                              second_point,
                                                              third_point,
                                                              fourth_point)

    assert (context.locate_point_in_point_point_point_circle(
            *permute(points_quadruplet, index))
            is (result
                if is_even_permutation(index, len(points_quadruplet))
                else to_opposite_location(result)))
