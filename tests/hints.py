from typing import (Sequence,
                    Tuple,
                    TypeVar)

from hypothesis.strategies import SearchStrategy

from ground.hints import (Coordinate,
                          Point)
from ground.core.hints import QuaternaryPointFunction

Domain = TypeVar('Domain')
Strategy = SearchStrategy
CrossProducer = DotProducer = IncircleDeterminer = (
    QuaternaryPointFunction[Coordinate])
PointsPair = Tuple[Point, Point]
PointsQuadruplet = Tuple[Point, Point, Point, Point]
PointsTriplet = Tuple[Point, Point, Point]
Permutation = Sequence[int]
