from hypothesis import given

from ground.base import Context
from ground.hints import Box, Point
from tests.hints import ScalarT

from . import strategies


@given(strategies.contexts_with_boxes_and_points)
def test_basic(
    context_with_boxes_pair: tuple[
        Context[ScalarT], Box[ScalarT], Point[ScalarT]
    ],
) -> None:
    context, box, point = context_with_boxes_pair

    result = context.box_point_squared_distance(box, point)

    assert isinstance(result, context.coordinate_cls)


@given(strategies.contexts_with_boxes)
def test_self(context_with_box: tuple[Context[ScalarT], Box[ScalarT]]) -> None:
    context, box = context_with_box

    point_cls = context.point_cls
    assert (
        context.box_point_squared_distance(
            box, point_cls(box.min_x, box.min_y)
        )
        == context.box_point_squared_distance(
            box, point_cls(box.max_x, box.min_y)
        )
        == context.box_point_squared_distance(
            box, point_cls(box.max_x, box.max_y)
        )
        == context.box_point_squared_distance(
            box, point_cls(box.min_x, box.max_y)
        )
        == context.zero
    )
