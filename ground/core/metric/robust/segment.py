from shewchuk import Expansion

from ground.core.enums import Relation
from ground.core.hints import (Point,
                               QuaternaryPointFunction,
                               Scalar)
from ground.core.primitive import square


def point_squared_distance(start: Point,
                           end: Point,
                           point: Point,
                           dot_producer: QuaternaryPointFunction[Scalar]
                           ) -> Scalar:
    segment_squared_norm = dot_producer(start, end, start, end)
    point_end_projection = dot_producer(point, end, start, end)
    start_point_projection = dot_producer(start, point, start, end)
    start_factor = ((point_end_projection
                     if point_end_projection > 0
                     else 0)
                    if point_end_projection < segment_squared_norm
                    else segment_squared_norm)
    end_factor = ((start_point_projection
                   if start_point_projection > 0
                   else 0)
                  if start_point_projection < segment_squared_norm
                  else segment_squared_norm)
    return ((square(segment_squared_norm * Expansion(start.x, -point.x)
                    + end_factor * Expansion(end.x, -start.x))
             + square(segment_squared_norm * Expansion(start.y, -point.y)
                      + end_factor * Expansion(end.y, -start.y))
             if (abs(segment_squared_norm - end_factor)
                 < abs(segment_squared_norm - start_factor))
             else (square(segment_squared_norm * Expansion(end.x, -point.x)
                          + start_factor * Expansion(start.x, -end.x))
                   + square(segment_squared_norm * Expansion(end.y, -point.y)
                            + start_factor * Expansion(start.y, -end.y))))
            / square(segment_squared_norm))


def segment_squared_distance(first_start: Point,
                             first_end: Point,
                             second_start: Point,
                             second_end: Point,
                             dot_producer: QuaternaryPointFunction[Scalar],
                             segments_relater
                             : QuaternaryPointFunction[Relation]) -> Scalar:
    return (min(point_squared_distance(first_start, first_end, second_start,
                                       dot_producer),
                point_squared_distance(first_start, first_end, second_end,
                                       dot_producer),
                point_squared_distance(second_start, second_end, first_start,
                                       dot_producer),
                point_squared_distance(second_start, second_end, first_end,
                                       dot_producer))
            if segments_relater(first_start, first_end, second_start,
                                second_end) is Relation.DISJOINT
            else 0)
