from numbers import Real

from ground.core.shewchuk import epsilon


def to_determinant_error(determinant: Real) -> Real:
    return (3 + 8 * epsilon) * epsilon * abs(determinant)


def to_signed_measure_first_error(upper_bound: Real) -> Real:
    return epsilon * (3 + 16 * epsilon) * upper_bound


def to_signed_measure_second_error(upper_bound: Real) -> Real:
    return epsilon * (2 + 12 * epsilon) * upper_bound


def to_signed_measure_third_error(upper_bound: Real) -> Real:
    return epsilon * epsilon * (9 + 64 * epsilon) * upper_bound
