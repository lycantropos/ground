from itertools import permutations
from typing import Tuple

from hypothesis import given

from ground.base import Context
from ground.hints import Multipoint
from tests.utils import (is_point,
                         permute_multipoint)
from . import strategies


@given(strategies.contexts_with_multipoints)
def test_basic(context_with_multipoint: Tuple[Context, Multipoint]) -> None:
    context, multipoint = context_with_multipoint

    result = context.multipoint_centroid(multipoint)

    assert is_point(result)


@given(strategies.contexts_with_rational_multipoints)
def test_permutations(context_with_multipoint: Tuple[Context, Multipoint]
                      ) -> None:
    context, multipoint = context_with_multipoint

    result = context.multipoint_centroid(multipoint)

    assert all(context.multipoint_centroid(permute_multipoint(multipoint,
                                                              permutation))
               == result
               for permutation in permutations(range(len(multipoint.points))))
