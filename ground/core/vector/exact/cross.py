from ground.core.hints import (Point,
                               Scalar)
from ground.core.primitive import rationalize


def multiply(first_start: Point,
             first_end: Point,
             second_start: Point,
             second_end: Point) -> Scalar:
    return ((rationalize(first_end.x) - rationalize(first_start.x))
            * (rationalize(second_end.y) - rationalize(second_start.y))
            - (rationalize(first_end.y) - rationalize(first_start.y))
            * (rationalize(second_end.x) - rationalize(second_start.x)))
