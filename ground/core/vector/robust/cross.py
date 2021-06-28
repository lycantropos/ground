from shewchuk import vectors_cross_product

from ground.core.hints import (Point,
                               Scalar)


def multiply(first_start: Point,
             first_end: Point,
             second_start: Point,
             second_end: Point) -> Scalar:
    return vectors_cross_product(first_start.x, first_start.y, first_end.x,
                                 first_end.y, second_start.x, second_start.y,
                                 second_end.x, second_end.y)
