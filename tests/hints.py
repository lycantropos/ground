from typing import (Sequence,
                    Tuple)

from hypothesis.strategies import SearchStrategy

from ground.hints import Point

Strategy = SearchStrategy
PointsPair = Tuple[Point, Point]
PointsQuadruplet = Tuple[Point, Point, Point, Point]
PointsTriplet = Tuple[Point, Point, Point]
Permutation = Sequence[int]
