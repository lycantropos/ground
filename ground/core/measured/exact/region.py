from fractions import Fraction
from typing import Sequence

from ground.core.hints import (Coordinate,
                               Point)
from ground.core.primitive import rationalize


def signed_area(vertices: Sequence[Point],
                *,
                _half: Fraction = Fraction(1, 2)) -> Coordinate:
    result, vertex = 0, vertices[-1]
    vertex_x, vertex_y = rationalize(vertex.x), rationalize(vertex.y)
    for next_vertex in vertices:
        next_vertex_x, next_vertex_y = (rationalize(next_vertex.x),
                                        rationalize(next_vertex.y))
        result += vertex_x * next_vertex_y - next_vertex_x * vertex_y
        vertex_x, vertex_y = next_vertex_x, next_vertex_y
    return _half * result
