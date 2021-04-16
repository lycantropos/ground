from typing import (Callable,
                    Sequence,
                    Type)

from ground.core.hints import (Coordinate,
                               Point,
                               Segment)


def centroid(segments: Sequence[Segment],
             point_cls: Type[Point],
             sqrt: Callable[[Coordinate], Coordinate]) -> Point:
    accumulated_x = accumulated_y = accumulated_length = 0
    for segment in segments:
        start, end = segment.start, segment.end
        length = sqrt((end.x - start.x) ** 2 + (end.y - start.y) ** 2)
        accumulated_x += (start.x + end.x) * length
        accumulated_y += (start.y + end.y) * length
        accumulated_length += length
    inverted_divisor = 1 / (2 * accumulated_length)
    return point_cls(accumulated_x * inverted_divisor,
                     accumulated_y * inverted_divisor)
