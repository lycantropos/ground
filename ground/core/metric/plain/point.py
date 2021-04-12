from ground.core.hints import (Coordinate,
                               Point)


def point_squared_distance(first: Point, second: Point) -> Coordinate:
    return (first.x - second.x) ** 2 + (first.y - second.y) ** 2
