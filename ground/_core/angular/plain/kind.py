from ground._core.enums import Kind
from ground._core.hints import Point, QuaternaryPointFunction, ScalarT
from ground._core.primitive import to_sign
from ground._core.vector.plain import dot


def kind(
    vertex: Point[ScalarT],
    first_ray_point: Point[ScalarT],
    second_ray_point: Point[ScalarT],
    zero: ScalarT,
    /,
    *,
    dot_producer: QuaternaryPointFunction[ScalarT, ScalarT] = dot.multiply,
) -> Kind:
    return Kind(
        to_sign(
            dot_producer(vertex, first_ray_point, vertex, second_ray_point),
            zero,
        )
    )
