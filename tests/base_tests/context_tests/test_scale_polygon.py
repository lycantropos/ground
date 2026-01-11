from hypothesis import given

from ground.context import Context
from ground.hints import Polygon
from tests.hints import ScalarT
from tests.utils import (
    reverse_geometry_coordinates,
    reverse_polygon_border,
    reverse_polygon_coordinates,
    reverse_polygon_holes,
)

from . import strategies


@given(strategies.contexts_with_polygons_and_scalars_pairs)
def test_basic(
    context_with_polygon_and_factors: tuple[
        Context[ScalarT], Polygon[ScalarT], ScalarT, ScalarT
    ],
) -> None:
    context, polygon, factor_x, factor_y = context_with_polygon_and_factors

    result = context.scale_polygon(polygon, factor_x, factor_y)

    assert isinstance(
        result,
        (context.multipoint_cls, context.polygon_cls, context.segment_cls),
    )


@given(strategies.contexts_with_polygons_and_scalars_pairs)
def test_reversals(
    context_with_polygon_and_factors: tuple[
        Context[ScalarT], Polygon[ScalarT], ScalarT, ScalarT
    ],
) -> None:
    context, polygon, factor_x, factor_y = context_with_polygon_and_factors

    result = context.scale_polygon(polygon, factor_x, factor_y)

    assert not isinstance(
        result, context.polygon_cls
    ) or reverse_polygon_border(result) == context.scale_polygon(
        reverse_polygon_border(polygon), factor_x, factor_y
    )
    assert not isinstance(
        result, context.polygon_cls
    ) or reverse_polygon_holes(result) == context.scale_polygon(
        reverse_polygon_holes(polygon), factor_x, factor_y
    )
    assert reverse_geometry_coordinates(result) == context.scale_polygon(
        reverse_polygon_coordinates(polygon), factor_y, factor_x
    )
