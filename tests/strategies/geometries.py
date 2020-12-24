from hypothesis import strategies

from ground.base import get_context
from ground.hints import (Coordinate,
                          Point)
from tests.hints import Strategy
from .coordinates import (coordinates_strategies,
                          rational_coordinates_strategies)


def coordinates_to_points(coordinates: Strategy[Coordinate]
                          ) -> Strategy[Point]:
    return strategies.builds(get_context().point_cls, coordinates, coordinates)


points_strategies = coordinates_strategies.map(coordinates_to_points)
rational_points_strategies = (rational_coordinates_strategies
                              .map(coordinates_to_points))
