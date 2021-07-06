from ground.core.enums import Location
from ground.core.hints import (Point,
                               Scalar)
from ground.core.primitive import (rationalize,
                                   to_sign)


def test(point: Point,
         first: Point,
         second: Point,
         third: Point) -> Scalar:
    point_x, point_y = rationalize(point.x), rationalize(point.y)
    first_dx, first_dy = (rationalize(first.x) - point_x,
                          rationalize(first.y) - point_y)
    second_dx, second_dy = (rationalize(second.x) - point_x,
                            rationalize(second.y) - point_y)
    third_dx, third_dy = (rationalize(third.x) - point_x,
                          rationalize(third.y) - point_y)
    return Location(1
                    + to_sign((first_dx * first_dx + first_dy * first_dy)
                              * (second_dx * third_dy - second_dy * third_dx)
                              - (second_dx * second_dx + second_dy * second_dy)
                              * (first_dx * third_dy - first_dy * third_dx)
                              + (third_dx * third_dx + third_dy * third_dy)
                              * (first_dx * second_dy - first_dy * second_dx)))
