from numbers import Real

from ground.hints import Coordinate
from . import bounds
from .utils import (sum_expansions,
                    to_cross_product,
                    two_diff_tail,
                    two_product,
                    two_two_diff)


def signed_area(first_start_x: Coordinate,
                first_start_y: Coordinate,
                first_end_x: Coordinate,
                first_end_y: Coordinate,
                second_start_x: Coordinate,
                second_start_y: Coordinate,
                second_end_x: Coordinate,
                second_end_y: Coordinate) -> Coordinate:
    """
    Calculates signed area of parallelogram built on segments' vectors.

    Positive sign of result means that second vector is counterclockwise,
    negative -- clockwise,
    zero -- collinear to first vector.

    >>> signed_area(0, 0, 1, 0, 0, 0, 1, 0)
    0
    >>> signed_area(0, 0, 1, 0, 0, 0, 0, 1)
    1
    >>> signed_area(0, 0, 1, 0, 0, 1, 0, 0)
    -1
    """
    minuend = (first_end_x - first_start_x) * (second_end_y - second_start_y)
    subtrahend = ((first_end_y - first_start_y)
                  * (second_end_x - second_start_x))
    result = minuend - subtrahend
    if minuend > 0:
        if subtrahend <= 0:
            return result
        else:
            upper_bound = minuend + subtrahend
    elif minuend < 0:
        if subtrahend >= 0:
            return result
        else:
            upper_bound = -minuend - subtrahend
    else:
        return result
    error_bound = bounds.to_signed_measure_first_error(upper_bound)
    if result >= error_bound or -result >= error_bound:
        return result
    return _adjusted_signed_area(first_start_x, first_start_y, first_end_x,
                                 first_end_y, second_start_x, second_start_y,
                                 second_end_x, second_end_y, upper_bound)


def _adjusted_signed_area(first_start_x: Real,
                          first_start_y: Real,
                          first_end_x: Real,
                          first_end_y: Real,
                          second_start_x: Real,
                          second_start_y: Real,
                          second_end_x: Real,
                          second_end_y: Real,
                          upper_bound: Real) -> Real:
    minuend_multiplier_x = first_end_x - first_start_x
    minuend_multiplier_y = second_end_y - second_start_y
    subtrahend_multiplier_x = second_end_x - second_start_x
    subtrahend_multiplier_y = first_end_y - first_start_y
    minuend_tail, minuend_head = two_product(minuend_multiplier_x,
                                             minuend_multiplier_y)
    subtrahend_tail, subtrahend_head = two_product(subtrahend_multiplier_y,
                                                   subtrahend_multiplier_x)
    result_expansion = two_two_diff(minuend_tail, minuend_head,
                                    subtrahend_tail, subtrahend_head)
    result = sum(result_expansion)
    error_bound = bounds.to_signed_measure_second_error(upper_bound)
    if result >= error_bound or -result >= error_bound:
        return result
    minuend_multiplier_x_tail = two_diff_tail(first_end_x, first_start_x,
                                              minuend_multiplier_x)
    subtrahend_multiplier_x_tail = two_diff_tail(second_end_x, second_start_x,
                                                 subtrahend_multiplier_x)
    subtrahend_multiplier_y_tail = two_diff_tail(first_end_y, first_start_y,
                                                 subtrahend_multiplier_y)
    minuend_multiplier_y_tail = two_diff_tail(second_end_y, second_start_y,
                                              minuend_multiplier_y)
    if (not minuend_multiplier_x_tail
            and not minuend_multiplier_y_tail
            and not subtrahend_multiplier_x_tail
            and not subtrahend_multiplier_y_tail):
        return result
    error_bound = (bounds.to_signed_measure_third_error(upper_bound)
                   + bounds.to_determinant_error(result))
    result += ((minuend_multiplier_x * minuend_multiplier_y_tail
                + minuend_multiplier_y * minuend_multiplier_x_tail)
               - (subtrahend_multiplier_y * subtrahend_multiplier_x_tail
                  + subtrahend_multiplier_x * subtrahend_multiplier_y_tail))
    if result >= error_bound or -result >= error_bound:
        return result
    result_expansion = sum_expansions(
            result_expansion, to_cross_product(minuend_multiplier_x_tail,
                                               minuend_multiplier_y,
                                               subtrahend_multiplier_x,
                                               subtrahend_multiplier_y_tail))
    result_expansion = sum_expansions(
            result_expansion, to_cross_product(minuend_multiplier_x,
                                               minuend_multiplier_y_tail,
                                               subtrahend_multiplier_x_tail,
                                               subtrahend_multiplier_y))
    result_expansion = sum_expansions(
            result_expansion, to_cross_product(minuend_multiplier_x_tail,
                                               minuend_multiplier_y_tail,
                                               subtrahend_multiplier_x_tail,
                                               subtrahend_multiplier_y_tail))
    return result_expansion[-1]
