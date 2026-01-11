from hypothesis import given

from ground.context import Context
from ground.enums import Location
from tests.hints import PointsQuadruplet, PointsTriplet, ScalarT
from tests.utils import is_even_permutation, permute, to_opposite_location

from . import strategies


@given(strategies.contexts_with_points_quadruplets)
def test_basic(
    context_with_points_quadruplet: tuple[
        Context[ScalarT], PointsQuadruplet[ScalarT]
    ],
) -> None:
    context, points_quadruplet = context_with_points_quadruplet
    point, first_point, second_point, third_point = points_quadruplet

    result = context.locate_point_in_point_point_point_circle(
        point, first_point, second_point, third_point
    )

    assert isinstance(result, Location)


@given(strategies.contexts_with_points_triplets)
def test_degenerate_cases(
    context_with_points_triplet: tuple[
        Context[ScalarT], PointsTriplet[ScalarT]
    ],
) -> None:
    context, points_triplet = context_with_points_triplet
    first_point, second_point, third_point = points_triplet

    assert all(
        context.locate_point_in_point_point_point_circle(
            point, first_point, second_point, third_point
        )
        is Location.BOUNDARY
        for point in points_triplet
    )


@given(strategies.contexts_with_points_quadruplets, strategies.indices)
def test_permutations(
    context_with_points_quadruplet: tuple[
        Context[ScalarT], PointsQuadruplet[ScalarT]
    ],
    index: int,
) -> None:
    context, points_quadruplet = context_with_points_quadruplet
    point, first_point, second_point, third_point = points_quadruplet

    result = context.locate_point_in_point_point_point_circle(
        point, first_point, second_point, third_point
    )

    assert context.locate_point_in_point_point_point_circle(
        *permute(points_quadruplet, index)
    ) is (
        result
        if is_even_permutation(index, len(points_quadruplet))
        else to_opposite_location(result)
    )
