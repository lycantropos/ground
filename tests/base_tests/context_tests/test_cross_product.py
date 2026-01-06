from hypothesis import given

from ground.base import Context
from tests.hints import PointsPair, PointsQuadruplet, ScalarT
from tests.utils import equivalence, is_even_permutation, permute, to_sign

from . import strategies


@given(strategies.contexts_with_points_quadruplets)
def test_basic(
    context_with_points_quadruplet: tuple[
        Context[ScalarT], PointsQuadruplet[ScalarT]
    ],
) -> None:
    context, points_quadruplet = context_with_points_quadruplet
    first_start, first_end, second_start, second_end = points_quadruplet

    result = context.cross_product(
        first_start, first_end, second_start, second_end
    )

    assert context.coordinate_checker(result)


@given(strategies.contexts_with_points_pairs)
def test_same_endpoints(
    context_with_points_pair: tuple[Context[ScalarT], PointsPair[ScalarT]],
) -> None:
    context, points_pair = context_with_points_pair
    first_start, first_end = points_pair

    assert not context.cross_product(
        first_start, first_end, first_start, first_end
    )


@given(strategies.contexts_with_points_quadruplets)
def test_segments_permutation(
    context_with_points_quadruplet: tuple[
        Context[ScalarT], PointsQuadruplet[ScalarT]
    ],
) -> None:
    context, points_quadruplet = context_with_points_quadruplet
    first_start, first_end, second_start, second_end = points_quadruplet

    result = context.cross_product(
        first_start, first_end, second_start, second_end
    )

    assert result == -context.cross_product(
        second_start, second_end, first_start, first_end
    )


@given(
    strategies.contexts_with_points_quadruplets,
    strategies.indices,
    strategies.indices,
)
def test_endpoints_permutations(
    context_with_points_quadruplet: tuple[
        Context[ScalarT], PointsQuadruplet[ScalarT]
    ],
    first_index: int,
    second_index: int,
) -> None:
    context, points_quadruplet = context_with_points_quadruplet
    first_start, first_end, second_start, second_end = points_quadruplet

    result = context.cross_product(
        first_start, first_end, second_start, second_end
    )

    result_sign = to_sign(result, context.zero)
    first_endpoints = first_start, first_end
    second_endpoints = second_start, second_end
    assert to_sign(
        context.cross_product(
            *permute(first_endpoints, first_index),
            *permute(second_endpoints, second_index),
        ),
        context.zero,
    ) == (
        result_sign
        if equivalence(
            is_even_permutation(first_index, len(first_endpoints)),
            is_even_permutation(second_index, len(second_endpoints)),
        )
        else -result_sign
    )
