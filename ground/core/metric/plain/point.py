from ground.core.hints import Point, ScalarT
from ground.core.primitive import square


def point_squared_distance(
    first: Point[ScalarT], second: Point[ScalarT]
) -> ScalarT:
    return square(first.x - second.x) + square(first.y - second.y)
