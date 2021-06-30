from typing import Type

from ground.core.hints import (Point,
                               Scalar)


def translate_point(point: Point,
                    step_x: Scalar,
                    step_y: Scalar,
                    point_cls: Type[Point]) -> Point:
    return point_cls(point.x + step_x, point.y + step_y)
