from hypothesis import strategies

from ground.geometries import to_point_cls
from ground.hints import (Coordinate,
                          Point)
from tests.hints import Strategy
from .coordinates import coordinates_strategies


def coordinates_to_points(coordinates: Strategy[Coordinate]
                          ) -> Strategy[Point]:
    return strategies.builds(to_point_cls(), coordinates, coordinates)


points_strategies = coordinates_strategies.map(coordinates_to_points)
