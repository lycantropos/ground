from numbers import Real

from ground.core.shewchuk import epsilon


def to_point_point_point_determinant_error(determinant: Real) -> Real:
    return (3 + 8 * epsilon) * epsilon * abs(determinant)


def to_point_point_point_first_error(upper_bound: Real) -> Real:
    return (10 + 96 * epsilon) * epsilon * upper_bound


def to_point_point_point_second_error(upper_bound: Real) -> Real:
    return epsilon * (4 + 48 * epsilon) * upper_bound


def to_point_point_point_third_error(upper_bound: Real) -> Real:
    return epsilon * epsilon * (44 + 576 * epsilon) * upper_bound
