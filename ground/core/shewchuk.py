from typing import Tuple

from ground.hints import Coordinate
from .hints import Expansion


def _to_epsilon_and_splitter() -> Tuple[Coordinate, int]:
    every_other = True
    epsilon, splitter = 1., 1
    check = 1.
    while True:
        last_check = check
        epsilon /= 2.
        if every_other:
            splitter *= 2
        every_other = not every_other
        check = 1. + epsilon
        if check == 1. or check == last_check:
            break
    splitter += 1
    return epsilon, splitter


epsilon, splitter = _to_epsilon_and_splitter()


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
          _splitter: Coordinate = splitter) -> Tuple[Coordinate, Coordinate]:
    base = _splitter * value
    high = base - (base - value)
    low = value - high
    return low, high


def two_mul(left: Coordinate,
            right: Coordinate) -> Tuple[Coordinate, Coordinate]:
    head = left * right
    left_low, left_high = split(left)
    right_low, right_high = split(right)
    first_error = head - left_high * right_high
    second_error = first_error - left_low * right_high
    third_error = second_error - left_high * right_low
    tail = left_low * right_low - third_error
    return tail, head


def two_mul_presplit(left: Coordinate,
                     right: Coordinate,
                     right_low: Coordinate,
                     right_high: Coordinate) -> Tuple[Coordinate, Coordinate]:
    head = left * right
    left_low, left_high = split(left)
    first_error = head - left_high * right_high
    second_error = first_error - left_low * right_high
    third_error = second_error - left_high * right_low
    tail = left_low * right_low - third_error
    return tail, head


def two_two_sub(left_tail: Coordinate,
                left_head: Coordinate,
                right_tail: Coordinate,
                right_head: Coordinate
                ) -> Tuple[Coordinate, Coordinate, Coordinate, Coordinate]:
    third_tail, mid_tail, mid_head = two_one_sub(left_tail, left_head,
                                                 right_tail)
    second_tail, first_tail, head = two_one_sub(mid_tail, mid_head, right_head)
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


def two_one_sub(left_tail: Coordinate,
                left_head: Coordinate,
                right: Coordinate
                ) -> Tuple[Coordinate, Coordinate, Coordinate]:
    second_tail, mid_head = two_sub(left_tail, right)
    first_tail, head = two_sum(left_head, mid_head)
    return second_tail, first_tail, head


def two_one_mul(left_tail: Coordinate,
                left_head: Coordinate,
                right: Coordinate
                ) -> Tuple[Coordinate, Coordinate, Coordinate, Coordinate]:
    right_low, right_high = split(right)
    head_tail, head = two_mul_presplit(left_head, right, right_low, right_high)
    tail_tail, tail_head = two_mul_presplit(left_tail, right, right_low,
                                            right_high)
    mid_tail, first_tail = two_sum(head_tail, tail_head)
    third_tail, second_tail = fast_two_sum(tail_tail, mid_tail)
    return third_tail, second_tail, first_tail, head


def two_sub(left: Coordinate,
            right: Coordinate) -> Tuple[Coordinate, Coordinate]:
    head = left - right
    return two_sub_tail(left, right, head), head


def two_sub_tail(left: Coordinate,
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


def add_to_expansion(expansion: Expansion, value: Coordinate) -> Expansion:
    """
    Adds given value to the expansion with zero components elimination.
    """
    result = []
    accumulator = value
    for index, component in enumerate(expansion):
        tail, accumulator = two_sum(accumulator, component)
        if tail:
            result.append(tail)
    if accumulator or not result:
        result.append(accumulator)
    return result


def sum_expansions(left: Expansion, right: Expansion) -> Expansion:
    """
    Sums two expansions with zero components elimination.
    """
    left_length, right_length = len(left), len(right)
    left_component, right_component = left[0], right[0]
    left_index = right_index = 0
    if ((right_component > left_component)
            is (right_component > -left_component)):
        accumulator = left_component
        left_index += 1
    else:
        accumulator = right_component
        right_index += 1
    result = []
    if (left_index < left_length) and (right_index < right_length):
        left_component, right_component = left[left_index], right[right_index]
        if ((right_component > left_component)
                is (right_component > -left_component)):
            tail, accumulator = fast_two_sum(left_component, accumulator)
            left_index += 1
        else:
            tail, accumulator = fast_two_sum(right_component, accumulator)
            right_index += 1
        if tail:
            result.append(tail)
        while (left_index < left_length) and (right_index < right_length):
            left_component, right_component = (left[left_index],
                                               right[right_index])
            if ((right_component > left_component)
                    is (right_component > -left_component)):
                tail, accumulator = two_sum(accumulator, left_component)
                left_index += 1
            else:
                tail, accumulator = two_sum(accumulator, right_component)
                right_index += 1
            if tail:
                result.append(tail)
    for left_index in range(left_index, left_length):
        left_component = left[left_index]
        tail, accumulator = two_sum(accumulator, left_component)
        if tail:
            result.append(tail)
    for right_index in range(right_index, right_length):
        right_component = right[right_index]
        tail, accumulator = two_sum(accumulator, right_component)
        if tail:
            result.append(tail)
    if accumulator or not result:
        result.append(accumulator)
    return result


def scale_expansion(expansion: Expansion, scalar: Coordinate) -> Expansion:
    """
    Multiplies the expansion by given scalar with zero components elimination.
    """
    components = iter(expansion)
    scalar_low, scalar_high = split(scalar)
    tail, accumulator = two_mul_presplit(next(components), scalar, scalar_low,
                                         scalar_high)
    result = []
    if tail:
        result.append(tail)
    for component in components:
        product_tail, product = two_mul_presplit(component, scalar, scalar_low,
                                                 scalar_high)
        tail, interim = two_sum(accumulator, product_tail)
        if tail:
            result.append(tail)
        tail, accumulator = fast_two_sum(product, interim)
        if tail:
            result.append(tail)
    if accumulator or not result:
        result.append(accumulator)
    return result


def to_cross_product(first_x: Coordinate,
                     first_y: Coordinate,
                     second_x: Coordinate,
                     second_y: Coordinate) -> Expansion:
    """
    Returns expansion of vectors' cross product.
    """
    minuend_tail, minuend_head = two_mul(first_x, second_y)
    subtrahend_tail, subtrahend_head = two_mul(second_x, first_y)
    return two_two_sub(minuend_tail, minuend_head, subtrahend_tail,
                       subtrahend_head)


def to_dot_product(first_x: Coordinate, first_y: Coordinate,
                   second_x: Coordinate, second_y: Coordinate) -> Expansion:
    """
    Returns expansion of vectors' dot product.
    """
    x_tail, x_head = two_mul(first_x, second_x)
    y_tail, y_head = two_mul(first_y, second_y)
    return two_two_sum(x_tail, x_head, y_tail, y_head)
