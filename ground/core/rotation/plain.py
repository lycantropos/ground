from typing import (Tuple,
                    Type)

from ground.core.hints import (Point,
                               Scalar)


def rotate_point_around_origin(point: Point,
                               cosine: Scalar,
                               sine: Scalar,
                               point_cls: Type[Point]) -> Point:
    return point_cls(cosine * point.x - sine * point.y,
                     sine * point.x + cosine * point.y)


def rotate_translate_point(point: Point,
                           cosine: Scalar,
                           sine: Scalar,
                           step_x: Scalar,
                           step_y: Scalar,
                           point_cls: Type[Point]) -> Point:
    return point_cls(cosine * point.x - sine * point.y + step_x,
                     sine * point.x + cosine * point.y + step_y)


def point_to_step(point: Point,
                  cosine: Scalar,
                  sine: Scalar) -> Tuple[Scalar, Scalar]:
    return (point.x - (cosine * point.x - sine * point.y),
            point.y - (sine * point.x + cosine * point.y))
