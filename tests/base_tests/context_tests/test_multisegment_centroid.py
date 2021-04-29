from typing import Tuple

from hypothesis import given

from ground.base import Context
from ground.hints import Multisegment
from tests.utils import (is_point,
                         reverse_multisegment,
                         reverse_multisegment_coordinates,
                         reverse_point_coordinates,
                         rotate_multisegment)
from . import strategies


@given(strategies.contexts_with_multisegments)
def test_basic(context_with_multisegment: Tuple[Context, Multisegment]
               ) -> None:
    context, multisegment = context_with_multisegment

    result = context.multisegment_centroid(multisegment)

    assert is_point(result)


@given(strategies.contexts_with_rational_multisegments)
def test_reversals(context_with_multisegment: Tuple[Context, Multisegment]
                   ) -> None:
    context, multisegment = context_with_multisegment

    result = context.multisegment_centroid(multisegment)

    assert result == context.multisegment_centroid(reverse_multisegment(
            multisegment))
    assert result == reverse_point_coordinates(context.multisegment_centroid(
            reverse_multisegment_coordinates(multisegment)))


@given(strategies.contexts_with_multisegments, strategies.indices)
def test_rotations(context_with_multisegment: Tuple[Context, Multisegment],
                   offset: int) -> None:
    context, multisegment = context_with_multisegment

    result = context.multisegment_centroid(multisegment)

    assert result == context.multisegment_centroid(rotate_multisegment(
            multisegment, offset))
