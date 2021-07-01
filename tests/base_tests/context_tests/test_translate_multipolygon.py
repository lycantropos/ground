from typing import Tuple

from hypothesis import given

from ground.base import Context
from ground.hints import (Multipolygon,
                          Scalar)
from tests.utils import (reverse_multipolygon,
                         reverse_multipolygon_coordinates)
from . import strategies


@given(strategies.contexts_with_multipolygons_and_scalars_pairs)
def test_basic(context_with_multipolygon_and_steps
               : Tuple[Context, Multipolygon, Scalar, Scalar]) -> None:
    context, multipolygon, step_x, step_y = context_with_multipolygon_and_steps

    result = context.translate_multipolygon(multipolygon, step_x, step_y)

    assert isinstance(result, context.multipolygon_cls)


@given(strategies.contexts_with_rational_multipolygons_and_scalars_pairs)
def test_round_trip(context_with_multipolygon_and_steps
                    : Tuple[Context, Multipolygon, Scalar, Scalar]) -> None:
    context, multipolygon, step_x, step_y = context_with_multipolygon_and_steps

    result = context.translate_multipolygon(multipolygon, step_x, step_y)

    assert (context.translate_multipolygon(result, -step_x, -step_y)
            == context.translate_multipolygon(multipolygon, 0, 0))


@given(strategies.contexts_with_multipolygons_and_scalars_pairs)
def test_reversals(context_with_multipolygon_and_steps
                   : Tuple[Context, Multipolygon, Scalar, Scalar]) -> None:
    context, multipolygon, step_x, step_y = context_with_multipolygon_and_steps

    result = context.translate_multipolygon(multipolygon, step_x, step_y)

    assert reverse_multipolygon(result) == context.translate_multipolygon(
            reverse_multipolygon(multipolygon), step_x, step_y)
    assert (reverse_multipolygon_coordinates(result)
            == context.translate_multipolygon(
                    reverse_multipolygon_coordinates(multipolygon), step_y,
                    step_x))
