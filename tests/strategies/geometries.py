from hypothesis import strategies

from ground.hints import Coordinate
from tests.hints import Strategy
from tests.utils import Point
from .coordinates import coordinates_strategies


def coordinates_to_points(coordinates: Strategy[Coordinate]
                          ) -> Strategy[Point]:
    return strategies.builds(Point, coordinates, coordinates)


points_strategies = coordinates_strategies.map(coordinates_to_points)
