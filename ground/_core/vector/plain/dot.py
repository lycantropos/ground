from ground._core.hints import Point, ScalarT


def multiply(
    first_start: Point[ScalarT],
    first_end: Point[ScalarT],
    second_start: Point[ScalarT],
    second_end: Point[ScalarT],
    /,
) -> ScalarT:
    return (first_end.x - first_start.x) * (second_end.x - second_start.x) + (
        first_end.y - first_start.y
    ) * (second_end.y - second_start.y)
