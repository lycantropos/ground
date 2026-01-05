from ground.core.enums import Kind, Orientation
from ground.core.hints import Point, QuaternaryPointFunction, ScalarT
from ground.core.primitive import to_sign
from ground.core.vector.plain import cross, dot


def kind(
    vertex: Point[ScalarT],
    first_ray_point: Point[ScalarT],
    second_ray_point: Point[ScalarT],
    dot_producer: QuaternaryPointFunction[ScalarT, ScalarT] = dot.multiply,
) -> Kind:
    return Kind(
        to_sign(
            dot_producer(vertex, first_ray_point, vertex, second_ray_point)
        )
    )


def orientation(
    vertex: Point[ScalarT],
    first_ray_point: Point[ScalarT],
    second_ray_point: Point[ScalarT],
    cross_producer: QuaternaryPointFunction[ScalarT, ScalarT] = cross.multiply,
) -> Orientation:
    return Orientation(
        to_sign(
            cross_producer(vertex, first_ray_point, vertex, second_ray_point)
        )
    )
