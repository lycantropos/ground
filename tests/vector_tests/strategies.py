from operator import attrgetter

from hypothesis import strategies

from ground.core.vector import (plain_context,
                                robust_context)
from tests.strategies.geometries import points_strategies
from tests.utils import (to_pairs,
                         to_quadruplets,
                         to_triplets)

contexts = strategies.sampled_from([plain_context, robust_context])
cross_products = contexts.map(attrgetter('cross_product'))
dot_products = contexts.map(attrgetter('dot_product'))
points_pairs = points_strategies.flatmap(to_pairs)
points_quadruplets = points_strategies.flatmap(to_quadruplets)
points_triplets = points_strategies.flatmap(to_triplets)
