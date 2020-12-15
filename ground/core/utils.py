from typing import Tuple

from ground.hints import Coordinate
from . import bounds
from .hints import Expansion


def fast_two_sum(left: Coordinate,
                 right: Coordinate) -> Tuple[Coordinate, Coordinate]:
    head = left + right
    right_virtual = head - left
    tail = right - right_virtual
    return tail, head


def two_sum(left: Coordinate,
            right: Coordinate) -> Tuple[Coordinate, Coordinate]:
    head = left + right
    right_virtual = head - left
    left_virtual = head - right_virtual
    right_tail = right - right_virtual
    left_tail = left - left_virtual
    tail = left_tail + right_tail
    return tail, head


def split(value: Coordinate,
          *,
          splitter: Coordinate = bounds.splitter
          ) -> Tuple[Coordinate, Coordinate]:
    base = splitter * value
    high = base - (base - value)
    low = value - high
    return low, high


def two_product_presplit(left: Coordinate,
                         right: Coordinate,
                         right_low: Coordinate,
                         right_high: Coordinate
                         ) -> Tuple[Coordinate, Coordinate]:
    head = left * right
    left_low, left_high = split(left)
    first_error = head - left_high * right_high
    second_error = first_error - left_low * right_high
    third_error = second_error - left_high * right_low
    tail = left_low * right_low - third_error
    return tail, head


def two_product(left: Coordinate,
                right: Coordinate) -> Tuple[Coordinate, Coordinate]:
    head = left * right
    left_low, left_high = split(left)
    right_low, right_high = split(right)
    first_error = head - left_high * right_high
    second_error = first_error - left_low * right_high
    third_error = second_error - left_high * right_low
    tail = left_low * right_low - third_error
    return tail, head


def two_two_diff(left_tail: Coordinate,
                 left_head: Coordinate,
                 right_tail: Coordinate,
                 right_head: Coordinate
                 ) -> Tuple[Coordinate, Coordinate, Coordinate, Coordinate]:
    third_tail, mid_tail, mid_head = two_one_diff(left_tail, left_head,
                                                  right_tail)
    second_tail, first_tail, head = two_one_diff(mid_tail, mid_head,
                                                 right_head)
    return third_tail, second_tail, first_tail, head


def two_two_sum(left_tail: Coordinate,
                left_head: Coordinate,
                right_tail: Coordinate,
                right_head: Coordinate
                ) -> Tuple[Coordinate, Coordinate, Coordinate, Coordinate]:
    third_tail, mid_tail, mid_head = two_one_sum(left_tail, left_head,
                                                 right_tail)
    second_tail, first_tail, head = two_one_sum(mid_tail, mid_head, right_head)
    return third_tail, second_tail, first_tail, head


def two_one_sum(left_tail: Coordinate,
                left_head: Coordinate,
                right: Coordinate
                ) -> Tuple[Coordinate, Coordinate, Coordinate]:
    second_tail, mid_head = two_sum(left_tail, right)
    first_tail, head = two_sum(left_head, mid_head)
    return second_tail, first_tail, head


def two_one_diff(left_tail: Coordinate,
                 left_head: Coordinate,
                 right: Coordinate
                 ) -> Tuple[Coordinate, Coordinate, Coordinate]:
    second_tail, mid_head = two_diff(left_tail, right)
    first_tail, head = two_sum(left_head, mid_head)
    return second_tail, first_tail, head


def two_diff(left: Coordinate,
             right: Coordinate) -> Tuple[Coordinate, Coordinate]:
    head = left - right
    return two_diff_tail(left, right, head), head


def two_diff_tail(left: Coordinate,
                  right: Coordinate,
                  head: Coordinate) -> Coordinate:
    right_virtual = left - head
    left_virtual = head + right_virtual
    right_error = right_virtual - right
    left_error = left - left_virtual
    return left_error + right_error


def square(value: Coordinate) -> Tuple[Coordinate, Coordinate]:
    head = value * value
    value_low, value_high = split(value)
    first_error = head - value_high * value_high
    second_error = first_error - (value_high + value_high) * value_low
    tail = value_low * value_low - second_error
    return tail, head


def sum_expansions(left: Expansion, right: Expansion) -> Expansion:
    """
    Sums two expansions with zero components elimination.
    """
    left_length, right_length = len(left), len(right)
    left_element, right_element = left[0], right[0]
    left_index = right_index = 0
    if (right_element > left_element) is (right_element > -left_element):
        accumulator = left_element
        left_index += 1
    else:
        accumulator = right_element
        right_index += 1
    result = []
    if (left_index < left_length) and (right_index < right_length):
        left_element, right_element = left[left_index], right[right_index]
        if (right_element > left_element) is (right_element > -left_element):
            tail, accumulator = fast_two_sum(left_element, accumulator)
            left_index += 1
        else:
            tail, accumulator = fast_two_sum(right_element, accumulator)
            right_index += 1
        if tail:
            result.append(tail)
        while (left_index < left_length) and (right_index < right_length):
            left_element, right_element = left[left_index], right[right_index]
            if ((right_element > left_element)
                    is (right_element > -left_element)):
                tail, accumulator = two_sum(accumulator, left_element)
                left_index += 1
            else:
                tail, accumulator = two_sum(accumulator, right_element)
                right_index += 1
            if tail:
                result.append(tail)
    for left_index in range(left_index, left_length):
        left_element = left[left_index]
        tail, accumulator = two_sum(accumulator, left_element)
        if tail:
            result.append(tail)
    for right_index in range(right_index, right_length):
        right_element = right[right_index]
        tail, accumulator = two_sum(accumulator, right_element)
        if tail:
            result.append(tail)
    if accumulator or not result:
        result.append(accumulator)
    return result


def scale_expansion(expansion: Expansion, scalar: Coordinate) -> Expansion:
    """
    Multiplies an expansion by a scalar with zero components elimination.
    """
    expansion = iter(expansion)
    scalar_low, scalar_high = split(scalar)
    tail, accumulator = two_product_presplit(next(expansion), scalar,
                                             scalar_low, scalar_high)
    result = []
    if tail:
        result.append(tail)
    for element in expansion:
        product_tail, product = two_product_presplit(element, scalar,
                                                     scalar_low, scalar_high)
        tail, interim = two_sum(accumulator, product_tail)
        if tail:
            result.append(tail)
        tail, accumulator = fast_two_sum(product, interim)
        if tail:
            result.append(tail)
    if accumulator or not result:
        result.append(accumulator)
    return result


def to_cross_product(minuend_multiplier_x: Coordinate,
                     minuend_multiplier_y: Coordinate,
                     subtrahend_multiplier_x: Coordinate,
                     subtrahend_multiplier_y: Coordinate) -> Expansion:
    """
    Returns expansion of vectors' planar cross product.
    """
    minuend_tail, minuend_head = two_product(minuend_multiplier_x,
                                             minuend_multiplier_y)
    subtrahend_tail, subtrahend_head = two_product(subtrahend_multiplier_y,
                                                   subtrahend_multiplier_x)
    return two_two_diff(minuend_tail, minuend_head, subtrahend_tail,
                        subtrahend_head)
