from fractions import Fraction

from ground.core.hints import (Contour,
                               Coordinate)


def signed_area(contour: Contour[Coordinate],
                *,
                _half: Fraction = Fraction(1, 2)) -> Coordinate:
    vertices = contour.vertices
    result, vertex = 0, vertices[-1]
    for next_vertex in vertices:
        result += vertex.x * next_vertex.y - next_vertex.x * vertex.y
        vertex = next_vertex
    return _half * result
