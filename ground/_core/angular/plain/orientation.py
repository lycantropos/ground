from ground._core.enums import Orientation
from ground._core.hints import Point, QuaternaryPointFunction, ScalarT
from ground._core.primitive import to_sign
from ground._core.vector.plain import cross


def orientation(
    vertex: Point[ScalarT],
    first_ray_point: Point[ScalarT],
    second_ray_point: Point[ScalarT],
    zero: ScalarT,
    /,
    *,
    cross_producer: QuaternaryPointFunction[ScalarT, ScalarT] = cross.multiply,
) -> Orientation:
    return Orientation(
        to_sign(
            cross_producer(vertex, first_ray_point, vertex, second_ray_point),
            zero,
        )
    )
