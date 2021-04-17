from operator import add
from typing import (Sequence,
                    Tuple)

from hypothesis import strategies

from ground.base import (Context,
                         Orientation)
from ground.hints import (Box,
                          Contour,
                          Coordinate,
                          Point,
                          Polygon,
                          Segment)
from tests.hints import (PointsPair,
                         PointsQuadruplet,
                         Strategy)
from tests.utils import (MAX_SEQUENCE_SIZE,
                         Box,
                         Point,
                         pack,
                         sub_lists,
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


def to_contexts_with_convex_hulls(
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


to_contexts_with_vertices_sequences = to_contexts_with_convex_hulls


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


def to_contexts_with_boxes_and_points(
        contexts_with_coordinates
        : Tuple[Strategy[Context], Strategy[Coordinate]]
) -> Strategy[Tuple[Context, Box, Point]]:
    contexts, coordinates = contexts_with_coordinates
    return strategies.tuples(contexts, coordinates_to_boxes(coordinates),
                             coordinates_to_points(coordinates))


def to_contexts_with_boxes_and_segments_endpoints(
        contexts_with_coordinates
        : Tuple[Strategy[Context], Strategy[Coordinate]]
) -> Strategy[Tuple[Context, Box, PointsPair]]:
    contexts, coordinates = contexts_with_coordinates
    points = coordinates_to_points(coordinates)
    return strategies.tuples(contexts, coordinates_to_boxes(coordinates),
                             points_to_segments_endpoints(points))


def to_contexts_with_polygons_sequences(
        contexts_with_coordinates: Tuple[Strategy[Context],
                                         Strategy[Coordinate]]
) -> Strategy[Tuple[Context, Sequence[Polygon]]]:
    def to_context_with_polygons(context_with_border_and_holes
                                 : Tuple[Context, Contour, Sequence[Contour]]
                                 ) -> Tuple[Context, Sequence[Polygon]]:
        context, border, holes = context_with_border_and_holes
        return context, [context.polygon_cls(border, holes)]

    return (to_contexts_with_borders_and_holes_sequences(
            contexts_with_coordinates)
            .map(to_context_with_polygons))


def to_contexts_with_contours_sequences(
        contexts_with_coordinates: Tuple[Strategy[Context],
                                         Strategy[Coordinate]]
) -> Strategy[Tuple[Context, Sequence[Contour]]]:
    def to_context_with_contours_sequence(context_with_convex_hull
                                          : Tuple[Context, Sequence[Point]]
                                          ) -> Tuple[Context,
                                                     Sequence[Contour]]:
        context, convex_hull = context_with_convex_hull
        return context, [context.contour_cls(convex_hull)]

    return (to_contexts_with_convex_hulls(contexts_with_coordinates)
            .map(to_context_with_contours_sequence))


def to_contexts_with_segments_sequences(
        contexts_with_coordinates: Tuple[Strategy[Context],
                                         Strategy[Coordinate]]
) -> Strategy[Tuple[Context, Sequence[Segment]]]:
    def to_context_with_segments(context_with_convex_hull
                                 : Tuple[Context, Sequence[Point]],
                                 center_offset: int
                                 ) -> Tuple[Context, Sequence[Segment]]:
        context, convex_hull = context_with_convex_hull
        center_offset %= len(convex_hull)
        center = convex_hull[center_offset]
        edges = [context.segment_cls(convex_hull[end_index - 1], end)
                 for end_index, end in enumerate(convex_hull)]
        radii = ([context.segment_cls(center, convex_hull[index])
                  for index in range(center_offset == len(convex_hull) - 1,
                                     center_offset - 1)]
                 + [context.segment_cls(center, convex_hull[index])
                    for index in range(center_offset + 2,
                                       len(convex_hull))]
                 if center_offset
                 else
                 [context.segment_cls(center, convex_hull[index])
                  for index in range(2, len(convex_hull) - 1)])
        assert not any(radius in edges for radius in radii)
        return context, edges + radii

    def to_contexts_with_segments_subsets(
            context_with_segments: Tuple[Context, Sequence[Segment]]
    ) -> Strategy[Tuple[Context, Sequence[Segment]]]:
        context, segments = context_with_segments
        return strategies.tuples(strategies.just(context),
                                 sub_lists(segments,
                                           min_size=2))

    return (strategies.builds(
            to_context_with_segments,
            to_contexts_with_convex_hulls(contexts_with_coordinates),
            strategies.integers(0))
            .flatmap(to_contexts_with_segments_subsets))


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
