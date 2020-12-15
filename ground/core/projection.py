from ground.hints import Coordinate
from .parallelogram import signed_area


def signed_length(first_start_x: Coordinate,
                  first_start_y: Coordinate,
                  first_end_x: Coordinate,
                  first_end_y: Coordinate,
                  second_start_x: Coordinate,
                  second_start_y: Coordinate,
                  second_end_x: Coordinate,
                  second_end_y: Coordinate) -> Coordinate:
    """
    Calculates signed length of projection of one vector onto another.

    Positive sign of result means that angle between vectors is acute,
    negative -- obtuse,
    zero -- right.

    >>> signed_length(0, 0, 1, 0, 0, 0, 1, 0)
    1
    >>> signed_length(0, 0, 1, 0, 0, 0, 0, 1)
    0
    >>> signed_length(0, 0, 1, 0, 1, 0, 0, 0)
    -1
    """
    return signed_area(first_start_x, first_start_y, first_end_x, first_end_y,
                       -second_start_y, second_start_x, -second_end_y,
                       second_end_x)
