from ground.hints import Point
from .enums import (Kind,
                    Orientation)
from .hints import QuaternaryPointFunction
from .utils import to_sign


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
