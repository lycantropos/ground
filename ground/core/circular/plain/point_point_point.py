from ground.core.enums import Location
from ground.core.hints import Point
from ground.core.primitive import to_sign


def test(point: Point, first: Point, second: Point, third: Point) -> Location:
    first_dx, first_dy = first.x - point.x, first.y - point.y
    second_dx, second_dy = second.x - point.x, second.y - point.y
    third_dx, third_dy = third.x - point.x, third.y - point.y
    return Location(1
                    + to_sign((first_dx * first_dx + first_dy * first_dy)
                              * (second_dx * third_dy - second_dy * third_dx)
                              - (second_dx * second_dx + second_dy * second_dy)
                              * (first_dx * third_dy - first_dy * third_dx)
                              + (third_dx * third_dx + third_dy * third_dy)
                              * (first_dx * second_dy - first_dy * second_dx)))
