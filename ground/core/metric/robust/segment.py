from fractions import Fraction
from typing import (Callable,
                    Type)

from ground.core.enums import Relation
from ground.core.hints import (Coordinate,
                               Point,
                               QuaternaryPointFunction)
from ground.core.shewchuk import (scale_expansion,
                                  sum_expansions,
                                  two_mul,
                                  two_one_mul,
                                  two_square,
                                  two_sub)


def point_squared_distance(segment_start: Point,
                           segment_end: Point,
                           point: Point,
                           dot_producer: QuaternaryPointFunction[Coordinate],
                           point_cls: Type[Point],
                           inverse: Callable[[Coordinate], Coordinate]
                           = Fraction(1).__truediv__) -> Coordinate:
    segment_squared_norm = dot_producer(segment_start, segment_end,
                                        segment_start, segment_end)
    end_factor_numerator = max(0, min(segment_squared_norm,
                                      dot_producer(segment_start, point,
                                                   segment_start,
                                                   segment_end)))
    start_factor_numerator_tail, start_factor_numerator_head = two_sub(
            segment_squared_norm, end_factor_numerator)
    dx, dy = (
        sum_expansions(sum_expansions(two_one_mul(start_factor_numerator_tail,
                                                  start_factor_numerator_head,
                                                  segment_start.x),
                                      two_mul(end_factor_numerator,
                                              segment_end.x)),
                       two_mul(point.x, -segment_squared_norm)),
        sum_expansions(sum_expansions(two_one_mul(start_factor_numerator_tail,
                                                  start_factor_numerator_head,
                                                  segment_start.y),
                                      two_mul(end_factor_numerator,
                                              segment_end.y)),
                       two_mul(point.y, -segment_squared_norm)))
    return scale_expansion(sum_expansions(two_square(sum(dx[:-1]), dx[-1]),
                                          two_square(sum(dy[:-1]), dy[-1])),
                           inverse(segment_squared_norm))[-1]


def segment_squared_distance(first_start: Point,
                             first_end: Point,
                             second_start: Point,
                             second_end: Point,
                             dot_producer: QuaternaryPointFunction[Coordinate],
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
