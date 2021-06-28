from shewchuk import (kind as raw_kind,
                      orientation as raw_orientation)

from ground.core.enums import (Kind,
                               Orientation)
from ground.core.hints import Point


def kind(vertex: Point,
         first_ray_point: Point,
         second_ray_point: Point) -> Kind:
    return Kind(raw_kind(vertex.x, vertex.y, first_ray_point.x,
                         first_ray_point.y, second_ray_point.x,
                         second_ray_point.y))


def orientation(vertex: Point,
                first_ray_point: Point,
                second_ray_point: Point) -> Orientation:
    return Orientation(raw_orientation(vertex.x, vertex.y, first_ray_point.x,
                                       first_ray_point.y, second_ray_point.x,
                                       second_ray_point.y))
