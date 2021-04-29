from ground.core.hints import (Point,
                               Scalar)
from ground.core.primitive import rationalize


def point_squared_distance(first: Point, second: Point) -> Scalar:
    return ((rationalize(first.x) - rationalize(second.x)) ** 2
            + (rationalize(first.y) - rationalize(second.y)) ** 2)
