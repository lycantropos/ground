from hypothesis import strategies

from ground.hints import Coordinate
from tests.hints import Strategy
from tests.utils import (Multipoint,
                         Point)
from .coordinates import coordinates_strategies


def coordinates_to_points(coordinates: Strategy[Coordinate]
                          ) -> Strategy[Point]:
    return strategies.builds(Point, coordinates, coordinates)


points_strategies = coordinates_strategies.map(coordinates_to_points)


def coordinates_to_multipoints(coordinates: Strategy[Coordinate]
                               ) -> Strategy[Multipoint]:
    return (strategies.lists(coordinates_to_points(coordinates),
                             min_size=1,
                             max_size=10,
                             unique=True)
            .map(Multipoint))
