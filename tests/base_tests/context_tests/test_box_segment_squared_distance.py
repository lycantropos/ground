from typing import Tuple

from hypothesis import given

from ground.base import Context
from ground.hints import (Box,
                          Point)
from tests.utils import is_coordinate
from . import strategies


@given(strategies.contexts_with_boxes_and_segments_endpoints)
def test_basic(context_with_boxes_pair: Tuple[Context, Box, Point]) -> None:
    context, box, (start, end) = context_with_boxes_pair

    result = context.box_segment_squared_distance(box, start, end)

    assert is_coordinate(result)


@given(strategies.contexts_with_boxes_and_segments_endpoints)
def test_endpoints_symmetry(context_with_boxes_pair: Tuple[Context, Box, Point]
                            ) -> None:
    context, box, (start, end) = context_with_boxes_pair

    result = context.box_segment_squared_distance(box, start, end)

    assert result == context.box_segment_squared_distance(box, end, start)


@given(strategies.contexts_with_boxes)
def test_self(context_with_box: Tuple[Context, Box]) -> None:
    context, box = context_with_box

    point_cls = context.point_cls
    bottom_left, bottom_right = (point_cls(box.min_x, box.min_y),
                                 point_cls(box.max_x, box.min_y))
    top_left, top_right = (point_cls(box.min_x, box.max_y),
                           point_cls(box.max_x, box.max_y))
    assert (context.box_segment_squared_distance(box, bottom_left,
                                                 bottom_right)
            == context.box_segment_squared_distance(box, bottom_right,
                                                    top_right)
            == context.box_segment_squared_distance(box, top_right, top_left)
            == context.box_segment_squared_distance(box, top_left, bottom_left)
            == 0)
