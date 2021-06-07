from cfractions import Fraction

from ground.core.hints import (Contour,
                               Scalar)
from ground.core.primitive import rationalize


def signed_area(contour: Contour[Scalar],
                *,
                _half: Fraction = Fraction(1, 2)) -> Scalar:
    vertices = contour.vertices
    result, vertex = 0, vertices[-1]
    vertex_x, vertex_y = rationalize(vertex.x), rationalize(vertex.y)
    for next_vertex in vertices:
        next_vertex_x, next_vertex_y = (rationalize(next_vertex.x),
                                        rationalize(next_vertex.y))
        result += vertex_x * next_vertex_y - next_vertex_x * vertex_y
        vertex_x, vertex_y = next_vertex_x, next_vertex_y
    return _half * result
