from typing import (Sequence,
                    Tuple)

from hypothesis import strategies

from ground.base import (Context,
                         Orientation)
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


def contexts_with_coordinates_to_contexts_with_contours(
        contexts_with_coordinates: Tuple[Strategy[Context],
                                         Strategy[Coordinate]]
) -> Strategy[Tuple[Context, Contour]]:
    contexts, coordinates = contexts_with_coordinates

    def are_points_non_collinear(context_with_points_list
                                 : Tuple[Context, Sequence[Point]]) -> bool:
        context, points_list = context_with_points_list
        return any(context.orientation(points_list[index - 2],
                                       points_list[index - 1],
                                       points_list[index])
                   is not Orientation.COLLINEAR
                   for index in range(len(points_list)))

    def to_context_with_points_convex_hull(context_with_points_list
                                           : Tuple[Context, Sequence[Point]]
                                           ) -> Tuple[Context,
                                                      Sequence[Point]]:
        context, points_list = context_with_points_list
        return context, Contour(context.points_convex_hull(points_list))

    return (strategies.tuples(
            contexts,
            strategies.lists(coordinates_to_points(coordinates),
                             min_size=3,
                             max_size=MAX_SEQUENCE_SIZE,
                             unique=True))
            .filter(are_points_non_collinear)
            .map(to_context_with_points_convex_hull))
