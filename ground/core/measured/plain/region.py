from cfractions import Fraction

from ground.core.hints import (Contour,
                               Scalar)


def signed_area(contour: Contour[Scalar],
                *,
                _half: Fraction = Fraction(1, 2)) -> Scalar:
    vertices = contour.vertices
    result, vertex = 0, vertices[-1]
    for next_vertex in vertices:
        result += vertex.x * next_vertex.y - next_vertex.x * vertex.y
        vertex = next_vertex
    return _half * result
