from ground._core.hints import Multipoint, Point, ScalarFactory, ScalarT


def centroid(
    multipoint: Multipoint[ScalarT],
    coordinate_factory: ScalarFactory[ScalarT],
    point_cls: type[Point[ScalarT]],
    /,
) -> Point[ScalarT]:
    result_x = result_y = coordinate_factory(0)
    for point in multipoint.points:
        result_x += point.x
        result_y += point.y
    divisor = coordinate_factory(len(multipoint.points))
    return point_cls(result_x / divisor, result_y / divisor)
