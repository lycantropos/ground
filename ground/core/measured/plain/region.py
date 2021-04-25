from fractions import Fraction
from typing import Sequence

from ground.core.hints import (Coordinate,
                               Point)


def signed_area(vertices: Sequence[Point],
                *,
                _half: Fraction = Fraction(1, 2)) -> Coordinate:
    result, vertex = 0, vertices[-1]
    for next_vertex in vertices:
        result += vertex.x * next_vertex.y - next_vertex.x * vertex.y
        vertex = next_vertex
    return _half * result
