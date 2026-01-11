from hypothesis import given

from ground.context import Context
from ground.hints import Polygon
from tests.hints import ScalarT
from tests.utils import (
    reverse_point_coordinates,
    reverse_polygon_border,
    reverse_polygon_coordinates,
    reverse_polygon_holes,
    rotate_polygon_border,
    rotate_polygon_holes,
)

from . import strategies


@given(strategies.contexts_with_polygons)
def test_basic(
    context_with_polygon: tuple[Context[ScalarT], Polygon[ScalarT]],
) -> None:
    context, polygon = context_with_polygon

    result = context.polygon_centroid(polygon)

    assert isinstance(result, context.point_cls)


@given(strategies.contexts_with_rational_polygons)
def test_reversals(
    context_with_polygon: tuple[Context[ScalarT], Polygon[ScalarT]],
) -> None:
    context, polygon = context_with_polygon

    result = context.polygon_centroid(polygon)

    assert (
        result
        == context.polygon_centroid(reverse_polygon_border(polygon))
        == context.polygon_centroid(reverse_polygon_holes(polygon))
    )
    assert reverse_point_coordinates(result) == context.polygon_centroid(
        reverse_polygon_coordinates(polygon)
    )


@given(strategies.contexts_with_rational_polygons, strategies.indices)
def test_rotations(
    context_with_polygon: tuple[Context[ScalarT], Polygon[ScalarT]],
    offset: int,
) -> None:
    context, polygon = context_with_polygon

    result = context.polygon_centroid(polygon)

    assert result == context.polygon_centroid(
        rotate_polygon_border(polygon, offset)
    )
    assert result == context.polygon_centroid(
        rotate_polygon_holes(polygon, offset)
    )
