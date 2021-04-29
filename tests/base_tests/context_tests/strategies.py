import sys
from functools import partial
from operator import itemgetter

from hypothesis import strategies

from ground.base import (Context,
                         Mode)
from tests.strategies.coordinates import (coordinates_strategies,
                                          rational_coordinates_strategies)
from tests.strategies.geometries import (to_borders_and_holes_sequences,
                                         to_boxes,
                                         to_contours,
                                         to_contours_sequences,
                                         to_crossing_segments_pairs,
                                         to_crossing_segments_pairs_endpoints,
                                         to_multipoints,
                                         to_points,
                                         to_polygons_sequences,
                                         to_segments,
                                         to_segments_endpoints,
                                         to_segments_sequences,
                                         to_touching_segments_pairs,
                                         to_touching_segments_pairs_endpoints,
                                         to_vertices_sequences)
from tests.utils import (MAX_SEQUENCE_SIZE,
                         cleave_in_tuples,
                         compose,
                         pack,
                         to_pairs,
                         to_quadruplets,
                         to_triplets)

indices = strategies.integers(0, sys.maxsize)
contexts = strategies.builds(Context,
                             mode=strategies.sampled_from(list(Mode)))
contexts_with_empty_lists = strategies.tuples(contexts,
                                              strategies.builds(list))
contexts_with_rational_coordinates_strategies = strategies.tuples(
        contexts, rational_coordinates_strategies)
contexts_with_coordinates_strategies = strategies.tuples(
        contexts, coordinates_strategies)
to_contexts_with = partial(cleave_in_tuples,
                           compose(strategies.just, itemgetter(0)))
borders_and_holes_sequences_factory = pack(to_borders_and_holes_sequences)
boxes_factory = pack(to_boxes)
contours_factory = pack(to_contours)
crossing_segments_pairs_endpoints_factory = pack(
        to_crossing_segments_pairs_endpoints)
crossing_segments_pairs_factory = pack(to_crossing_segments_pairs)
multipoints_factory = pack(to_multipoints)
points_factory = pack(to_points)
polygons_sequences_factory = pack(to_polygons_sequences)
segments_endpoints_factory = pack(to_segments_endpoints)
segments_factory = pack(to_segments)
segments_sequences_factory = pack(to_segments_sequences)
touching_segments_endpoints_factory = pack(
        to_touching_segments_pairs_endpoints)
touching_segments_pairs_factory = pack(to_touching_segments_pairs)
vertices_sequences_factories = pack(to_vertices_sequences)

contexts_with_boxes = (contexts_with_coordinates_strategies
                       .flatmap(to_contexts_with(boxes_factory)))
contexts_with_boxes_pairs = contexts_with_coordinates_strategies.flatmap(
        to_contexts_with(compose(to_pairs, boxes_factory)))
contexts_with_boxes_triplets = contexts_with_coordinates_strategies.flatmap(
        to_contexts_with(compose(to_triplets, boxes_factory)))
contexts_with_boxes_and_points = (contexts_with_coordinates_strategies
                                  .flatmap(to_contexts_with(boxes_factory,
                                                            points_factory)))
contexts_with_rational_boxes_and_segments = (
    contexts_with_rational_coordinates_strategies.flatmap(to_contexts_with(
            boxes_factory, segments_factory)))
contexts_with_boxes_and_segments = (
    contexts_with_coordinates_strategies.flatmap(to_contexts_with(
            boxes_factory, segments_factory)))
contexts_with_points = (contexts_with_coordinates_strategies
                        .flatmap(to_contexts_with(points_factory)))
contexts_with_points_pairs = (
    contexts_with_coordinates_strategies.flatmap(to_contexts_with(compose(
            to_pairs, points_factory))))
contexts_with_rational_points_pairs = (
    contexts_with_rational_coordinates_strategies.flatmap(
            to_contexts_with(compose(to_pairs, points_factory))))
contexts_with_points_lists = (
    contexts_with_coordinates_strategies.flatmap(to_contexts_with(
            compose(partial(strategies.lists,
                            max_size=MAX_SEQUENCE_SIZE),
                    points_factory))))
contexts_with_non_empty_points_lists = (
    contexts_with_coordinates_strategies.flatmap(to_contexts_with(
            compose(partial(strategies.lists,
                            min_size=1,
                            max_size=MAX_SEQUENCE_SIZE),
                    points_factory))))
contexts_with_points_triplets = (
    contexts_with_coordinates_strategies.flatmap(to_contexts_with(
            compose(to_triplets, points_factory))))
contexts_with_points_quadruplets = (
    contexts_with_coordinates_strategies.flatmap(to_contexts_with(
            compose(to_quadruplets, points_factory))))
contexts_with_rational_segments_endpoints = (
    contexts_with_rational_coordinates_strategies.flatmap(to_contexts_with(
            segments_endpoints_factory)))
