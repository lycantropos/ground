from operator import attrgetter

from hypothesis import strategies

from ground.core.incircle import (plain_context,
                                  robust_context)
from tests.strategies.geometries import (points_strategies,
                                         rational_points_strategies)
from tests.utils import (to_quadruplets,
                         to_triplets)

contexts = strategies.sampled_from([plain_context, robust_context])
point_point_point_determinants = contexts.map(
        attrgetter('point_point_point_determinant'))
points_quadruplets = points_strategies.flatmap(to_quadruplets)
points_triplets = points_strategies.flatmap(to_triplets)
rational_points_quadruplets = (rational_points_strategies
                               .flatmap(to_quadruplets))
