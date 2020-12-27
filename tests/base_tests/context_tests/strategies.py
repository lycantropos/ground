from functools import partial
from operator import add
from typing import (Tuple,
                    Type)

from hypothesis import strategies

from ground.base import Context
from ground.hints import (Coordinate,
                          Point)
from tests.hints import (PointsPair,
                         Strategy)
from tests.strategies.coordinates import (
    coordinates_types,
    coordinates_types_with_strategies,
    rational_coordinates_types_with_strategies)
from tests.strategies.geometries import (context_with_coordinates_to_contours,
                                         coordinates_to_multipoints,
                                         coordinates_to_points)
from tests.utils import (MAX_SEQUENCE_SIZE,
                         combine,
                         compose,
                         identity,
                         pack,
                         to_pairs,
                         to_quadruplets,
                         to_triplets)

contexts = strategies.builds(Context,
                             coordinate_cls=coordinates_types)
contexts_with_empty_lists = strategies.tuples(contexts,
                                              strategies.builds(list))


def to_context_with_coordinates(coordinate_type_with_strategy
                                : Tuple[Type[Coordinate], Strategy[Coordinate]]
                                ) -> Tuple[Strategy[Context],
                                           Strategy[Coordinate]]:
    coordinate_type, strategy = coordinate_type_with_strategy
    return (strategies.builds(Context,
                              coordinate_cls=strategies.just(coordinate_type)),
            strategy)


contexts_with_coordinates_strategies = (coordinates_types_with_strategies
                                        .map(to_context_with_coordinates))
contexts_with_rational_coordinates_strategies = (
    (rational_coordinates_types_with_strategies
     .map(to_context_with_coordinates)))
contexts_with_points_strategies = (contexts_with_coordinates_strategies
                                   .map(combine(identity,
                                                coordinates_to_points)))
contexts_with_points_pairs = (contexts_with_points_strategies
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


def points_to_segments_endpoints(points: Strategy[Point]
                                 ) -> Strategy[PointsPair]:
    return (strategies.lists(points,
                             min_size=2,
                             max_size=2,
                             unique=True)
            .map(tuple))


contexts_with_segments_endpoints = (
    (contexts_with_points_strategies
     .map(combine(identity, points_to_segments_endpoints))
     .flatmap(pack(strategies.tuples))))
contexts_with_segments_pairs_endpoints = (
    (contexts_with_points_strategies
     .map(combine(identity, compose(to_pairs, points_to_segments_endpoints)))
     .flatmap(pack(strategies.tuples))
     .map(combine(identity, pack(add)))))
contexts_with_multipoints = (contexts_with_coordinates_strategies
                             .map(combine(identity,
                                          coordinates_to_multipoints))
                             .flatmap(pack(strategies.tuples)))
contexts_with_rational_multipoints = (
    (contexts_with_rational_coordinates_strategies
     .map(combine(identity, coordinates_to_multipoints))
     .flatmap(pack(strategies.tuples))))
contexts_with_contours = (contexts_with_coordinates_strategies
                          .map(context_with_coordinates_to_contours)
                          .flatmap(pack(strategies.tuples)))
contexts_with_rational_contours = (
    (contexts_with_rational_coordinates_strategies
     .map(context_with_coordinates_to_contours)
     .flatmap(pack(strategies.tuples))))
