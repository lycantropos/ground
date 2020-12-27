from typing import (Sequence,
                    Tuple)

from hypothesis import strategies

from ground.base import (Context,
                         Orientation)
from ground.core.hints import TernaryPointFunction
from ground.hints import Coordinate
from tests.hints import Strategy
from tests.utils import (MAX_SEQUENCE_SIZE,
                         Contour,
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
                             max_size=MAX_SEQUENCE_SIZE,
                             unique=True)
            .map(Multipoint))


def context_with_coordinates_to_contours(
        context_with_coordinates: Tuple[Context, Strategy[Coordinate]]
) -> Strategy[Contour]:
    context, coordinates = context_with_coordinates

    def are_points_non_collinear(points: Sequence[Point],
                                 to_orientation
                                 : TernaryPointFunction[Orientation]
                                 = context.orientation) -> bool:
        return any(to_orientation(points[index - 2], points[index - 1],
                                  points[index]) is not Orientation.COLLINEAR
                   for index in range(len(points)))

    return (strategies.lists(coordinates_to_points(coordinates),
                             min_size=3,
                             max_size=MAX_SEQUENCE_SIZE,
                             unique=True)
            .filter(are_points_non_collinear)
            .map(context.points_convex_hull)
            .map(Contour))
