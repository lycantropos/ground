from ground._core.hints import (
    Multisegment,
    Point,
    ScalarFactory,
    ScalarT,
    SquareRooter,
)
from ground._core.primitive import square


def centroid(
    multisegment: Multisegment[ScalarT],
    coordinate_factory: ScalarFactory[ScalarT],
    point_cls: type[Point[ScalarT]],
    sqrt: SquareRooter[ScalarT],
    /,
) -> Point[ScalarT]:
    accumulated_x = accumulated_y = accumulated_length = coordinate_factory(0)
    for segment in multisegment.segments:
        start, end = segment.start, segment.end
        length = sqrt(square(end.x - start.x) + square(end.y - start.y))
        accumulated_x += (start.x + end.x) * length
        accumulated_y += (start.y + end.y) * length
        accumulated_length += length
    divisor = coordinate_factory(2) * accumulated_length
    return point_cls(accumulated_x / divisor, accumulated_y / divisor)
