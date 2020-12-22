from ground.hints import Coordinate


def determinant(first_x: Coordinate,
                first_y: Coordinate,
                second_x: Coordinate,
                second_y: Coordinate,
                third_x: Coordinate,
                third_y: Coordinate,
                fourth_x: Coordinate,
                fourth_y: Coordinate) -> Coordinate:
    """
    Calculates determinant of linear equations' system
    for checking if four points lie on the same circle.

    Positive sign of result means that point lies inside,
    negative -- outside,
    zero -- on a circle defined by other points.

    >>> determinant(0, 0, 2, 0, 2, 2, 0, 2)
    0
    >>> determinant(0, 0, 2, 0, 2, 2, 0, 3)
    -12
    >>> determinant(0, 0, 2, 0, 2, 2, 0, 1)
    4
    """
    first_dx, first_dy = first_x - fourth_x, first_y - fourth_y
    second_dx, second_dy = second_x - fourth_x, second_y - fourth_y
    third_dx, third_dy = third_x - fourth_x, third_y - fourth_y
    return ((first_dx * first_dx + first_dy * first_dy)
            * (second_dx * third_dy - second_dy * third_dx)
            - (second_dx * second_dx + second_dy * second_dy)
            * (first_dx * third_dy - first_dy * third_dx)
            + (third_dx * third_dx + third_dy * third_dy)
            * (first_dx * second_dy - first_dy * second_dx))
