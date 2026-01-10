from ground._core.hints import Point, ScalarT


def scale_point(
    point: Point[ScalarT],
    factor_x: ScalarT,
    factor_y: ScalarT,
    point_cls: type[Point[ScalarT]],
    /,
) -> Point[ScalarT]:
    return point_cls(point.x * factor_x, point.y * factor_y)
