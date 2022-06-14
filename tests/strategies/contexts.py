from hypothesis import strategies

from ground.base import (Context,
                         Mode)
from .coordinates import (rational_coordinates_strategies,
                          real_coordinates_strategies)

rational_contexts = strategies.builds(Context,
                                      mode=strategies.sampled_from(list(Mode)))
real_contexts = strategies.builds(Context,
                                  mode=strategies.sampled_from([Mode.EXACT,
                                                                Mode.ROBUST]))
rational_contexts_with_coordinates_strategies = strategies.tuples(
        rational_contexts, rational_coordinates_strategies
)
real_contexts_with_coordinates_strategies = strategies.tuples(
        real_contexts, real_coordinates_strategies
)
contexts_with_coordinates_strategies = (
        rational_contexts_with_coordinates_strategies
        | real_contexts_with_coordinates_strategies
)
