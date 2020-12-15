from enum import (IntEnum,
                  unique)
from typing import (Tuple,
                    Type)

from ground.hints import Point
from .hints import (BinaryCoordinatesOperation,
                    QuaternaryPointFunction)


@unique
class SegmentsRelationship(IntEnum):
    """
    Represents relationship between segments based on their intersection.
    """
    #: intersection is empty
    NONE = 0
    #: intersection is an endpoint of one of segments
    TOUCH = 1
    #: intersection is a point which is not an endpoint of any of segments
    CROSS = 2
    #: intersection is a segment itself
    OVERLAP = 3


def segment_contains_point(cross_producer: QuaternaryPointFunction,
                           start: Point,
                           end: Point,
                           point: Point) -> bool:
    return (point == start or point == end
            or (_bounding_box_contains(start, end, point)
                and not cross_producer(start, end, start, point)))


def segments_intersection(cross_producer: QuaternaryPointFunction,
                          divider: BinaryCoordinatesOperation,
                          point_cls: Type[Point],
                          first_start: Point,
                          first_end: Point,
                          second_start: Point,
                          second_end: Point) -> Point:
    if segment_contains_point(cross_producer, first_start, first_end,
                              second_start):
        return second_start
    elif segment_contains_point(cross_producer, first_start, first_end,
                                second_end):
        return second_end
    elif segment_contains_point(cross_producer, second_start, second_end,
                                first_start):
        return first_start
    elif segment_contains_point(cross_producer, second_start, second_end,
                                first_end):
        return first_end
    else:
        first_base_numerator = cross_producer(first_start, second_start,
                                              second_start, second_end)
        second_base_numerator = cross_producer(first_start, second_start,
                                               first_start, first_end)
        first_start_x, first_start_y = first_start.x, first_start.y
        first_end_x, first_end_y = first_end.x, first_end.y
        second_start_x, second_start_y = second_start.x, second_start.y
        second_end_x, second_end_y = second_end.x, second_end.y
        first_x_addend = (first_end_x - first_start_x) * first_base_numerator
        first_y_addend = (first_end_y - first_start_y) * first_base_numerator
        second_x_addend = ((second_end_x - second_start_x)
                           * second_base_numerator)
        second_y_addend = ((second_end_y - second_start_y)
                           * second_base_numerator)
        delta_x, delta_y = (abs(second_x_addend) - abs(first_x_addend),
                            abs(second_y_addend) - abs(first_y_addend))
        denominator_inv = divider(1, cross_producer(first_start, first_end,
                                                    second_start, second_end))
        return point_cls(
                first_start_x + first_x_addend * denominator_inv
                if 0 < delta_x
                else (second_start_x + second_x_addend * denominator_inv
                      if delta_x < 0
                      else (first_start_x + second_start_x
                            + (first_x_addend + second_x_addend)
                            * denominator_inv) / 2),
                first_start_y + first_y_addend * denominator_inv
                if 0 < delta_y
                else (second_start_y + second_y_addend * denominator_inv
                      if delta_y < 0
                      else (first_start_y + second_start_y
                            + (first_y_addend + second_y_addend)
                            * denominator_inv) / 2))


def segments_intersections(cross_producer: QuaternaryPointFunction,
                           divider: BinaryCoordinatesOperation,
                           point_cls: Type[Point],
                           first_start: Point,
                           first_end: Point,
                           second_start: Point,
                           second_end: Point) -> Tuple[Point, ...]:
    relationship = segments_relationship(cross_producer, first_start,
                                         first_end, second_start, second_end)
    if relationship is SegmentsRelationship.NONE:
        return ()
    elif relationship is SegmentsRelationship.OVERLAP:
        if first_start < first_end:
            first_start, first_end = first_end, first_start
        if second_start < second_end:
            second_start, second_end = second_end, second_start
        return (first_start
                if first_start < second_start
                else second_start,
                first_end
                if first_end < second_end
                else second_end)
    else:
        return segments_intersection(cross_producer, divider, point_cls,
                                     first_start, first_end, second_start,
                                     second_end),


def segments_relationship(cross_producer: QuaternaryPointFunction,
                          first_start: Point,
                          first_end: Point,
                          second_start: Point,
                          second_end: Point) -> SegmentsRelationship:
    if first_start > first_end:
        first_start, first_end = first_end, first_start
    if second_start > second_end:
        second_start, second_end = second_end, second_start
    starts_equal = first_start == second_start
    ends_equal = first_end == second_end
    if starts_equal and ends_equal:
        return SegmentsRelationship.OVERLAP
    first_start_cross_product = cross_producer(second_end, second_start,
                                               second_end, first_start)
    first_end_cross_product = cross_producer(second_end, second_start,
                                             second_end, first_end)
    if first_start_cross_product and first_end_cross_product:
        if (first_start_cross_product > 0) is (first_end_cross_product > 0):
            return SegmentsRelationship.NONE
        else:
            second_start_cross_product = cross_producer(first_start, first_end,
                                                        first_start,
                                                        second_start)
            second_end_cross_product = cross_producer(first_start, first_end,
                                                      first_start, second_end)
            if second_start_cross_product and second_end_cross_product:
                return (SegmentsRelationship.NONE
                        if ((second_start_cross_product > 0)
                            is (second_end_cross_product > 0))
                        else SegmentsRelationship.CROSS)
            elif second_start_cross_product:
                return (SegmentsRelationship.TOUCH
                        if first_start < second_end < first_end
                        else SegmentsRelationship.NONE)
            elif second_end_cross_product:
                return (SegmentsRelationship.TOUCH
                        if first_start < second_start < first_end
                        else SegmentsRelationship.NONE)
    elif first_start_cross_product:
        return (SegmentsRelationship.TOUCH
                if second_start <= first_end <= second_end
                else SegmentsRelationship.NONE)
    elif first_end_cross_product:
        return (SegmentsRelationship.TOUCH
                if second_start <= first_start <= second_end
                else SegmentsRelationship.NONE)
    elif starts_equal or ends_equal:
        return SegmentsRelationship.OVERLAP
    elif first_start == second_end or first_end == second_start:
        return SegmentsRelationship.TOUCH
    elif (second_start < first_start < second_end
          or first_start < second_start < first_end):
        return SegmentsRelationship.OVERLAP
    else:
        return SegmentsRelationship.NONE


def _bounding_box_contains(start: Point, end: Point, point: Point) -> bool:
    start_x, start_y = start.x, start.y
    end_x, end_y = end.x, end.y
    left_x, right_x = ((start_x, end_x)
                       if start_x < end_x
                       else (end_x, start_x))
    bottom_y, top_y = ((start_y, end_y)
                       if start_y < end_y
                       else (end_y, start_y))
    point_x, point_y = point
    return left_x <= point_x <= right_x and bottom_y <= point_y <= top_y
