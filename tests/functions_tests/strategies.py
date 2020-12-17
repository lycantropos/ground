from operator import attrgetter

from hypothesis import strategies

from ground.functions import (plain_context,
                              robust_context)
from tests.strategies.geometries import (points_strategies,
                                         rational_points_strategies)
from tests.utils import (to_pairs,
                         to_quadruplets,
                         to_triplets)

contexts = strategies.sampled_from([plain_context, robust_context])
cross_producers = contexts.map(attrgetter('cross_producer'))
dot_producers = contexts.map(attrgetter('dot_producer'))
incircle_determiners = contexts.map(attrgetter('incircle_determiner'))
points_pairs = points_strategies.flatmap(to_pairs)
points_quadruplets = points_strategies.flatmap(to_quadruplets)
points_triplets = points_strategies.flatmap(to_triplets)
rational_points_quadruplets = (rational_points_strategies
                               .flatmap(to_quadruplets))
