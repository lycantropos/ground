from ground.hints import Coordinate


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
    return ((first_end_x - first_start_x) * (second_end_y - second_start_y)
            - (first_end_y - first_start_y) * (second_end_x - second_start_x))
