from functools import partial
from numbers import Rational
from typing import (Tuple,
                    Type)

from hypothesis import strategies

from ground.base import (Context,
                         Mode,
                         Orientation)
from ground.hints import (Coordinate,
                          Point)
from tests.hints import (PointsQuadruplet,
                         PointsTriplet,
                         Strategy)
from tests.strategies.coordinates import (
    coordinates_types_with_strategies,
    rational_coordinates_types_with_strategies)
from tests.strategies.geometries import (
    coordinates_to_boxes,
    coordinates_to_points,
    coordinates_to_points_sequences,
    points_to_segments_endpoints,
    to_contexts_with_borders_and_holes_sequences,
    to_contexts_with_boxes_and_points,
    to_contexts_with_boxes_and_segments_endpoints,
    to_contexts_with_polygons_sequences,
    to_contexts_with_segments_endpoints_and_points,
    to_contexts_with_segments_pairs_endpoints,
    to_contexts_with_segments_sequences,
    to_contexts_with_vertices_sequences)
from tests.utils import (MAX_SEQUENCE_SIZE,
                         combine,
                         compose,
                         identity,
                         pack,
                         to_pairs,
                         to_quadruplets,
                         to_triplets)

contexts = strategies.builds(Context,
                             mode=strategies.sampled_from(list(Mode)))
contexts_with_empty_lists = strategies.tuples(contexts,
                                              strategies.builds(list))


def to_context_with_coordinates(coordinate_type_with_strategy
                                : Tuple[Type[Coordinate], Strategy[Coordinate]]
                                ) -> Tuple[Strategy[Context],
                                           Strategy[Coordinate]]:
    coordinate_type, strategy = coordinate_type_with_strategy
    return (strategies.builds(Context,
                              mode=strategies.sampled_from(
                                      list(Mode)
                                      if issubclass(coordinate_type, Rational)
                                      else [Mode.EXACT, Mode.ROBUST])),
            strategy)


contexts_with_coordinates_strategies = (coordinates_types_with_strategies
                                        .map(to_context_with_coordinates))
contexts_with_rational_coordinates_strategies = (
    (rational_coordinates_types_with_strategies
     .map(to_context_with_coordinates)))
contexts_with_boxes = (contexts_with_coordinates_strategies
                       .map(combine(identity, coordinates_to_boxes))
                       .flatmap(pack(strategies.tuples)))
contexts_with_boxes_and_points = (contexts_with_coordinates_strategies
                                  .flatmap(to_contexts_with_boxes_and_points))
contexts_with_boxes_and_segments_endpoints = (
    (contexts_with_coordinates_strategies
     .flatmap(to_contexts_with_boxes_and_segments_endpoints)))
contexts_with_boxes_pairs = (contexts_with_coordinates_strategies
                             .map(combine(identity,
                                          compose(to_pairs,
                                                  coordinates_to_boxes)))
                             .flatmap(pack(strategies.tuples)))
contexts_with_boxes_triplets = (contexts_with_coordinates_strategies
                                .map(combine(identity,
                                             compose(to_triplets,
                                                     coordinates_to_boxes)))
                                .flatmap(pack(strategies.tuples)))
contexts_with_points_strategies = (contexts_with_coordinates_strategies
                                   .map(combine(identity,
                                                coordinates_to_points)))
contexts_with_rational_points_strategies = (
    (contexts_with_rational_coordinates_strategies
     .map(combine(identity, coordinates_to_points))))
contexts_with_points = (contexts_with_points_strategies
                        .flatmap(pack(strategies.tuples)))
contexts_with_points_pairs = (contexts_with_points_strategies
                              .map(combine(identity, to_pairs))
                              .flatmap(pack(strategies.tuples)))
contexts_with_rational_points_pairs = (contexts_with_rational_points_strategies
                                       .map(combine(identity, to_pairs))
                                       .flatmap(pack(strategies.tuples)))
contexts_with_points_lists = (
    (contexts_with_points_strategies
     .map(combine(identity, partial(strategies.lists,
                                    max_size=MAX_SEQUENCE_SIZE)))
     .flatmap(pack(strategies.tuples))))
contexts_with_non_empty_points_lists = (
    (contexts_with_points_strategies
     .map(combine(identity, partial(strategies.lists,
                                    min_size=1,
                                    max_size=MAX_SEQUENCE_SIZE)))
     .flatmap(pack(strategies.tuples))))
contexts_with_points_triplets = (contexts_with_points_strategies
                                 .map(combine(identity, to_triplets))
                                 .flatmap(pack(strategies.tuples)))
contexts_with_points_quadruplets = (contexts_with_points_strategies
                                    .map(combine(identity, to_quadruplets))
                                    .flatmap(pack(strategies.tuples)))


def to_contexts_with_touching_segments_endpoints(
        contexts_with_points: Strategy[Tuple[Strategy[Context],
                                             Strategy[Point]]]
) -> Strategy[Tuple[Context, PointsQuadruplet]]:
    def to_context_with_segments_pairs_endpoints(
            context_with_angle_points: Tuple[Context, PointsTriplet]
    ) -> Tuple[Context, PointsQuadruplet]:
        context, angle_points = context_with_angle_points
        vertex, first_ray_point, second_ray_point = angle_points
        return context, (vertex, first_ray_point, vertex, second_ray_point)

    return (to_context_with_non_zero_angles(contexts_with_points)
            .map(to_context_with_segments_pairs_endpoints))


