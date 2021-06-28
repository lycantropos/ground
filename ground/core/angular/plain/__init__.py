from ground.core.enums import (Kind,
                               Orientation)
from ground.core.hints import (Point,
                               QuaternaryPointFunction,
                               Scalar)
from ground.core.primitive import to_sign
from ground.core.vector.plain import (cross,
                                      dot)


def kind(vertex: Point,
         first_ray_point: Point,
         second_ray_point: Point,
         dot_producer: QuaternaryPointFunction[Scalar] = dot.multiply) -> Kind:
    return Kind(to_sign(dot_producer(vertex, first_ray_point, vertex,
                                     second_ray_point)))


def orientation(vertex: Point,
                first_ray_point: Point,
                second_ray_point: Point,
                cross_producer: QuaternaryPointFunction[Scalar]
                = cross.multiply) -> Orientation:
    return Orientation(to_sign(cross_producer(vertex, first_ray_point, vertex,
                                              second_ray_point)))
