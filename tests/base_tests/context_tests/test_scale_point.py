from typing import Tuple

from hypothesis import given

from ground.base import Context
from ground.hints import (Point,
                          Scalar)
from tests.utils import reverse_point_coordinates
from . import strategies


@given(strategies.contexts_with_points_and_scalars_pairs)
def test_basic(context_with_point_and_factors
               : Tuple[Context, Point, Scalar, Scalar]) -> None:
    context, point, factor_x, factor_y = context_with_point_and_factors

    result = context.scale_point(point, factor_x, factor_y)

    assert isinstance(result, context.point_cls)


@given(strategies.contexts_with_points_and_scalars_pairs)
def test_reversals(context_with_point_and_factors
                   : Tuple[Context, Point, Scalar, Scalar]) -> None:
    context, point, factor_x, factor_y = context_with_point_and_factors

    result = context.scale_point(point, factor_x, factor_y)

    assert reverse_point_coordinates(result) == context.scale_point(
            reverse_point_coordinates(point), factor_y, factor_x)
