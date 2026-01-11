from hypothesis import given

from ground.context import Context
from ground.hints import Multipolygon
from tests.hints import ScalarT
from tests.utils import (
    reverse_multipolygon,
    reverse_multipolygon_coordinates,
    reverse_point_coordinates,
    rotate_multipolygon,
)

from . import strategies


@given(strategies.contexts_with_multipolygons)
def test_basic(
    context_with_polygons: tuple[Context[ScalarT], Multipolygon[ScalarT]],
) -> None:
    context, polygons = context_with_polygons

    result = context.multipolygon_centroid(polygons)

    assert isinstance(result, context.point_cls)


@given(strategies.contexts_with_rational_multipolygons)
def test_reversals(
    context_with_polygons: tuple[Context[ScalarT], Multipolygon[ScalarT]],
) -> None:
    context, multipolygon = context_with_polygons

    result = context.multipolygon_centroid(multipolygon)

    assert result == context.multipolygon_centroid(
        reverse_multipolygon(multipolygon)
    )
    assert reverse_point_coordinates(result) == context.multipolygon_centroid(
        reverse_multipolygon_coordinates(multipolygon)
    )


@given(strategies.contexts_with_rational_multipolygons, strategies.indices)
def test_rotations(
    context_with_polygons: tuple[Context[ScalarT], Multipolygon[ScalarT]],
    offset: int,
) -> None:
    context, polygons = context_with_polygons

    result = context.multipolygon_centroid(polygons)

    assert result == context.multipolygon_centroid(
        rotate_multipolygon(polygons, offset)
    )
