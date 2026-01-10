from ground._core.hints import (
    Point,
    QuaternaryPointFunction,
    ScalarFactory,
    ScalarT,
)
from ground._core.primitive import square

from .point import point_squared_distance as point_point_squared_distance


def point_squared_distance(
    start: Point[ScalarT],
    end: Point[ScalarT],
    point: Point[ScalarT],
    dot_producer: QuaternaryPointFunction[ScalarT, ScalarT],
    coordinate_factory: ScalarFactory[ScalarT],
    /,
) -> ScalarT:
    end_factor = max(
        coordinate_factory(0),
        min(
            coordinate_factory(1),
            (
                dot_producer(start, point, start, end)
                / point_point_squared_distance(start, end)
            ),
        ),
    )
    start_factor = coordinate_factory(1) - end_factor
    return square(
        start_factor * start.x + end_factor * end.x - point.x
    ) + square(start_factor * start.y + end_factor * end.y - point.y)


def segment_squared_distance(
    first_start: Point[ScalarT],
    first_end: Point[ScalarT],
    second_start: Point[ScalarT],
    second_end: Point[ScalarT],
    dot_producer: QuaternaryPointFunction[ScalarT, ScalarT],
    segments_collision_detector: QuaternaryPointFunction[ScalarT, bool],
    coordinate_factory: ScalarFactory[ScalarT],
    /,
) -> ScalarT:
    return (
        coordinate_factory(0)
        if segments_collision_detector(
            first_start, first_end, second_start, second_end
        )
        else min(
            point_squared_distance(
                first_start,
                first_end,
                second_start,
                dot_producer,
                coordinate_factory,
            ),
            point_squared_distance(
                first_start,
                first_end,
                second_end,
                dot_producer,
                coordinate_factory,
            ),
            point_squared_distance(
                second_start,
                second_end,
                first_start,
                dot_producer,
                coordinate_factory,
            ),
            point_squared_distance(
                second_start,
                second_end,
                first_end,
                dot_producer,
                coordinate_factory,
            ),
        )
    )
