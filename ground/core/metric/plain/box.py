from typing import Type

from ground.core.enums import Relation
from ground.core.hints import (Box,
                               Coordinate,
                               Point,
                               QuaternaryPointFunction)
from .segment import (point_squared_distance as point_point_squared_distance,
                      segment_squared_distance
                      as segment_segment_squared_distance)


def point_squared_distance(box: Box, point: Point) -> Coordinate:
    return (_linear_interval_distance(box.min_x, box.max_x, point.x) ** 2
            + _linear_interval_distance(box.min_y, box.max_y, point.y) ** 2)


def segment_squared_distance(box: Box,
                             segment_start: Point,
                             segment_end: Point,
                             dot_producer: QuaternaryPointFunction[Coordinate],
                             segments_relater
                             : QuaternaryPointFunction[Relation],
                             point_cls: Type[Point]) -> Coordinate:
    min_x, min_y, max_x, max_y = box.min_x, box.min_y, box.max_x, box.max_y
    return (0
            if ((min_x <= segment_start.x <= max_x
                 and min_y <= segment_start.y <= max_y)
                or (min_x <= segment_end.x <= max_x
                    and min_y <= segment_end.y <= max_y))
            else
            ((point_point_squared_distance(segment_start, segment_end,
                                           point_cls(min_x, min_y),
                                           dot_producer, point_cls)
              if min_y == max_y
              else segment_segment_squared_distance(
                    segment_start, segment_end, point_cls(min_x, min_y),
                    point_cls(min_x, max_y), dot_producer, segments_relater,
                    point_cls))
             if min_x == max_x
             else (segment_segment_squared_distance(
                    segment_start, segment_end, point_cls(min_x, min_y),
                    point_cls(max_x, min_y), dot_producer, segments_relater,
                    point_cls)
                   if min_y == max_y
                   else _non_degenerate_segment_squared_distance(
                    max_x, max_y, min_x, min_y, segment_start, segment_end,
                    dot_producer, segments_relater, point_cls))))


def _linear_interval_distance(min_coordinate: Coordinate,
                              max_coordinate: Coordinate,
                              coordinate: Coordinate) -> Coordinate:
    return (min_coordinate - coordinate
            if coordinate < min_coordinate
            else (coordinate - max_coordinate
                  if coordinate > max_coordinate
                  else 0))


def _non_degenerate_segment_squared_distance(
        max_x: Coordinate,
        max_y: Coordinate,
        min_x: Coordinate,
        min_y: Coordinate,
        segment_start: Point,
        segment_end: Point,
        dot_producer: QuaternaryPointFunction[Coordinate],
        segments_relater: QuaternaryPointFunction[Relation],
        point_cls: Type[Point]) -> Coordinate:
    bottom_left, bottom_right = (point_cls(min_x, min_y),
                                 point_cls(max_x, min_y))
    bottom_side_distance = segment_segment_squared_distance(
            segment_start, segment_end, bottom_left, bottom_right,
            dot_producer, segments_relater, point_cls)
    if not bottom_side_distance:
        return bottom_side_distance
    top_right = point_cls(max_x, max_y)
    right_side_distance = segment_segment_squared_distance(
            segment_start, segment_end, bottom_right, top_right, dot_producer,
            segments_relater, point_cls)
    if not right_side_distance:
        return right_side_distance
    top_left = point_cls(min_x, max_y)
    top_side_distance = segment_segment_squared_distance(
            segment_start, segment_end, top_left, top_right, dot_producer,
            segments_relater, point_cls)
    if not top_side_distance:
        return top_side_distance
    left_side_distance = segment_segment_squared_distance(
            segment_start, segment_end, bottom_left, top_left, dot_producer,
            segments_relater, point_cls)
    return (left_side_distance
            and min(bottom_side_distance, right_side_distance,
                    top_side_distance, left_side_distance))
