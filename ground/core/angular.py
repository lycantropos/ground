from .enums import (Kind,
                    Orientation)
from .hints import (Point,
                    QuaternaryPointFunction,
                    Scalar)


def kind(vertex: Point,
         first_ray_point: Point,
         second_ray_point: Point,
         dot_producer: QuaternaryPointFunction[Scalar]) -> Kind:
    return Kind(to_sign(dot_producer(vertex, first_ray_point, vertex,
                                     second_ray_point)))


def orientation(vertex: Point,
                first_ray_point: Point,
                second_ray_point: Point,
                cross_producer: QuaternaryPointFunction[Scalar]
                ) -> Orientation:
    return Orientation(to_sign(cross_producer(vertex, first_ray_point, vertex,
                                              second_ray_point)))


def to_sign(value: Scalar) -> int:
    return (1 if value > 0 else -1) if value else 0
