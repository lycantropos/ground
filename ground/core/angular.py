from ground.hints import (Coordinate,
                          Point)
from .enums import (Kind,
                    Orientation)
from .hints import QuaternaryPointFunction


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
