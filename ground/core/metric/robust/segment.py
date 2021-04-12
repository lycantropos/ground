from typing import Type

from ground.core.enums import Relation
from ground.core.hints import (Coordinate,
                               Point,
                               QuaternaryPointFunction)
from .point import point_squared_distance as point_point_squared_distance


def point_squared_distance(segment_start: Point,
                           segment_end: Point,
                           point: Point,
                           dot_producer: QuaternaryPointFunction[Coordinate],
                           point_cls: Type[Point]) -> Coordinate:
    end_factor = max(0, min(1,
                            dot_producer(segment_start, point, segment_start,
                                         segment_end)
                            / point_point_squared_distance(segment_start,
                                                           segment_end)))
    start_factor = 1 - end_factor
    return point_point_squared_distance(
            point_cls(start_factor * segment_start.x
                      + end_factor * segment_end.x,
                      start_factor * segment_start.y
                      + end_factor * segment_end.y),
            point)


def segment_squared_distance(first_start: Point,
                             first_end: Point,
                             second_start: Point,
                             second_end: Point,
                             dot_producer
                             : QuaternaryPointFunction[Coordinate],
                             segments_relater
                             : QuaternaryPointFunction[Relation],
                             point_cls: Type[Point]) -> Coordinate:
    return (min(point_squared_distance(first_start, first_end, second_start,
                                       dot_producer, point_cls),
                point_squared_distance(first_start, first_end, second_end,
                                       dot_producer, point_cls),
                point_squared_distance(second_start, second_end, first_start,
                                       dot_producer, point_cls),
                point_squared_distance(second_start, second_end, first_end,
                                       dot_producer, point_cls))
            if segments_relater(first_start, first_end, second_start,
                                second_end) is Relation.DISJOINT
            else 0)
