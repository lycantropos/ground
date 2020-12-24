from typing import Sequence

from hypothesis import strategies

from ground.base import (Orientation,
                         get_context)
from ground.hints import Coordinate
from tests.hints import Strategy
from tests.utils import (Contour,
                         Multipoint,
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


def coordinates_to_contours(coordinates: Strategy[Coordinate]
                            ) -> Strategy[Contour]:
    return (strategies.lists(coordinates_to_points(coordinates),
                             min_size=3,
                             max_size=10,
                             unique=True)
            .filter(are_points_non_collinear)
            .map(Contour))


def are_points_non_collinear(points: Sequence[Point]) -> bool:
    to_orientation = get_context().orientation
    return any(to_orientation(points[index - 2], points[index - 1],
                              points[index]) is not Orientation.COLLINEAR
               for index in range(len(points)))
