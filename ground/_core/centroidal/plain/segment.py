from ground._core.hints import Point, ScalarFactory, ScalarT, Segment


def centroid(
    segment: Segment[ScalarT],
    coordinate_factory: ScalarFactory[ScalarT],
    point_cls: type[Point[ScalarT]],
    /,
) -> Point[ScalarT]:
    divisor = coordinate_factory(2)
    return point_cls(
        (segment.start.x + segment.end.x) / divisor,
        (segment.start.y + segment.end.y) / divisor,
    )
