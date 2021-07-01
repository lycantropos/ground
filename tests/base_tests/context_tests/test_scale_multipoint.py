from typing import Tuple

from hypothesis import given

from ground.base import Context
from ground.hints import (Multipoint,
                          Scalar)
from tests.utils import (reverse_multipoint,
                         reverse_multipoint_coordinates)
from . import strategies


@given(strategies.contexts_with_multipoints_and_scalars_pairs)
def test_basic(context_with_multipoint_and_factors
               : Tuple[Context, Multipoint, Scalar, Scalar]) -> None:
    (context, multipoint, factor_x,
     factor_y) = context_with_multipoint_and_factors

    result = context.scale_multipoint(multipoint, factor_x, factor_y)

    assert isinstance(result, context.multipoint_cls)


@given(strategies.contexts_with_multipoints_and_scalars_pairs)
def test_reversals(context_with_multipoint_and_factors
                   : Tuple[Context, Multipoint, Scalar, Scalar]) -> None:
    (context, multipoint, factor_x,
     factor_y) = context_with_multipoint_and_factors

    result = context.scale_multipoint(multipoint, factor_x, factor_y)

    assert reverse_multipoint(result) == context.scale_multipoint(
            reverse_multipoint(multipoint), factor_x, factor_y)
    assert (reverse_multipoint_coordinates(result)
            == context.scale_multipoint(
                    reverse_multipoint_coordinates(multipoint), factor_y,
                    factor_x))
