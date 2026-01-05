from hypothesis import given

from ground.base import Context
from ground.hints import Box, Segment
from tests.hints import ScalarT
from tests.utils import reverse_segment

from . import strategies


@given(strategies.contexts_with_boxes_and_segments)
def test_basic(
    context_with_box_and_segment: tuple[
        Context[ScalarT], Box[ScalarT], Segment[ScalarT]
    ],
) -> None:
    context, box, segment = context_with_box_and_segment

    result = context.box_segment_squared_distance(box, segment)

    assert context.coordinate_checker(result)


@given(strategies.contexts_with_rational_boxes_and_segments)
def test_endpoints_symmetry(
    context_with_box_and_segment: tuple[
        Context[ScalarT], Box[ScalarT], Segment[ScalarT]
    ],
) -> None:
    context, box, segment = context_with_box_and_segment

    result = context.box_segment_squared_distance(box, segment)

    assert result == context.box_segment_squared_distance(
        box, reverse_segment(segment)
    )


@given(strategies.contexts_with_boxes)
def test_self(context_with_box: tuple[Context[ScalarT], Box[ScalarT]]) -> None:
    context, box = context_with_box

    point_cls, segment_cls = context.point_cls, context.segment_cls
    bottom_left, bottom_right = (
        point_cls(box.min_x, box.min_y),
        point_cls(box.max_x, box.min_y),
    )
    top_left, top_right = (
        point_cls(box.min_x, box.max_y),
        point_cls(box.max_x, box.max_y),
    )
    assert (
        context.box_segment_squared_distance(
            box, segment_cls(bottom_left, bottom_right)
        )
        == context.box_segment_squared_distance(
            box, segment_cls(bottom_right, top_right)
        )
        == context.box_segment_squared_distance(
            box, segment_cls(top_right, top_left)
        )
        == context.box_segment_squared_distance(
            box, segment_cls(top_left, bottom_left)
        )
        == context.zero
    )
