from typing import Type

from shewchuk import Expansion

from ground.core.hints import (Point,
                               Scalar)


def scale_point(point: Point,
                factor_x: Scalar,
                factor_y: Scalar,
                point_cls: Type[Point]) -> Point:
    return point_cls(Expansion(point.x) * factor_x,
                     Expansion(point.y) * factor_y)