def to_contexts_with_crossing_segments_pairs_endpoints(
        contexts_with_points: Strategy[Tuple[Strategy[Context],
                                             Strategy[Point]]]
) -> Strategy[Tuple[Context, PointsQuadruplet]]:
    def to_context_with_segments_pairs_endpoints(
            context_with_angle_points: Tuple[Context, PointsTriplet],
            first_scale: int,
            second_scale: int) -> Tuple[Context, PointsQuadruplet]:
        context, angle_points = context_with_angle_points
        vertex, first_ray_point, second_ray_point = angle_points
        return context, (to_scaled_segment_end(context, first_ray_point,
                                               vertex, first_scale),
                         first_ray_point,
                         to_scaled_segment_end(context, second_ray_point,
                                               vertex, second_scale),
                         second_ray_point)

    def to_scaled_segment_end(context: Context,
                              start: Point,
                              end: Point,
                              scale: int) -> Point:
        return context.point_cls(end.x + scale * (end.x - start.x),
                                 end.y + scale * (end.y - start.y))

    scales = strategies.integers(1, 100)
    return strategies.builds(
            to_context_with_segments_pairs_endpoints,
            to_context_with_non_zero_sine_angles(contexts_with_points),
            scales, scales)


def to_context_with_non_zero_angles(
        contexts_with_points: Strategy[Tuple[Strategy[Context],
                                             Strategy[Point]]]
) -> Strategy[Tuple[Context, PointsTriplet]]:
    def is_non_zero_angle(context_with_angle_points
                          : Tuple[Context, PointsTriplet]) -> bool:
        context, angle_points = context_with_angle_points
        vertex, first_ray_point, second_ray_point = angle_points
        return (second_ray_point < min(vertex, first_ray_point)
                or (context.angle_orientation(vertex, first_ray_point,
                                              second_ray_point)
                    is not Orientation.COLLINEAR))

    return (contexts_with_points
            .map(combine(identity, partial(strategies.lists,
                                           min_size=3,
                                           max_size=3,
                                           unique=True)))
            .flatmap(pack(strategies.tuples))
            .filter(is_non_zero_angle))


def to_context_with_non_zero_sine_angles(
        contexts_with_points: Strategy[Tuple[Strategy[Context],
                                             Strategy[Point]]]
) -> Strategy[Tuple[Context, PointsTriplet]]:
    def is_non_zero_sine_angle(context_with_angle_points
                               : Tuple[Context, PointsTriplet]) -> bool:
        context, angle_points = context_with_angle_points
        vertex, first_ray_point, second_ray_point = angle_points
        return (context.angle_orientation(vertex, first_ray_point,
                                          second_ray_point)
                is not Orientation.COLLINEAR)

    return (contexts_with_points
            .map(combine(identity, partial(strategies.lists,
                                           min_size=3,
                                           max_size=3,
                                           unique=True)))
            .flatmap(pack(strategies.tuples))
            .filter(is_non_zero_sine_angle))


contexts_with_segments_endpoints = (
    (contexts_with_points_strategies
     .map(combine(identity, points_to_segments_endpoints))
     .flatmap(pack(strategies.tuples))))
contexts_with_segments_pairs_endpoints = (
    (contexts_with_points_strategies
     .flatmap(to_contexts_with_segments_pairs_endpoints)))
contexts_with_segments_endpoints_and_points = (
    (contexts_with_points_strategies
     .flatmap(to_contexts_with_segments_endpoints_and_points)))
contexts_with_crossing_or_touching_segments_pairs_endpoints = (
        to_contexts_with_crossing_segments_pairs_endpoints(
                contexts_with_points_strategies)
        |
        to_contexts_with_touching_segments_endpoints(
                contexts_with_points_strategies))
contexts_with_points_sequences = (
    (contexts_with_coordinates_strategies
     .map(combine(identity, coordinates_to_points_sequences))
     .flatmap(pack(strategies.tuples))))
contexts_with_rational_points_sequences = (
    (contexts_with_rational_coordinates_strategies
     .map(combine(identity, coordinates_to_points_sequences))
     .flatmap(pack(strategies.tuples))))
contexts_with_vertices = (
    (contexts_with_coordinates_strategies
     .flatmap(to_contexts_with_vertices_sequences)))
contexts_with_rational_vertices = (
    (contexts_with_rational_coordinates_strategies
     .flatmap(to_contexts_with_vertices_sequences)))
contexts_with_borders_and_holes_sequences = (
    (contexts_with_coordinates_strategies
     .flatmap(to_contexts_with_borders_and_holes_sequences)))
contexts_with_rational_borders_and_holes_sequences = (
    (contexts_with_rational_coordinates_strategies
     .flatmap(to_contexts_with_borders_and_holes_sequences)))
contexts_with_polygons_sequences = (
    (contexts_with_coordinates_strategies
     .flatmap(to_contexts_with_polygons_sequences)))
contexts_with_rational_polygons_sequences = (
    (contexts_with_rational_coordinates_strategies
     .flatmap(to_contexts_with_polygons_sequences)))
contexts_with_segments_sequences = (
    (contexts_with_coordinates_strategies
     .flatmap(to_contexts_with_segments_sequences)))
contexts_with_rational_segments_sequences = (
    (contexts_with_rational_coordinates_strategies
     .flatmap(to_contexts_with_segments_sequences)))
