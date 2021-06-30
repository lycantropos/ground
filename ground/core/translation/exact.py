from typing import Type

from ground.core.hints import (Point,
                               Scalar)
from ground.core.primitive import rationalize


def translate_point(point: Point,
                    step_x: Scalar,
                    step_y: Scalar,
                    point_cls: Type[Point]) -> Point:
    return point_cls(rationalize(point.x) + rationalize(step_x),
                     rationalize(point.y) + rationalize(step_y))
