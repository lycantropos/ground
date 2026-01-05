from collections.abc import Sequence
from typing import TypeAlias

from hypothesis.strategies import SearchStrategy

from ground.core.hints import ScalarT as ScalarT
from ground.hints import Point

Strategy = SearchStrategy

PointsPair: TypeAlias = tuple[Point[ScalarT], Point[ScalarT]]
PointsQuadruplet: TypeAlias = tuple[
    Point[ScalarT], Point[ScalarT], Point[ScalarT], Point[ScalarT]
]
PointsTriplet: TypeAlias = tuple[
    Point[ScalarT], Point[ScalarT], Point[ScalarT]
]
Permutation = Sequence[int]
