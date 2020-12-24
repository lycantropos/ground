from ground.hints import (Coordinate,
                          Point)


def test(first: Point,
         second: Point,
         third: Point,
         fourth: Point) -> Coordinate:
    first_dx, first_dy = first.x - fourth.x, first.y - fourth.y
    second_dx, second_dy = second.x - fourth.x, second.y - fourth.y
    third_dx, third_dy = third.x - fourth.x, third.y - fourth.y
    return ((first_dx * first_dx + first_dy * first_dy)
            * (second_dx * third_dy - second_dy * third_dx)
            - (second_dx * second_dx + second_dy * second_dy)
            * (first_dx * third_dy - first_dy * third_dx)
            + (third_dx * third_dx + third_dy * third_dy)
            * (first_dx * second_dy - first_dy * second_dx))
