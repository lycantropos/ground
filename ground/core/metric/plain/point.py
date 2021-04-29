from ground.core.hints import (Point,
                               Scalar)


def point_squared_distance(first: Point, second: Point) -> Scalar:
    return (first.x - second.x) ** 2 + (first.y - second.y) ** 2
