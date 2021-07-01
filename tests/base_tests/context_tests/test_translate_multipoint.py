from typing import Tuple

from hypothesis import given

from ground.base import Context
from ground.hints import (Multipoint,
                          Scalar)
from tests.utils import (reverse_multipoint,
                         reverse_multipoint_coordinates)
from . import strategies


@given(strategies.contexts_with_multipoints_and_scalars_pairs)
def test_basic(context_with_multipoint_and_steps
               : Tuple[Context, Multipoint, Scalar, Scalar]) -> None:
    context, multipoint, step_x, step_y = context_with_multipoint_and_steps

    result = context.translate_multipoint(multipoint, step_x, step_y)

    assert isinstance(result, context.multipoint_cls)


@given(strategies.contexts_with_rational_multipoints_and_scalars_pairs)
def test_round_trip(context_with_multipoint_and_steps
                    : Tuple[Context, Multipoint, Scalar, Scalar]) -> None:
    context, multipoint, step_x, step_y = context_with_multipoint_and_steps

    result = context.translate_multipoint(multipoint, step_x, step_y)

    assert (context.translate_multipoint(result, -step_x, -step_y)
            == context.translate_multipoint(multipoint, 0, 0))


@given(strategies.contexts_with_multipoints_and_scalars_pairs)
def test_reversals(context_with_multipoint_and_steps
                   : Tuple[Context, Multipoint, Scalar, Scalar]) -> None:
    context, multipoint, step_x, step_y = context_with_multipoint_and_steps

    result = context.translate_multipoint(multipoint, step_x, step_y)

    assert reverse_multipoint(result) == context.translate_multipoint(
            reverse_multipoint(multipoint), step_x, step_y)
    assert (reverse_multipoint_coordinates(result)
            == context.translate_multipoint(
                    reverse_multipoint_coordinates(multipoint), step_y,
                    step_x))
