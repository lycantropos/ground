from hypothesis import strategies

from ground.functions import (plain_context,
                              robust_context)

contexts = strategies.sampled_from([plain_context, robust_context])
