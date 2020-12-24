from typing import (Tuple,
                    Type)

from hypothesis import strategies

from ground.base import (Context,
                         get_context,
                         set_context)
from ground.hints import Coordinate
from tests.hints import Strategy
from tests.strategies.coordinates import coordinates_types_with_strategies
from tests.strategies.geometries import coordinates_to_points
from tests.utils import (to_pairs,
                         to_triplets)

contexts = strategies.builds(get_context)


def to_set_coordinate_strategy(coordinate_type_with_strategy
                               : Tuple[Type[Coordinate], Strategy[Coordinate]]
                               ) -> Strategy[Coordinate]:
    coordinate_type, strategy = coordinate_type_with_strategy
    set_context(Context(coordinate_cls=coordinate_type))
    return strategy


set_coordinates_strategies = (coordinates_types_with_strategies
                              .map(to_set_coordinate_strategy))
points_strategies = set_coordinates_strategies.map(coordinates_to_points)
points_pairs = points_strategies.flatmap(to_pairs)
points_triplets = points_strategies.flatmap(to_triplets)
