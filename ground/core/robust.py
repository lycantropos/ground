from shewchuk import Expansion

from .hints import Scalar
from .primitive import square


def to_cross_product(first_x: Scalar,
                     first_y: Scalar,
                     second_x: Scalar,
                     second_y: Scalar) -> Expansion:
    """
    Returns expansion of vectors' cross product.
    """
    return Expansion(first_x) * second_y - Expansion(second_x) * first_y


def to_squared_points_distance(first_x: Scalar,
                               first_y: Scalar,
                               second_x: Scalar,
                               second_y: Scalar) -> Expansion:
    return (square(Expansion(first_x, -second_x))
            + square(Expansion(first_y, -second_y)))
