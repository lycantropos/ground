from operator import add
from typing import (Sequence,
                    Tuple)

from hypothesis import strategies

from ground.base import (Context,
                         Orientation)
from ground.hints import (Contour,
                          Coordinate,
                          Point)
from tests.hints import (PointsPair,
                         PointsQuadruplet,
                         Strategy)
from tests.utils import (MAX_SEQUENCE_SIZE,
                         Box,
                         Point,
                         pack,
                         to_pairs)
from .coordinates import coordinates_strategies


def coordinates_to_boxes(coordinates: Strategy[Coordinate]
                         ) -> Strategy[Box]:
    return (to_pairs(strategies.lists(coordinates,
                                      unique=True,
                                      min_size=2,
                                      max_size=2)
                     .map(sorted))
            .map(pack(add))
            .map(pack(Box)))


def coordinates_to_points(coordinates: Strategy[Coordinate]
                          ) -> Strategy[Point]:
    return strategies.builds(Point, coordinates, coordinates)


points_strategies = coordinates_strategies.map(coordinates_to_points)


def points_to_segments_endpoints(points: Strategy[Point]
                                 ) -> Strategy[PointsPair]:
    return (strategies.lists(points,
                             min_size=2,
                             max_size=2,
                             unique=True)
            .map(tuple))


def coordinates_to_points_sequences(coordinates: Strategy[Coordinate]
                                    ) -> Strategy[Sequence[Point]]:
    return strategies.lists(coordinates_to_points(coordinates),
                            min_size=1,
                            max_size=MAX_SEQUENCE_SIZE,
                            unique=True)


def to_contexts_with_vertices_sequences(
        contexts_with_coordinates: Tuple[Strategy[Context],
                                         Strategy[Coordinate]]
) -> Strategy[Tuple[Context, Sequence[Point]]]:
    contexts, coordinates = contexts_with_coordinates

    def are_points_non_collinear(context_with_points_list
                                 : Tuple[Context, Sequence[Point]]) -> bool:
        context, points_list = context_with_points_list
        return any(context.angle_orientation(points_list[index - 2],
                                             points_list[index - 1],
                                             points_list[index])
                   is not Orientation.COLLINEAR
                   for index in range(len(points_list)))

    def to_context_with_points_convex_hull(context_with_points_list
                                           : Tuple[Context, Sequence[Point]]
                                           ) -> Tuple[Context,
                                                      Sequence[Point]]:
        context, points_list = context_with_points_list
        return context, context.points_convex_hull(points_list)

    return (strategies.tuples(
            contexts,
            strategies.lists(coordinates_to_points(coordinates),
                             min_size=3,
                             max_size=MAX_SEQUENCE_SIZE,
                             unique=True))
            .filter(are_points_non_collinear)
            .map(to_context_with_points_convex_hull))


def to_contexts_with_borders_and_holes_sequences(
        contexts_with_coordinates: Tuple[Strategy[Context],
                                         Strategy[Coordinate]]
) -> Strategy[Tuple[Context, Contour, Sequence[Contour]]]:
    def to_context_with_border_and_holes(context_with_vertices
                                         : Tuple[Context, Sequence[Point]]
                                         ) -> Tuple[Context, Contour,
                                                    Sequence[Contour]]:
        context, vertices = context_with_vertices
        return context, context.contour_cls(vertices), []

    return (to_contexts_with_vertices_sequences(contexts_with_coordinates)
            .map(to_context_with_border_and_holes))


def to_contexts_with_segments_endpoints_and_points(
        contexts_with_points: Tuple[Strategy[Context], Strategy[Point]]
) -> Strategy[Tuple[Context, PointsPair, Point]]:
    contexts, points = contexts_with_points
    return strategies.tuples(contexts, points_to_segments_endpoints(points),
                             points)


def to_contexts_with_segments_pairs_endpoints(
        contexts_with_points: Tuple[Strategy[Context], Strategy[Point]]
) -> Strategy[Tuple[Context, PointsQuadruplet]]:
    contexts, points = contexts_with_points
    return strategies.tuples(contexts,
                             to_pairs(points_to_segments_endpoints(points))
                             .map(pack(add)))
