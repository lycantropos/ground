from collections.abc import Sequence

from hypothesis import given

from ground.context import Context
from ground.hints import Polygon
from tests.hints import ScalarT
from tests.utils import (
    is_box,
    permute,
    reverse_box_coordinates,
    reverse_polygons_coordinates,
    reverse_sequence,
)

from . import strategies


@given(strategies.contexts_with_polygons_sequences)
def test_basic(
    context_with_polygons: tuple[Context[ScalarT], Sequence[Polygon[ScalarT]]],
) -> None:
    context, polygons = context_with_polygons

    result = context.polygons_box(polygons)

    assert is_box(result)


@given(strategies.contexts_with_polygons_sequences)
def test_reversals(
    context_with_polygons: tuple[Context[ScalarT], Sequence[Polygon[ScalarT]]],
) -> None:
    context, polygons = context_with_polygons

    result = context.polygons_box(polygons)

    assert result == context.polygons_box(reverse_sequence(polygons))
    assert result == reverse_box_coordinates(
        context.polygons_box(reverse_polygons_coordinates(polygons))
    )


@given(strategies.contexts_with_polygons_sequences, strategies.indices)
def test_permutations(
    context_with_polygons: tuple[Context[ScalarT], Sequence[Polygon[ScalarT]]],
    index: int,
) -> None:
    context, polygons = context_with_polygons

    result = context.polygons_box(polygons)

    assert result == context.polygons_box(permute(polygons, index))
