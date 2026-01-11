from hypothesis import given

from ground.context import Context
from ground.hints import Multipoint
from tests.hints import ScalarT
from tests.utils import is_point, permute_multipoint, reverse_multipoint

from . import strategies


@given(strategies.contexts_with_multipoints)
def test_basic(
    context_with_points: tuple[Context[ScalarT], Multipoint[ScalarT]],
) -> None:
    context, multipoint = context_with_points

    result = context.multipoint_centroid(multipoint)

    assert is_point(result)


@given(strategies.contexts_with_rational_multipoints)
def test_reversals(
    context_with_points: tuple[Context[ScalarT], Multipoint[ScalarT]],
) -> None:
    context, multipoint = context_with_points

    result = context.multipoint_centroid(multipoint)

    assert result == context.multipoint_centroid(
        reverse_multipoint(multipoint)
    )


@given(strategies.contexts_with_rational_multipoints, strategies.indices)
def test_permutations(
    context_with_points: tuple[Context[ScalarT], Multipoint[ScalarT]],
    index: int,
) -> None:
    context, multipoint = context_with_points

    result = context.multipoint_centroid(multipoint)

    assert result == context.multipoint_centroid(
        permute_multipoint(multipoint, index)
    )
