from hypothesis import given

from ground.base import Context
from ground.hints import Polygon
from tests.hints import ScalarT
from tests.utils import (
    reverse_polygon_border,
    reverse_polygon_coordinates,
    reverse_polygon_holes,
)

from . import strategies


@given(strategies.contexts_with_polygons_and_scalars_pairs)
def test_basic(
    context_with_polygon_and_steps: tuple[
        Context[ScalarT], Polygon[ScalarT], ScalarT, ScalarT
    ],
) -> None:
    context, polygon, step_x, step_y = context_with_polygon_and_steps

    result = context.translate_polygon(polygon, step_x, step_y)

    assert isinstance(result, context.polygon_cls)


@given(strategies.contexts_with_rational_polygons_and_scalars_pairs)
def test_round_trip(
    context_with_polygon_and_steps: tuple[
        Context[ScalarT], Polygon[ScalarT], ScalarT, ScalarT
    ],
) -> None:
    context, polygon, step_x, step_y = context_with_polygon_and_steps

    result = context.translate_polygon(polygon, step_x, step_y)

    assert context.translate_polygon(
        result, -step_x, -step_y
    ) == context.translate_polygon(polygon, context.zero, context.zero)


@given(strategies.contexts_with_polygons_and_scalars_pairs)
def test_reversals(
    context_with_polygon_and_steps: tuple[
        Context[ScalarT], Polygon[ScalarT], ScalarT, ScalarT
    ],
) -> None:
    context, polygon, step_x, step_y = context_with_polygon_and_steps

    result = context.translate_polygon(polygon, step_x, step_y)

    assert reverse_polygon_border(result) == context.translate_polygon(
        reverse_polygon_border(polygon), step_x, step_y
    )
    assert reverse_polygon_holes(result) == context.translate_polygon(
        reverse_polygon_holes(polygon), step_x, step_y
    )
    assert reverse_polygon_coordinates(result) == context.translate_polygon(
        reverse_polygon_coordinates(polygon), step_y, step_x
    )
