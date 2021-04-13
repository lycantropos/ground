from functools import reduce

from ground.core.arithmetic import robust_divide
from ground.core.enums import Relation
from ground.core.hints import (Coordinate,
                               Expansion,
                               Point,
                               QuaternaryPointFunction)
from ground.core.shewchuk import (add_to_expansion,
                                  scale_expansion,
                                  sum_expansions,
                                  two_mul,
                                  two_one_mul,
                                  two_sub)


def point_squared_distance(start: Point,
                           end: Point,
                           point: Point,
                           dot_producer: QuaternaryPointFunction[Coordinate]
                           ) -> Coordinate:
    if end < start:
        start, end = end, start
    segment_squared_norm = dot_producer(start, end, start, end)
    end_factor_numerator = max(0, min(segment_squared_norm,
                                      dot_producer(start, point, start, end)))
    end_factor = robust_divide(end_factor_numerator, segment_squared_norm)
    start_factor_tail, start_factor_head = two_sub(1, end_factor)
    return sum_expansions(
            square_expansion(add_to_expansion(sum_expansions(
                    two_one_mul(start_factor_tail, start_factor_head, start.x),
                    two_mul(end_factor, end.x)), -point.x)),
            square_expansion(add_to_expansion(sum_expansions(
                    two_one_mul(start_factor_tail, start_factor_head, start.y),
                    two_mul(end_factor, end.y)), -point.y)))[-1]


def square_expansion(expansion: Expansion) -> Expansion:
    return reduce(sum_expansions, [scale_expansion(expansion, component)
                                   for component in expansion])


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
