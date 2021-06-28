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
    end_factor_numerator = max(0, min(segment_squared_norm,
                                      dot_producer(start, point, start, end)))
    start_factor_numerator = Expansion(segment_squared_norm,
                                       -end_factor_numerator)
    return ((square(start_factor_numerator * start.x
                    + end_factor_numerator * end.x
                    - segment_squared_norm * point.x)
             + square(start_factor_numerator * start.y
                      + end_factor_numerator * end.y
                      - segment_squared_norm * point.y))
            / square(segment_squared_norm))


def segment_squared_distance(first_start: Point,
                             first_end: Point,
                             second_start: Point,
                             second_end: Point,
                             dot_producer: QuaternaryPointFunction[Scalar],
                             segments_relater
                             : QuaternaryPointFunction[Relation]
                             ) -> Scalar:
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
