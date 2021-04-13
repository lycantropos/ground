from fractions import Fraction

from ground.core.enums import Relation
from ground.core.hints import (Coordinate,
                               Point,
                               QuaternaryPointFunction)
from .point import point_squared_distance as point_point_squared_distance


def point_squared_distance(segment_start: Point,
                           segment_end: Point,
                           point: Point,
                           dot_producer: QuaternaryPointFunction[Coordinate]
                           ) -> Coordinate:
    end_factor = max(0, min(1,
                            dot_producer(segment_start, point, segment_start,
                                         segment_end)
                            / point_point_squared_distance(segment_start,
                                                           segment_end)))
    start_factor = 1 - end_factor
    return ((start_factor * Fraction(segment_start.x)
             + end_factor * Fraction(segment_end.x) - Fraction(point.x)) ** 2
            + (start_factor * Fraction(segment_start.y)
               + end_factor * Fraction(segment_end.y)
               - Fraction(point.y)) ** 2)


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
