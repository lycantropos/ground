from hypothesis import strategies

from ground.coordinates import (float_context,
                                rational_context,
                                real_context)

contexts = strategies.sampled_from([float_context, rational_context,
                                    real_context])
