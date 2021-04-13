from fractions import Fraction
from typing import Callable

from ground.core.enums import Relation
from ground.core.hints import (Coordinate,
                               Point,
                               QuaternaryPointFunction)
from .point import point_squared_distance as point_point_squared_distance


def point_squared_distance(start: Point,
                           end: Point,
                           point: Point,
                           dot_producer: QuaternaryPointFunction[Coordinate],
                           inverse: Callable[[Coordinate], Coordinate]
                           = Fraction(1).__truediv__) -> Coordinate:
    end_factor = max(0, min(1,
                            dot_producer(start, point, start, end)
                            * inverse(point_point_squared_distance(start,
                                                                   end))))
    start_factor = 1 - end_factor
    return ((start_factor * start.x + end_factor * end.x - point.x) ** 2
            + (start_factor * start.y + end_factor * end.y - point.y) ** 2)


def segment_squared_distance(first_start: Point,
                             first_end: Point,
                             second_start: Point,
                             second_end: Point,
                             dot_producer: QuaternaryPointFunction[Coordinate],
                             segments_relater
                             : QuaternaryPointFunction[Relation]
                             ) -> Coordinate:
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
