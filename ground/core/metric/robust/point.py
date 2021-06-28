from ground.core.hints import (Point,
                               Scalar)
from ground.core.robust import to_squared_points_distance


def point_squared_distance(first: Point, second: Point) -> Scalar:
    return to_squared_points_distance(first.x, first.y, second.x, second.y)
