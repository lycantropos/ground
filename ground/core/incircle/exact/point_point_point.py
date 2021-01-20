from fractions import Fraction

from ground.hints import (Coordinate,
                          Point)


def test(first: Point,
         second: Point,
         third: Point,
         fourth: Point) -> Coordinate:
    fourth_x, fourth_y = Fraction(fourth.x), Fraction(fourth.y)
    first_dx, first_dy = (Fraction(first.x) - fourth_x,
                          Fraction(first.y) - fourth_y)
    second_dx, second_dy = (Fraction(second.x) - fourth_x,
                            Fraction(second.y) - fourth_y)
    third_dx, third_dy = (Fraction(third.x) - fourth_x,
                          Fraction(third.y) - fourth_y)
    return ((first_dx * first_dx + first_dy * first_dy)
            * (second_dx * third_dy - second_dy * third_dx)
            - (second_dx * second_dx + second_dy * second_dy)
            * (first_dx * third_dy - first_dy * third_dx)
            + (third_dx * third_dx + third_dy * third_dy)
            * (first_dx * second_dy - first_dy * second_dx))
