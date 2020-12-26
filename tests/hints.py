from typing import (Sequence,
                    Tuple,
                    TypeVar)

from hypothesis.strategies import SearchStrategy

from ground.hints import Point

Domain = TypeVar('Domain')
Range = TypeVar('Range')
Strategy = SearchStrategy
PointsPair = Tuple[Point, Point]
PointsQuadruplet = Tuple[Point, Point, Point, Point]
PointsTriplet = Tuple[Point, Point, Point]
Permutation = Sequence[int]
