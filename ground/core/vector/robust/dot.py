from ground.core.shewchuk import (sum_expansions,
                                  to_dot_product,
                                  two_mul,
                                  two_sub_tail,
                                  two_two_sum)
from ground.hints import (Coordinate,
                          Point)
from . import bounds


def multiply(first_start: Point,
             first_end: Point,
             second_start: Point,
             second_end: Point) -> Coordinate:
    first_start_x, first_start_y = first_start.x, first_start.y
    first_end_x, first_end_y = first_end.x, first_end.y
    second_start_x, second_start_y = second_start.x, second_start.y
    second_end_x, second_end_y = second_end.x, second_end.y
    addend_x = (first_end_x - first_start_x) * (second_end_x - second_start_x)
    addend_y = (first_end_y - first_start_y) * (second_end_y - second_start_y)
    result = addend_x + addend_y
    if 0 < addend_x:
        if 0 < addend_y:
            upper_bound = addend_x + addend_y
        else:
            return result
    elif addend_x < 0:
        if addend_y < 0:
            upper_bound = -addend_x - addend_y
        else:
            return result
    else:
        return result
    error_bound = bounds.to_multiply_first_error(upper_bound)
    if result >= error_bound or -result >= error_bound:
        return result
    return _adjusted_signed_area(first_start_x, first_start_y, first_end_x,
                                 first_end_y, second_start_x, second_start_y,
                                 second_end_x, second_end_y, upper_bound)


def _adjusted_signed_area(first_start_x: Coordinate,
                          first_start_y: Coordinate,
                          first_end_x: Coordinate,
                          first_end_y: Coordinate,
                          second_start_x: Coordinate,
                          second_start_y: Coordinate,
                          second_end_x: Coordinate,
                          second_end_y: Coordinate,
                          upper_bound: Coordinate) -> Coordinate:
    first_dx_head = first_end_x - first_start_x
    second_dx_head = second_end_x - second_start_x
    first_dy_head = first_end_y - first_start_y
    second_dy_head = second_end_y - second_start_y
    addend_x_tail, addend_x_head = two_mul(first_dx_head, second_dx_head)
    addend_y_tail, addend_y_head = two_mul(first_dy_head, second_dy_head)
    result_expansion = two_two_sum(addend_x_tail, addend_x_head,
                                   addend_y_tail, addend_y_head)
    result = sum(result_expansion)
    error_bound = bounds.to_multiply_second_error(upper_bound)
    if result >= error_bound or -result >= error_bound:
        return result
    first_dx_tail = two_sub_tail(first_end_x, first_start_x, first_dx_head)
    second_dx_tail = two_sub_tail(second_end_x, second_start_x, second_dx_head)
    first_dy_tail = two_sub_tail(first_end_y, first_start_y, first_dy_head)
    second_dy_tail = two_sub_tail(second_end_y, second_start_y, second_dy_head)
    if not (first_dx_tail or second_dx_tail or second_dy_tail
            or first_dy_tail):
        return result
    error_bound = (bounds.to_multiply_third_error(upper_bound)
                   + bounds.to_determinant_error(result))
    result += ((first_dx_head * second_dx_tail
                + second_dx_head * first_dx_tail)
               + (first_dy_head * second_dy_tail
                  + second_dy_head * first_dy_tail))
    if result >= error_bound or -result >= error_bound:
        return result
    result_expansion = sum_expansions(
            result_expansion, to_dot_product(first_dx_tail, first_dy_tail,
                                             second_dx_head, second_dy_head))
    result_expansion = sum_expansions(
            result_expansion, to_dot_product(first_dx_head, first_dy_head,
                                             second_dx_tail, second_dy_tail))
    result_expansion = sum_expansions(
            result_expansion, to_dot_product(first_dx_tail, first_dy_tail,
                                             second_dx_tail, second_dy_tail))
    return result_expansion[-1]
