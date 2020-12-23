from ground.hints import (Coordinate,
                          Point)


def multiply(first_start: Point,
             first_end: Point,
             second_start: Point,
             second_end: Point) -> Coordinate:
    return ((first_end.x - first_start.x) * (second_end.y - second_start.y)
            - (first_end.y - first_start.y) * (second_end.x - second_start.x))
