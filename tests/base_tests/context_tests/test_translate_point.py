from typing import Tuple

from hypothesis import given

from ground.base import Context
from ground.hints import (Point,
                          Scalar)
from tests.utils import reverse_point_coordinates
from . import strategies


@given(strategies.contexts_with_points_and_scalars_pairs)
def test_basic(context_with_point_and_steps
               : Tuple[Context, Point, Scalar, Scalar]) -> None:
    context, point, step_x, step_y = context_with_point_and_steps

    result = context.translate_point(point, step_x, step_y)

    assert isinstance(result, context.point_cls)


@given(strategies.contexts_with_rational_points_and_scalars_pairs)
def test_round_trip(context_with_point_and_steps
                    : Tuple[Context, Point, Scalar, Scalar]) -> None:
    context, point, step_x, step_y = context_with_point_and_steps

    result = context.translate_point(point, step_x, step_y)

    assert (context.translate_point(result, -step_x, -step_y)
            == context.translate_point(point, 0, 0))


@given(strategies.contexts_with_points_and_scalars_pairs)
def test_reversals(context_with_point_and_steps
                   : Tuple[Context, Point, Scalar, Scalar]) -> None:
    context, point, step_x, step_y = context_with_point_and_steps

    result = context.translate_point(point, step_x, step_y)

    assert reverse_point_coordinates(result) == context.translate_point(
            reverse_point_coordinates(point), step_y, step_x)
