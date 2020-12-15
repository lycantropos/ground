from enum import (IntEnum,
                  unique)

from ground.hints import (Coordinate,
                          Point)
from .hints import QuaternaryPointFunction


@unique
class Kind(IntEnum):
    """
    Represents kinds of angles
    based on their degrees value in range ``[0, 180]``.
    """
    #: ``(90, 180]`` degrees
    OBTUSE = -1
    #: ``90`` degrees
    RIGHT = 0
    #: ``[0, 90)`` degrees
    ACUTE = 1


@unique
class Orientation(IntEnum):
    """
    Represents kinds of angle orientations.
    """
    #: in the same direction as a clock's hands
    CLOCKWISE = -1
    #: to the top and then to the bottom or vice versa
    COLLINEAR = 0
    #: opposite to clockwise
    COUNTERCLOCKWISE = 1


def kind(dot_producer: QuaternaryPointFunction,
         vertex: Point,
         first_ray_point: Point,
         second_ray_point: Point) -> Kind:
    return Kind(to_sign(dot_producer(vertex, first_ray_point, vertex,
                                     second_ray_point)))


def orientation(cross_producer: QuaternaryPointFunction,
                vertex: Point,
                first_ray_point: Point,
                second_ray_point: Point) -> Orientation:
    return Orientation(to_sign(cross_producer(vertex, first_ray_point, vertex,
                                              second_ray_point)))


def to_sign(value: Coordinate) -> int:
    return (1 if value > 0 else -1) if value else 0
