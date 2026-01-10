from ground._core.hints import Point, ScalarT


def rotate_point_around_origin(
    point: Point[ScalarT],
    cosine: ScalarT,
    sine: ScalarT,
    point_cls: type[Point[ScalarT]],
    /,
) -> Point[ScalarT]:
    return point_cls(
        cosine * point.x - sine * point.y, sine * point.x + cosine * point.y
    )


def rotate_translate_point(
    point: Point[ScalarT],
    cosine: ScalarT,
    sine: ScalarT,
    step_x: ScalarT,
    step_y: ScalarT,
    point_cls: type[Point[ScalarT]],
    /,
) -> Point[ScalarT]:
    return point_cls(
        cosine * point.x - sine * point.y + step_x,
        sine * point.x + cosine * point.y + step_y,
    )


def point_to_step(
    point: Point[ScalarT], cosine: ScalarT, sine: ScalarT, /
) -> tuple[ScalarT, ScalarT]:
    return (
        point.x - (cosine * point.x - sine * point.y),
        point.y - (sine * point.x + cosine * point.y),
    )
