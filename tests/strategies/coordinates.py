from collections.abc import Callable, Mapping
from fractions import Fraction
from typing import Any

from hypothesis import strategies

MAX_COORDINATE: int = 10**10
MIN_COORDINATE: int = -MAX_COORDINATE


rational_coordinates_strategies_factories: Mapping[
    type[Any], Callable[[int, int], Any]
] = {Fraction: strategies.fractions}
rational_coordinates_strategies = strategies.sampled_from(
    [
        factory(MIN_COORDINATE, MAX_COORDINATE)
        for factory in rational_coordinates_strategies_factories.values()
    ]
)
