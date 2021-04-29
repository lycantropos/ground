from typing import (Callable,
                    Type)

from ground.core.hints import (Multisegment,
                               Point,
                               Scalar)
from ground.core.primitive import rationalize


def centroid(multisegment: Multisegment,
             point_cls: Type[Point],
             sqrt: Callable[[Scalar], Scalar]) -> Point:
    accumulated_x = accumulated_y = accumulated_length = 0
    for segment in multisegment.segments:
        start, end = segment.start, segment.end
        start_x, start_y = rationalize(start.x), rationalize(start.y)
        end_x, end_y = rationalize(end.x), rationalize(end.y)
        length = sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2)
        accumulated_x += (start_x + end_x) * length
        accumulated_y += (start_y + end_y) * length
        accumulated_length += length
    inverted_divisor = 1 / (2 * accumulated_length)
    return point_cls(accumulated_x * inverted_divisor,
                     accumulated_y * inverted_divisor)
