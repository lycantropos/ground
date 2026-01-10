from ground._core.hints import Point, ScalarT


def translate_point(
    point: Point[ScalarT],
    step_x: ScalarT,
    step_y: ScalarT,
    point_cls: type[Point[ScalarT]],
    /,
) -> Point[ScalarT]:
    return point_cls(point.x + step_x, point.y + step_y)
