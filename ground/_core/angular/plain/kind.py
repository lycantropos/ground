from ground._core.enums import Kind
from ground._core.hints import Point, QuaternaryPointFunction, ScalarT
from ground._core.primitive import to_sign


def kind(
    vertex: Point[ScalarT],
    first_ray_point: Point[ScalarT],
    second_ray_point: Point[ScalarT],
    dot_product: QuaternaryPointFunction[ScalarT, ScalarT],
    zero: ScalarT,
    /,
) -> Kind:
    return Kind(
        to_sign(
            dot_product(vertex, first_ray_point, vertex, second_ray_point),
            zero,
        )
    )
