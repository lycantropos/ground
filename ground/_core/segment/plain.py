from ground._core.hints import (
    Point,
    QuaternaryPointFunction,
    ScalarT,
    TernaryPointFunction,
)
from ground._core.vector.plain import cross


def intersect(
    first_start: Point[ScalarT],
    first_end: Point[ScalarT],
    second_start: Point[ScalarT],
    second_end: Point[ScalarT],
    point_cls: type[Point[ScalarT]],
    containment_checker: TernaryPointFunction[ScalarT, bool],
    /,
    *,
    cross_product: QuaternaryPointFunction[ScalarT, ScalarT] = cross.multiply,
) -> Point[ScalarT]:
    if containment_checker(first_start, first_end, second_start):
        return second_start
    if containment_checker(first_start, first_end, second_end):
        return second_end
    if containment_checker(second_start, second_end, first_start):
        return first_start
    if containment_checker(second_start, second_end, first_end):
        return first_end
    scale = cross_product(
        first_start, second_start, second_start, second_end
    ) / cross_product(first_start, first_end, second_start, second_end)
    return point_cls(
        first_start.x + (first_end.x - first_start.x) * scale,
        first_start.y + (first_end.y - first_start.y) * scale,
    )
