from fractions import Fraction
from typing import Sequence

from ground.core.hints import (Coordinate,
                               Point)
from ground.core.shewchuk import (sum_expansions,
                                  to_cross_product)


def signed_area(vertices: Sequence[Point],
                *,
                _half: Fraction = Fraction(1, 2)) -> Coordinate:
    result, vertex = (0,), vertices[-1]
    for next_vertex in vertices:
        result = sum_expansions(result,
                                to_cross_product(vertex.x, vertex.y,
                                                 next_vertex.x, next_vertex.y))
        vertex = next_vertex
    return _half * result[-1]
