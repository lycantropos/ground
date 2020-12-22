from numbers import Real
from typing import Tuple


def _to_epsilon_and_splitter() -> Tuple[Real, Real]:
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


def to_determinant_error(determinant: Real) -> Real:
    return (3 + 8 * epsilon) * epsilon * abs(determinant)


def to_signed_measure_first_error(upper_bound: Real) -> Real:
    return epsilon * (3 + 16 * epsilon) * upper_bound


def to_signed_measure_second_error(upper_bound: Real) -> Real:
    return epsilon * (2 + 12 * epsilon) * upper_bound


def to_signed_measure_third_error(upper_bound: Real) -> Real:
    return epsilon * epsilon * (9 + 64 * epsilon) * upper_bound


def to_cocircular_first_error(upper_bound: Real) -> Real:
    return (10 + 96 * epsilon) * epsilon * upper_bound


def to_cocircular_second_error(upper_bound: Real) -> Real:
    return epsilon * (4 + 48 * epsilon) * upper_bound


def to_cocircular_third_error(upper_bound: Real) -> Real:
    return epsilon * epsilon * (44 + 576 * epsilon) * upper_bound
