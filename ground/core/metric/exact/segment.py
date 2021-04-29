from ground.core.hints import (Point,
                               QuaternaryPointFunction,
                               Scalar)
from ground.core.primitive import rationalize
from .point import point_squared_distance as point_point_squared_distance


def point_squared_distance(segment_start: Point,
                           segment_end: Point,
                           point: Point,
                           dot_producer: QuaternaryPointFunction[Scalar]
                           ) -> Scalar:
    end_factor = max(0, min(1,
                            dot_producer(segment_start, point, segment_start,
                                         segment_end)
                            / point_point_squared_distance(segment_start,
                                                           segment_end)))
    start_factor = 1 - end_factor
    return ((start_factor * rationalize(segment_start.x)
             + end_factor * rationalize(segment_end.x)
             - rationalize(point.x)) ** 2
            + (start_factor * rationalize(segment_start.y)
               + end_factor * rationalize(segment_end.y)
               - rationalize(point.y)) ** 2)


def segment_squared_distance(first_start: Point,
                             first_end: Point,
                             second_start: Point,
                             second_end: Point,
                             dot_producer: QuaternaryPointFunction[Scalar],
                             segments_collision_detector
                             : QuaternaryPointFunction[bool]) -> Scalar:
    return (0
            if segments_collision_detector(first_start, first_end,
                                           second_start, second_end)
            else min(point_squared_distance(first_start, first_end,
                                            second_start, dot_producer),
                     point_squared_distance(first_start, first_end, second_end,
                                            dot_producer),
                     point_squared_distance(second_start, second_end,
                                            first_start, dot_producer),
                     point_squared_distance(second_start, second_end,
                                            first_end, dot_producer)))