contexts_with_segments_endpoints = (
    contexts_with_coordinates_strategies.flatmap(to_contexts_with(
            segments_endpoints_factory)))
contexts_with_rational_segments_endpoints_pairs = (
    contexts_with_rational_coordinates_strategies.flatmap(to_contexts_with(
            compose(to_pairs, segments_endpoints_factory))))
contexts_with_segments_endpoints_pairs = (
    contexts_with_coordinates_strategies.flatmap(to_contexts_with(
            compose(to_pairs, segments_endpoints_factory))))
contexts_with_rational_segments = (
    contexts_with_rational_coordinates_strategies.flatmap(to_contexts_with(
            segments_factory)))
contexts_with_segments = (
    contexts_with_coordinates_strategies.flatmap(to_contexts_with(
            segments_factory)))
contexts_with_rational_segments_and_points = (
    contexts_with_rational_coordinates_strategies.flatmap(to_contexts_with(
            segments_factory, points_factory)))
contexts_with_segments_and_points = (
    contexts_with_coordinates_strategies.flatmap(to_contexts_with(
            segments_factory, points_factory)))
contexts_with_rational_segments_endpoints_and_points = (
    (contexts_with_rational_coordinates_strategies
     .flatmap(to_contexts_with(segments_endpoints_factory, points_factory))))
contexts_with_segments_endpoints_and_points = (
    (contexts_with_coordinates_strategies
     .flatmap(to_contexts_with(segments_endpoints_factory, points_factory))))
contexts_with_rational_crossing_or_touching_segments_pairs_endpoints = (
        contexts_with_rational_coordinates_strategies.flatmap(
                to_contexts_with(crossing_segments_pairs_endpoints_factory))
        |
        contexts_with_coordinates_strategies.flatmap(to_contexts_with(
                touching_segments_endpoints_factory)))
contexts_with_crossing_or_touching_segments_pairs_endpoints = (
        contexts_with_coordinates_strategies.flatmap(to_contexts_with(
                crossing_segments_pairs_endpoints_factory))
        |
        contexts_with_coordinates_strategies.flatmap(to_contexts_with(
                touching_segments_endpoints_factory)))
contexts_with_rational_crossing_or_touching_segments_pairs = (
        contexts_with_rational_coordinates_strategies.flatmap(
                to_contexts_with(crossing_segments_pairs_factory))
        |
        contexts_with_coordinates_strategies.flatmap(to_contexts_with(
                touching_segments_pairs_factory)))
contexts_with_crossing_or_touching_segments_pairs = (
        contexts_with_coordinates_strategies.flatmap(to_contexts_with(
                crossing_segments_pairs_factory))
        |
        contexts_with_coordinates_strategies.flatmap(to_contexts_with(
                touching_segments_pairs_factory)))
contexts_with_multipoints = (
    contexts_with_coordinates_strategies.flatmap(to_contexts_with(
            multipoints_factory)))
contexts_with_rational_multipoints = (
    contexts_with_rational_coordinates_strategies.flatmap(to_contexts_with(
            multipoints_factory)))
contexts_with_contours = contexts_with_coordinates_strategies.flatmap(
        to_contexts_with(contours_factory))
contexts_with_rational_contours = (
    contexts_with_rational_coordinates_strategies.flatmap(to_contexts_with(
            contours_factory)))
contexts_with_vertices = contexts_with_coordinates_strategies.flatmap(
        to_contexts_with(vertices_sequences_factories))
contexts_with_rational_vertices = (
    contexts_with_rational_coordinates_strategies.flatmap(to_contexts_with(
            vertices_sequences_factories)))
contexts_with_borders_and_holes_sequences = (
    contexts_with_coordinates_strategies.flatmap(to_contexts_with(
            borders_and_holes_sequences_factory)))
contexts_with_contours_sequences = (
    (contexts_with_coordinates_strategies
     .flatmap(to_contexts_with(pack(to_contours_sequences)))))
contexts_with_rational_borders_and_holes_sequences = (
    contexts_with_rational_coordinates_strategies.flatmap(to_contexts_with(
            borders_and_holes_sequences_factory)))
contexts_with_polygons_sequences = (
    contexts_with_coordinates_strategies.flatmap(to_contexts_with(
            polygons_sequences_factory)))
contexts_with_rational_polygons_sequences = (
    contexts_with_rational_coordinates_strategies.flatmap(to_contexts_with(
            polygons_sequences_factory)))
contexts_with_segments_sequences = (
    contexts_with_coordinates_strategies.flatmap(to_contexts_with(
            segments_sequences_factory)))
contexts_with_rational_segments_sequences = (
    contexts_with_rational_coordinates_strategies.flatmap(to_contexts_with(
            segments_sequences_factory)))
