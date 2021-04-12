from ground.core.hints import (Coordinate,
                               Point)
from ground.core.shewchuk import to_squared_points_distance


def point_squared_distance(first: Point, second: Point) -> Coordinate:
    return to_squared_points_distance(first.x, first.y, second.x, second.y)[-1]
