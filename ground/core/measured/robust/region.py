from fractions import Fraction

from ground.core.hints import (Contour,
                               Scalar)
from ground.core.shewchuk import (sum_expansions,
                                  to_cross_product)


def signed_area(contour: Contour[Scalar],
                *,
                _half: Fraction = Fraction(1, 2)) -> Scalar:
    vertices = contour.vertices
    result, vertex = (0,), vertices[-1]
    for next_vertex in vertices:
        result = sum_expansions(result,
                                to_cross_product(vertex.x, vertex.y,
                                                 next_vertex.x, next_vertex.y))
        vertex = next_vertex
    return _half * result[-1]
