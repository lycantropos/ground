from typing import Type

from shewchuk import Expansion

from ground.core.hints import (Point,
                               Scalar)


def translate_point(point: Point,
                    step_x: Scalar,
                    step_y: Scalar,
                    point_cls: Type[Point]) -> Point:
    return point_cls(Expansion(point.x) + step_x, Expansion(point.y) + step_y)
