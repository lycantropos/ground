from ground.core.hints import (Coordinate,
                               Point)
from ground.core.primitive import rationalize


def test(first: Point,
         second: Point,
         third: Point,
         fourth: Point) -> Coordinate:
    fourth_x, fourth_y = rationalize(fourth.x), rationalize(fourth.y)
    first_dx, first_dy = (rationalize(first.x) - fourth_x,
                          rationalize(first.y) - fourth_y)
    second_dx, second_dy = (rationalize(second.x) - fourth_x,
                            rationalize(second.y) - fourth_y)
    third_dx, third_dy = (rationalize(third.x) - fourth_x,
                          rationalize(third.y) - fourth_y)
    return ((first_dx * first_dx + first_dy * first_dy)
            * (second_dx * third_dy - second_dy * third_dx)
            - (second_dx * second_dx + second_dy * second_dy)
            * (first_dx * third_dy - first_dy * third_dx)
            + (third_dx * third_dx + third_dy * third_dy)
            * (first_dx * second_dy - first_dy * second_dx))
