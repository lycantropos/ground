from typing import Tuple

from hypothesis import given

from ground.base import Context
from ground.hints import (Multisegment,
                          Scalar)
from tests.utils import (reverse_multisegment,
                         reverse_multisegment_coordinates)
from . import strategies


@given(strategies.contexts_with_multisegments_and_scalars_pairs)
def test_basic(context_with_multisegment_and_steps
               : Tuple[Context, Multisegment, Scalar, Scalar]) -> None:
    context, multisegment, step_x, step_y = context_with_multisegment_and_steps

    result = context.translate_multisegment(multisegment, step_x, step_y)

    assert isinstance(result, context.multisegment_cls)


@given(strategies.contexts_with_multisegments_and_scalars_pairs)
def test_reversals(context_with_multisegment_and_steps
                   : Tuple[Context, Multisegment, Scalar, Scalar]) -> None:
    context, multisegment, step_x, step_y = context_with_multisegment_and_steps

    result = context.translate_multisegment(multisegment, step_x, step_y)

    assert reverse_multisegment(result) == context.translate_multisegment(
            reverse_multisegment(multisegment), step_x, step_y)
    assert (reverse_multisegment_coordinates(result)
            == context.translate_multisegment(
                    reverse_multisegment_coordinates(multisegment), step_y,
                    step_x))
