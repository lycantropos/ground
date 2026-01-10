from ground._core.hints import (
    Box,
    Point,
    QuaternaryPointFunction,
    ScalarFactory,
    ScalarT,
    Segment,
)
from ground._core.primitive import square

from .segment import (
    point_squared_distance as segment_point_squared_distance,
    segment_squared_distance as segment_segment_squared_distance,
)


def point_squared_distance(
    box: Box[ScalarT],
    point: Point[ScalarT],
    coordinate_factory: ScalarFactory[ScalarT],
    /,
) -> ScalarT:
    return square(
        _linear_interval_distance(
            box.min_x, box.max_x, point.x, coordinate_factory
        )
    ) + square(
        _linear_interval_distance(
            box.min_y, box.max_y, point.y, coordinate_factory
        )
    )


def segment_squared_distance(
    box: Box[ScalarT],
    segment: Segment[ScalarT],
    dot_producer: QuaternaryPointFunction[ScalarT, ScalarT],
    segments_collision_detector: QuaternaryPointFunction[ScalarT, bool],
    coordinate_factory: ScalarFactory[ScalarT],
    point_cls: type[Point[ScalarT]],
    /,
) -> ScalarT:
    segment_start, segment_end = segment.start, segment.end
    min_x, min_y, max_x, max_y = box.min_x, box.min_y, box.max_x, box.max_y
    return (
        coordinate_factory(0)
        if (
            (
                min_x <= segment_start.x <= max_x
                and min_y <= segment_start.y <= max_y
            )
            or (
                min_x <= segment_end.x <= max_x
                and min_y <= segment_end.y <= max_y
            )
        )
        else (
            (
                segment_point_squared_distance(
                    segment_start,
                    segment_end,
                    point_cls(min_x, min_y),
                    dot_producer,
                    coordinate_factory,
                )
                if min_y == max_y
                else segment_segment_squared_distance(
                    segment_start,
                    segment_end,
                    point_cls(min_x, min_y),
                    point_cls(min_x, max_y),
                    dot_producer,
                    segments_collision_detector,
                    coordinate_factory,
                )
            )
            if min_x == max_x
            else (
                segment_segment_squared_distance(
                    segment_start,
                    segment_end,
                    point_cls(min_x, min_y),
                    point_cls(max_x, min_y),
                    dot_producer,
                    segments_collision_detector,
                    coordinate_factory,
                )
                if min_y == max_y
                else _non_degenerate_segment_squared_distance(
                    max_x,
                    max_y,
                    min_x,
                    min_y,
                    segment_start,
                    segment_end,
                    dot_producer,
                    segments_collision_detector,
                    coordinate_factory,
                    point_cls,
                )
            )
        )
    )


def _linear_interval_distance(
    min_coordinate: ScalarT,
    max_coordinate: ScalarT,
    coordinate: ScalarT,
    coordinate_factory: ScalarFactory[ScalarT],
    /,
) -> ScalarT:
    return (
        min_coordinate - coordinate
        if coordinate < min_coordinate
        else (
            coordinate - max_coordinate
            if coordinate > max_coordinate
            else coordinate_factory(0)
        )
    )


def _non_degenerate_segment_squared_distance(
    max_x: ScalarT,
    max_y: ScalarT,
    min_x: ScalarT,
    min_y: ScalarT,
    segment_start: Point[ScalarT],
    segment_end: Point[ScalarT],
    dot_producer: QuaternaryPointFunction[ScalarT, ScalarT],
    segments_relater: QuaternaryPointFunction[ScalarT, bool],
    coordinate_factory: ScalarFactory[ScalarT],
    point_cls: type[Point[ScalarT]],
    /,
) -> ScalarT:
    bottom_left, bottom_right = (
        point_cls(min_x, min_y),
        point_cls(max_x, min_y),
    )
    bottom_side_distance = segment_segment_squared_distance(
        segment_start,
        segment_end,
        bottom_left,
        bottom_right,
        dot_producer,
        segments_relater,
        coordinate_factory,
    )
    if not bottom_side_distance:
        return bottom_side_distance
    top_right = point_cls(max_x, max_y)
    right_side_distance = segment_segment_squared_distance(
        segment_start,
        segment_end,
        bottom_right,
        top_right,
        dot_producer,
        segments_relater,
        coordinate_factory,
    )
    if not right_side_distance:
        return right_side_distance
    top_left = point_cls(min_x, max_y)
    top_side_distance = segment_segment_squared_distance(
        segment_start,
        segment_end,
        top_left,
        top_right,
        dot_producer,
        segments_relater,
        coordinate_factory,
    )
    if not top_side_distance:
        return top_side_distance
    left_side_distance = segment_segment_squared_distance(
        segment_start,
        segment_end,
        bottom_left,
        top_left,
        dot_producer,
        segments_relater,
        coordinate_factory,
    )
    return left_side_distance and min(
        bottom_side_distance,
        right_side_distance,
        top_side_distance,
        left_side_distance,
    )
