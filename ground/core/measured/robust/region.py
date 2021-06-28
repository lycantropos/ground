from cfractions import Fraction
from shewchuk import Expansion

from ground.core.hints import (Contour,
                               Scalar)
from ground.core.robust import to_cross_product


def signed_area(contour: Contour[Scalar],
                *,
                _half: Fraction = Fraction(1, 2)) -> Scalar:
    vertices = contour.vertices
    result, vertex = Expansion(), vertices[-1]
    for next_vertex in vertices:
        result = result + to_cross_product(vertex.x, vertex.y, next_vertex.x,
                                           next_vertex.y)
        vertex = next_vertex
    return result * _half
